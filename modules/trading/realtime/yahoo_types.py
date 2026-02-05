#!/usr/bin/env python3
"""
Yahoo Finance 데이터 타입 정의
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Yahoo Finance API 엔드포인트
YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"


@dataclass
class Quote:
    """시세 정보"""
    symbol: str
    price: float
    change: float
    change_pct: float
    volume: int
    market_cap: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return asdict(self)

    @classmethod
    def from_response(cls, data: Dict[str, Any]) -> 'Quote':
        """응답 데이터에서 생성"""
        return cls(
            symbol=data.get('symbol', ''),
            price=data.get('regularMarketPrice', 0.0),
            change=data.get('regularMarketChange', 0.0),
            change_pct=data.get('regularMarketChangePercent', 0.0),
            volume=data.get('regularMarketVolume', 0),
            market_cap=data.get('marketCap'),
            bid=data.get('bid'),
            ask=data.get('ask'),
            high_52w=data.get('fiftyTwoWeekHigh'),
            low_52w=data.get('fiftyTwoWeekLow'),
            updated_at=datetime.now().isoformat()
        )
