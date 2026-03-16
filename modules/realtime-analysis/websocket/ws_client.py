#!/usr/bin/env python3
"""
WebSocket 클라이언트
실시간 데이터 스트림 연결 관리

기능:
- 비동기 WebSocket 연결
- 자동 재연결
- 하트비트 관리
- 메시지 처리
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import logging


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionState(Enum):
    """연결 상태"""
    DISCONNECTED = 'disconnected'
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    RECONNECTING = 'reconnecting'
    CLOSING = 'closing'
    CLOSED = 'closed'
    ERROR = 'error'


@dataclass
class WebSocketConfig:
    """WebSocket 설정"""
    url: str
    subscribe_message: Optional[Dict] = None
    headers: Optional[Dict] = None
    ping_interval: float = 30.0           # 초 단위
    ping_timeout: float = 10.0
    reconnect_delay: float = 5.0
    max_reconnect_attempts: int = 10
    message_queue_size: int = 1000


@dataclass
class ConnectionStats:
    """연결 통계"""
    connected_at: Optional[str] = None
    last_message_at: Optional[str] = None
    message_count: int = 0
    reconnect_count: int = 0
    error_count: int = 0
    bytes_received: int = 0


class WebSocketClient:
    """
    WebSocket 클라이언트

    사용법:
        client = WebSocketClient(WebSocketConfig(
            url='wss://stream.binance.com:9443/ws/btcusdt@ticker'
        ))
        client.on_message = lambda msg: print(msg)
        await client.connect()
    """

    def __init__(self, config: WebSocketConfig):
        """
        초기화

        Args:
            config: WebSocket 설정
        """
        self.config = config
        self.state = ConnectionState.DISCONNECTED
        self.stats = ConnectionStats()

        self._ws = None
        self._task: Optional[asyncio.Task] = None
        self._ping_task: Optional[asyncio.Task] = None
        self._reconnect_attempts = 0
        self._running = False

        # 콜백
        self.on_message: Optional[Callable[[Dict], None]] = None
        self.on_connect: Optional[Callable[[], None]] = None
        self.on_disconnect: Optional[Callable[[], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None

    async def connect(self) -> bool:
        """
        WebSocket 연결

        Returns:
            연결 성공 여부
        """
        if self.state in [ConnectionState.CONNECTED, ConnectionState.CONNECTING]:
            logger.warning("이미 연결 중이거나 연결됨")
            return False

        self._running = True
        self.state = ConnectionState.CONNECTING

        try:
            # websockets 라이브러리 사용 (설치 필요: pip install websockets)
            # 실제 구현에서는 websockets 또는 aiohttp 사용
            # 여기서는 시뮬레이션
            logger.info(f"연결 시도: {self.config.url}")

            # 연결 성공 시뮬레이션
            await asyncio.sleep(0.5)

            self.state = ConnectionState.CONNECTED
            self.stats.connected_at = datetime.now().isoformat()
            self._reconnect_attempts = 0

            logger.info("연결 성공")

            if self.on_connect:
                self.on_connect()

            # 구독 메시지 전송
            if self.config.subscribe_message:
                await self._send(self.config.subscribe_message)
                logger.info(f"구독 메시지 전송: {self.config.subscribe_message}")

            # 메시지 수신 태스크 시작
            self._task = asyncio.create_task(self._receive_loop())

            # 핑 태스크 시작
            self._ping_task = asyncio.create_task(self._ping_loop())

            return True

        except Exception as e:
            self.state = ConnectionState.ERROR
            self.stats.error_count += 1
            logger.error(f"연결 실패: {e}")

            if self.on_error:
                self.on_error(e)

            return False

    async def disconnect(self):
        """연결 해제"""
        self._running = False
        self.state = ConnectionState.CLOSING

        # 태스크 취소
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        if self._ping_task:
            self._ping_task.cancel()
            try:
                await self._ping_task
            except asyncio.CancelledError:
                pass

        # WebSocket 연결 종료
        if self._ws:
            # await self._ws.close()
            self._ws = None

        self.state = ConnectionState.CLOSED
        logger.info("연결 해제됨")

        if self.on_disconnect:
            self.on_disconnect()

    async def _send(self, data: Dict):
        """메시지 전송"""
        if self.state != ConnectionState.CONNECTED:
            logger.warning("연결되지 않음")
            return

        try:
            message = json.dumps(data)
            # await self._ws.send(message)
            logger.debug(f"전송: {message}")
        except Exception as e:
            logger.error(f"전송 실패: {e}")

    async def _receive_loop(self):
        """메시지 수신 루프"""
        while self._running:
            try:
                # 실제 구현에서는 websocket에서 메시지 수신
                # message = await self._ws.recv()

                # 시뮬레이션: 1초마다 더미 메시지 생성
                await asyncio.sleep(1)

                if self.state != ConnectionState.CONNECTED:
                    break

                # 더미 메시지
                message = json.dumps({
                    'e': 'ticker',
                    's': 'BTCUSDT',
                    'c': '50000.00',
                    'v': '12345.67',
                    'E': int(datetime.now().timestamp() * 1000)
                })

                self.stats.message_count += 1
                self.stats.bytes_received += len(message)
                self.stats.last_message_at = datetime.now().isoformat()

                if self.on_message:
                    try:
                        data = json.loads(message)
                        self.on_message(data)
                    except json.JSONDecodeError:
                        logger.warning(f"JSON 파싱 실패: {message}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"수신 오류: {e}")
                self.stats.error_count += 1

                if self._running:
                    await self._reconnect()
                break

    async def _ping_loop(self):
        """핑 루프 (연결 유지)"""
        while self._running:
            try:
                await asyncio.sleep(self.config.ping_interval)

                if self.state == ConnectionState.CONNECTED:
                    # await self._ws.ping()
                    logger.debug("Ping 전송")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Ping 오류: {e}")

    async def _reconnect(self):
        """재연결"""
        if not self._running:
            return

        if self._reconnect_attempts >= self.config.max_reconnect_attempts:
            logger.error(f"최대 재연결 시도 초과 ({self.config.max_reconnect_attempts}회)")
            self.state = ConnectionState.ERROR
            return

        self.state = ConnectionState.RECONNECTING
        self._reconnect_attempts += 1
        self.stats.reconnect_count += 1

        logger.info(f"재연결 시도 {self._reconnect_attempts}/{self.config.max_reconnect_attempts}")

        await asyncio.sleep(self.config.reconnect_delay)

        if self._running:
            await self.connect()

    def get_stats(self) -> Dict:
        """통계 조회"""
        return {
            'state': self.state.value,
            'url': self.config.url,
            'connected_at': self.stats.connected_at,
            'last_message_at': self.stats.last_message_at,
            'message_count': self.stats.message_count,
            'bytes_received': self.stats.bytes_received,
            'reconnect_count': self.stats.reconnect_count,
            'error_count': self.stats.error_count
        }


class MultiStreamClient:
    """다중 스트림 클라이언트"""

    def __init__(self):
        """초기화"""
        self.clients: Dict[str, WebSocketClient] = {}
        self._callbacks: List[Callable[[str, Dict], None]] = []

    def add_stream(self, stream_id: str, config: WebSocketConfig):
        """
        스트림 추가

        Args:
            stream_id: 스트림 ID
            config: WebSocket 설정
        """
        client = WebSocketClient(config)

        # 메시지 핸들러 설정
        def on_message(data):
            for callback in self._callbacks:
                try:
                    callback(stream_id, data)
                except Exception:
                    pass

        client.on_message = on_message
        self.clients[stream_id] = client

    def add_callback(self, callback: Callable[[str, Dict], None]):
        """콜백 추가"""
        self._callbacks.append(callback)

    async def connect_all(self):
        """모든 스트림 연결"""
        tasks = [
            client.connect()
            for client in self.clients.values()
        ]
        await asyncio.gather(*tasks)

    async def disconnect_all(self):
        """모든 스트림 연결 해제"""
        tasks = [
            client.disconnect()
            for client in self.clients.values()
        ]
        await asyncio.gather(*tasks)

    def get_all_stats(self) -> Dict:
        """전체 통계"""
        return {
            stream_id: client.get_stats()
            for stream_id, client in self.clients.items()
        }


# 테스트
if __name__ == '__main__':
    async def main():
        print("=== WebSocket 클라이언트 테스트 ===\n")

        # 단일 클라이언트 테스트
        config = WebSocketConfig(
            url='wss://stream.binance.com:9443/ws/btcusdt@ticker',
            ping_interval=30.0,
            reconnect_delay=5.0
        )

        client = WebSocketClient(config)

        message_count = 0

        def on_message(data):
            nonlocal message_count
            message_count += 1
            if message_count <= 3:
                print(f"[메시지 {message_count}] {data.get('s')}: ${data.get('c')}")

        def on_connect():
            print("연결됨!")

        def on_disconnect():
            print("연결 해제됨!")

        client.on_message = on_message
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect

        print("연결 시도...")
        await client.connect()

        # 5초 동안 메시지 수신
        print("5초 동안 메시지 수신...")
        await asyncio.sleep(5)

        # 통계 출력
        stats = client.get_stats()
        print(f"\n통계:")
        print(f"  상태: {stats['state']}")
        print(f"  메시지 수: {stats['message_count']}")
        print(f"  수신 바이트: {stats['bytes_received']}")

        # 연결 해제
        await client.disconnect()

    asyncio.run(main())
