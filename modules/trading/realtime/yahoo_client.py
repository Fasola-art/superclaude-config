#!/usr/bin/env python3
"""
Yahoo Finance 클라이언트 (yfinance 기반)
실시간 주식 가격 데이터 조회
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Yahoo Finance API 엔드포인트
YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


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


class YahooFinanceClient:
    """
    Yahoo Finance 클라이언트

    사용법:
        client = YahooFinanceClient()
        quote = client.get_quote('AAPL')
        print(f"Apple: ${quote.price}")
    """

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        if not HAS_YFINANCE:
            logger.warning("yfinance 미설치: pip install yfinance")

    def get_quote(self, symbol: str) -> Optional[Quote]:
        """단일 심볼 시세 조회"""
        quotes = self.get_quotes([symbol])
        return quotes.get(symbol)

    def get_quotes(self, symbols: List[str]) -> Dict[str, Quote]:
        """다중 심볼 시세 조회"""
        if not HAS_YFINANCE or not symbols:
            return {}

        results = {}
        try:
            tickers = yf.Tickers(' '.join(symbols))
            for symbol in symbols:
                try:
                    info = tickers.tickers[symbol].fast_info
                    results[symbol] = Quote(
                        symbol=symbol,
                        price=info.last_price or 0.0,
                        change=info.last_price - info.previous_close if info.previous_close else 0.0,
                        change_pct=((info.last_price / info.previous_close) - 1) * 100 if info.previous_close else 0.0,
                        volume=int(info.last_volume or 0),
                        market_cap=info.market_cap,
                        high_52w=info.year_high,
                        low_52w=info.year_low,
                    )
                except Exception as e:
                    logger.warning(f"{symbol} 조회 실패: {e}")
        except Exception as e:
            logger.error(f"yfinance 오류: {e}")

        return results

    def get_price(self, symbol: str) -> Optional[float]:
        """단일 심볼 가격만 조회"""
        quote = self.get_quote(symbol)
        return quote.price if quote else None


# 편의 함수
_client: Optional[YahooFinanceClient] = None


def _get_client() -> YahooFinanceClient:
    global _client
    if _client is None:
        _client = YahooFinanceClient()
    return _client


def get_price(symbol: str) -> Optional[float]:
    """심볼 가격 조회"""
    return _get_client().get_price(symbol)


def get_quote(symbol: str) -> Optional[Quote]:
    """심볼 시세 조회"""
    return _get_client().get_quote(symbol)
