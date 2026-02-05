#!/usr/bin/env python3
"""
Binance 데이터 타입 정의
WebSocket 스트림용 타입 및 데이터 클래스
"""

from typing import Dict
from dataclasses import dataclass
from enum import Enum

# Binance WebSocket 엔드포인트
BINANCE_WS_BASE = "wss://stream.binance.com:9443/ws"
BINANCE_WS_STREAM = "wss://stream.binance.com:9443/stream"


class BinanceStreamType(Enum):
    """스트림 타입"""
    TICKER = 'ticker'           # 24시간 티커
    MINI_TICKER = 'miniTicker'  # 미니 티커
    TRADE = 'trade'             # 체결 데이터
    KLINE = 'kline'             # 캔들스틱
    DEPTH = 'depth'             # 호가창


@dataclass
class TickerData:
    """티커 데이터"""
    symbol: str
    price: float
    change_24h: float
    change_pct_24h: float
    volume_24h: float
    high_24h: float
    low_24h: float
    timestamp: int

    @classmethod
    def from_ws(cls, data: Dict) -> 'TickerData':
        """WebSocket 메시지에서 생성"""
        return cls(
            symbol=data.get('s', ''),
            price=float(data.get('c', 0)),
            change_24h=float(data.get('p', 0)),
            change_pct_24h=float(data.get('P', 0)),
            volume_24h=float(data.get('v', 0)),
            high_24h=float(data.get('h', 0)),
            low_24h=float(data.get('l', 0)),
            timestamp=data.get('E', 0)
        )


@dataclass
class TradeData:
    """체결 데이터"""
    symbol: str
    price: float
    quantity: float
    buyer_is_maker: bool
    timestamp: int

    @classmethod
    def from_ws(cls, data: Dict) -> 'TradeData':
        """WebSocket 메시지에서 생성"""
        return cls(
            symbol=data.get('s', ''),
            price=float(data.get('p', 0)),
            quantity=float(data.get('q', 0)),
            buyer_is_maker=data.get('m', False),
            timestamp=data.get('T', 0)
        )
