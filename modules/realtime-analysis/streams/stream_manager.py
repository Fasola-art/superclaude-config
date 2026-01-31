#!/usr/bin/env python3
"""
스트림 관리자
실시간 데이터 스트림 연결 및 관리

기능:
- 다중 WebSocket 연결 관리
- 자동 재연결
- 메시지 큐잉
- 데이터 정규화
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import threading


MODULE_DIR = Path(__file__).parent.parent
CONFIG_FILE = Path(__file__).parent / 'stream_config.json'


class StreamStatus(Enum):
    """스트림 상태"""
    IDLE = 'idle'               # 대기 중
    CONNECTING = 'connecting'   # 연결 중
    CONNECTED = 'connected'     # 연결됨
    RECONNECTING = 'reconnecting'  # 재연결 중
    DISCONNECTED = 'disconnected'  # 연결 해제
    ERROR = 'error'             # 오류


class StreamType(Enum):
    """스트림 타입"""
    WEBSOCKET = 'websocket'
    POLLING = 'polling'
    INTERNAL = 'internal'


@dataclass
class StreamConfig:
    """스트림 설정"""
    id: str
    name: str
    stream_type: StreamType
    provider: str
    url: Optional[str]
    symbols: List[str]
    data_types: List[str]
    enabled: bool
    priority: int
    subscribe_message: Optional[Dict] = None
    poll_interval: int = 60000
    reconnect_on_error: bool = True
    max_reconnects: int = 10
    description: str = ''


@dataclass
class StreamState:
    """스트림 상태"""
    config: StreamConfig
    status: StreamStatus = StreamStatus.IDLE
    connected_at: Optional[str] = None
    last_message_at: Optional[str] = None
    message_count: int = 0
    error_count: int = 0
    reconnect_count: int = 0
    last_error: Optional[str] = None


@dataclass
class DataMessage:
    """데이터 메시지"""
    stream_id: str
    timestamp: str
    data_type: str
    symbol: str
    data: Dict
    raw: Optional[str] = None


class MessageQueue:
    """메시지 큐"""

    def __init__(self, max_size: int = 1000):
        """초기화"""
        self.max_size = max_size
        self.queue: deque = deque(maxlen=max_size)
        self._lock = threading.Lock()

    def push(self, message: DataMessage):
        """메시지 추가"""
        with self._lock:
            self.queue.append(message)

    def pop(self) -> Optional[DataMessage]:
        """메시지 꺼내기"""
        with self._lock:
            if self.queue:
                return self.queue.popleft()
            return None

    def pop_all(self) -> List[DataMessage]:
        """모든 메시지 꺼내기"""
        with self._lock:
            messages = list(self.queue)
            self.queue.clear()
            return messages

    def peek(self, count: int = 10) -> List[DataMessage]:
        """메시지 미리보기"""
        with self._lock:
            return list(self.queue)[-count:]

    def size(self) -> int:
        """큐 크기"""
        return len(self.queue)

    def clear(self):
        """큐 비우기"""
        with self._lock:
            self.queue.clear()


class DataParser:
    """데이터 파서"""

    @staticmethod
    def parse_binance_ticker(data: Dict) -> Dict:
        """
        Binance 티커 데이터 파싱

        Args:
            data: 원시 데이터

        Returns:
            정규화된 데이터
        """
        return {
            'symbol': data.get('s', '').replace('USDT', '/USDT'),
            'price': float(data.get('c', 0)),
            'open': float(data.get('o', 0)),
            'high': float(data.get('h', 0)),
            'low': float(data.get('l', 0)),
            'volume': float(data.get('v', 0)),
            'quote_volume': float(data.get('q', 0)),
            'price_change': float(data.get('p', 0)),
            'price_change_percent': float(data.get('P', 0)),
            'trades': int(data.get('n', 0)),
            'event_time': data.get('E', 0)
        }

    @staticmethod
    def parse_coinbase_ticker(data: Dict) -> Dict:
        """
        Coinbase 티커 데이터 파싱

        Args:
            data: 원시 데이터

        Returns:
            정규화된 데이터
        """
        return {
            'symbol': data.get('product_id', '').replace('-', '/'),
            'price': float(data.get('price', 0)),
            'open': float(data.get('open_24h', 0)),
            'high': float(data.get('high_24h', 0)),
            'low': float(data.get('low_24h', 0)),
            'volume': float(data.get('volume_24h', 0)),
            'last_size': float(data.get('last_size', 0)),
            'trade_id': data.get('trade_id'),
            'side': data.get('side'),
            'time': data.get('time')
        }

    @staticmethod
    def parse(provider: str, data: Dict) -> Dict:
        """
        범용 파서

        Args:
            provider: 제공자 이름
            data: 원시 데이터

        Returns:
            정규화된 데이터
        """
        if provider == 'binance':
            return DataParser.parse_binance_ticker(data)
        elif provider == 'coinbase':
            return DataParser.parse_coinbase_ticker(data)
        else:
            return data


class StreamManager:
    """스트림 관리자"""

    def __init__(self):
        """초기화"""
        self.streams: Dict[str, StreamState] = {}
        self.message_queue = MessageQueue()
        self.callbacks: List[Callable[[DataMessage], None]] = []
        self.global_settings: Dict = {}
        self._load_config()

    def _load_config(self):
        """설정 로드"""
        if not CONFIG_FILE.exists():
            return

        try:
            data = json.loads(CONFIG_FILE.read_text())
            self.global_settings = data.get('globalSettings', {})

            for stream_data in data.get('streams', []):
                config = StreamConfig(
                    id=stream_data['id'],
                    name=stream_data['name'],
                    stream_type=StreamType(stream_data['type']),
                    provider=stream_data['provider'],
                    url=stream_data.get('url'),
                    symbols=stream_data.get('symbols', []),
                    data_types=stream_data.get('dataTypes', []),
                    enabled=stream_data.get('enabled', True),
                    priority=stream_data.get('priority', 5),
                    subscribe_message=stream_data.get('subscribeMessage'),
                    poll_interval=stream_data.get('pollInterval', 60000),
                    reconnect_on_error=stream_data.get('reconnectOnError', True),
                    max_reconnects=stream_data.get('maxReconnects', 10),
                    description=stream_data.get('description', '')
                )
                self.streams[config.id] = StreamState(config=config)

        except Exception as e:
            print(f"설정 로드 오류: {e}")

    def get_enabled_streams(self) -> List[StreamState]:
        """활성화된 스트림 목록"""
        return sorted(
            [s for s in self.streams.values() if s.config.enabled],
            key=lambda x: x.config.priority,
            reverse=True
        )

    def add_callback(self, callback: Callable[[DataMessage], None]):
        """메시지 콜백 추가"""
        self.callbacks.append(callback)

    def remove_callback(self, callback: Callable[[DataMessage], None]):
        """메시지 콜백 제거"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def _dispatch_message(self, message: DataMessage):
        """메시지 전달"""
        # 큐에 추가
        self.message_queue.push(message)

        # 콜백 실행
        for callback in self.callbacks:
            try:
                callback(message)
            except Exception:
                pass

    def process_raw_message(self, stream_id: str, raw_data: str) -> Optional[DataMessage]:
        """
        원시 메시지 처리

        Args:
            stream_id: 스트림 ID
            raw_data: 원시 데이터 (JSON 문자열)

        Returns:
            처리된 메시지 또는 None
        """
        if stream_id not in self.streams:
            return None

        stream = self.streams[stream_id]
        stream.last_message_at = datetime.now().isoformat()
        stream.message_count += 1

        try:
            data = json.loads(raw_data)

            # 파싱
            parsed = DataParser.parse(stream.config.provider, data)

            message = DataMessage(
                stream_id=stream_id,
                timestamp=datetime.now().isoformat(),
                data_type=stream.config.data_types[0] if stream.config.data_types else 'unknown',
                symbol=parsed.get('symbol', stream.config.symbols[0] if stream.config.symbols else ''),
                data=parsed,
                raw=raw_data
            )

            self._dispatch_message(message)
            return message

        except Exception as e:
            stream.error_count += 1
            stream.last_error = str(e)
            return None

    def update_stream_status(self, stream_id: str, status: StreamStatus):
        """스트림 상태 업데이트"""
        if stream_id in self.streams:
            stream = self.streams[stream_id]
            stream.status = status

            if status == StreamStatus.CONNECTED:
                stream.connected_at = datetime.now().isoformat()
            elif status == StreamStatus.RECONNECTING:
                stream.reconnect_count += 1

    def get_stream_status(self, stream_id: str) -> Optional[Dict]:
        """스트림 상태 조회"""
        if stream_id not in self.streams:
            return None

        stream = self.streams[stream_id]
        return {
            'id': stream.config.id,
            'name': stream.config.name,
            'status': stream.status.value,
            'type': stream.config.stream_type.value,
            'provider': stream.config.provider,
            'symbols': stream.config.symbols,
            'connected_at': stream.connected_at,
            'last_message_at': stream.last_message_at,
            'message_count': stream.message_count,
            'error_count': stream.error_count,
            'reconnect_count': stream.reconnect_count,
            'last_error': stream.last_error
        }

    def get_all_status(self) -> Dict:
        """전체 상태 조회"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_streams': len(self.streams),
            'enabled_streams': sum(1 for s in self.streams.values() if s.config.enabled),
            'connected_streams': sum(
                1 for s in self.streams.values()
                if s.status == StreamStatus.CONNECTED
            ),
            'queue_size': self.message_queue.size(),
            'streams': [
                self.get_stream_status(sid)
                for sid in self.streams
            ]
        }

    def simulate_message(self, stream_id: str, data: Dict) -> DataMessage:
        """
        메시지 시뮬레이션 (테스트용)

        Args:
            stream_id: 스트림 ID
            data: 시뮬레이션 데이터

        Returns:
            생성된 메시지
        """
        stream = self.streams.get(stream_id)

        message = DataMessage(
            stream_id=stream_id,
            timestamp=datetime.now().isoformat(),
            data_type='price',
            symbol=data.get('symbol', 'TEST/USD'),
            data=data
        )

        self._dispatch_message(message)

        if stream:
            stream.message_count += 1
            stream.last_message_at = datetime.now().isoformat()

        return message


# 테스트
if __name__ == '__main__':
    manager = StreamManager()

    print("=== 스트림 관리자 테스트 ===\n")

    # 상태 확인
    status = manager.get_all_status()
    print(f"총 스트림: {status['total_streams']}개")
    print(f"활성 스트림: {status['enabled_streams']}개")
    print(f"연결 스트림: {status['connected_streams']}개\n")

    # 활성 스트림 목록
    print("활성 스트림:")
    for stream in manager.get_enabled_streams():
        config = stream.config
        print(f"  - {config.name} ({config.stream_type.value}, P{config.priority})")

    # 콜백 테스트
    def on_message(msg: DataMessage):
        print(f"\n[콜백] {msg.symbol}: {msg.data}")

    manager.add_callback(on_message)

    # 시뮬레이션
    print("\n메시지 시뮬레이션...")
    manager.simulate_message('binance_btc', {
        'symbol': 'BTC/USDT',
        'price': 50000.00,
        'volume': 12345.67
    })

    print(f"\n큐 크기: {manager.message_queue.size()}")

    # 큐에서 메시지 확인
    messages = manager.message_queue.pop_all()
    print(f"큐에서 꺼낸 메시지: {len(messages)}개")
