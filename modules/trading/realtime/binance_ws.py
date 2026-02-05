#!/usr/bin/env python3
"""
Binance WebSocket 클라이언트
암호화폐 실시간 데이터 스트리밍
"""

import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Callable

from .binance_types import (
    BINANCE_WS_BASE, BINANCE_WS_STREAM, BinanceStreamType, TickerData
)

logger = logging.getLogger(__name__)


class BinanceWebSocket:
    """Binance WebSocket 클라이언트"""

    def __init__(self, ping_interval: float = 30.0, reconnect_delay: float = 5.0):
        self.ping_interval = ping_interval
        self.reconnect_delay = reconnect_delay
        self._ws = None
        self._running = False
        self._subscriptions: Dict[str, BinanceStreamType] = {}
        self.on_ticker: Optional[Callable[[TickerData], None]] = None
        self.on_trade: Optional[Callable[[Dict], None]] = None
        self.on_kline: Optional[Callable[[Dict], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def subscribe(self, symbols: List[str], stream_type: BinanceStreamType):
        """스트림 구독"""
        for symbol in symbols:
            self._subscriptions[f"{symbol.lower()}@{stream_type.value}"] = stream_type

    def unsubscribe(self, symbols: List[str], stream_type: BinanceStreamType):
        """구독 해제"""
        for symbol in symbols:
            self._subscriptions.pop(f"{symbol.lower()}@{stream_type.value}", None)

    def _build_url(self) -> str:
        if not self._subscriptions:
            return BINANCE_WS_BASE
        return f"{BINANCE_WS_STREAM}?streams={'/'.join(self._subscriptions.keys())}"

    async def run(self, duration: Optional[float] = None):
        """WebSocket 연결 및 메시지 수신"""
        self._running = True
        try:
            import websockets
            await self._run_websockets(websockets, duration)
        except ImportError:
            await self._run_simulation(duration)

    async def _run_websockets(self, websockets, duration: Optional[float]):
        """실제 WebSocket 연결"""
        start = asyncio.get_event_loop().time()
        while self._running:
            try:
                async with websockets.connect(self._build_url()) as ws:
                    self._ws = ws
                    ping_task = asyncio.create_task(self._ping_loop())
                    try:
                        async for msg in ws:
                            if not self._running:
                                break
                            if duration and asyncio.get_event_loop().time() - start >= duration:
                                self._running = False
                                break
                            self._handle_message(msg)
                    finally:
                        ping_task.cancel()
            except Exception as e:
                if self.on_error:
                    self.on_error(e)
                if self._running:
                    await asyncio.sleep(self.reconnect_delay)

    async def _run_simulation(self, duration: Optional[float]):
        """시뮬레이션 모드"""
        start = asyncio.get_event_loop().time()
        while self._running:
            await asyncio.sleep(1)
            if duration and asyncio.get_event_loop().time() - start >= duration:
                break
            for key, st in self._subscriptions.items():
                if st == BinanceStreamType.TICKER and self.on_ticker:
                    self.on_ticker(TickerData(
                        symbol=key.split('@')[0].upper(), price=50000.0,
                        change_24h=100.0, change_pct_24h=0.2, volume_24h=12345.67,
                        high_24h=51000.0, low_24h=49000.0,
                        timestamp=int(datetime.now().timestamp() * 1000)
                    ))

    async def _ping_loop(self):
        while self._running:
            await asyncio.sleep(self.ping_interval)
            if self._ws:
                try:
                    await self._ws.ping()
                except Exception:
                    pass

    def _handle_message(self, message: str):
        try:
            data = json.loads(message)
            stream = data.get('stream', '')
            payload = data.get('data', data)

            if 'ticker' in stream or payload.get('e') == '24hrTicker':
                if self.on_ticker:
                    self.on_ticker(TickerData.from_ws(payload))
            elif 'trade' in stream or payload.get('e') == 'trade':
                if self.on_trade:
                    self.on_trade(payload)
            elif 'kline' in stream or payload.get('e') == 'kline':
                if self.on_kline:
                    self.on_kline(payload)
        except json.JSONDecodeError:
            pass

    async def close(self):
        self._running = False
        if self._ws:
            await self._ws.close()
            self._ws = None
