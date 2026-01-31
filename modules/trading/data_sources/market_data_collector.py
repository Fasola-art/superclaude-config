#!/usr/bin/env python3
"""
실시간 시장 데이터 수집기.

- VIX, Gold, EUR/USD, USD/JPY, NASDAQ, S&P500, Bitcoin
- SOFR (NY Fed)
- MOVE Index (추정치)

⚠️ 정확성 원칙: 실제 데이터만 수집, 추정/가공 데이터는 명확히 표시
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# 로거 설정
logger = logging.getLogger(__name__)

# 설정 - config에서 가져오거나 기본값 사용
try:
    from config import MARKET_DATA_DIR as DATA_DIR
except ImportError:
    DATA_DIR = Path.home() / ".claude" / "modules" / "trading" / "data_sources" / "market_data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class MarketQuote:
    """시장 시세 데이터."""

    symbol: str
    name: str
    price: float
    change: float | None = None
    change_pct: float | None = None
    timestamp: str = ""
    source: str = ""  # 데이터 출처 명시


@dataclass
class SOFRData:
    """SOFR 데이터."""

    date: str
    rate: float
    average_30d: float | None = None
    average_90d: float | None = None
    source: str = "NY Fed"


@dataclass
class MarketDataSnapshot:
    """시장 데이터 스냅샷."""

    timestamp: str
    quotes: list[MarketQuote]
    sofr: SOFRData | None = None
    move_index: float | None = None
    move_source: str = ""
    notes: list[str] | None = None  # 데이터 관련 주의사항

    def __post_init__(self) -> None:
        """초기화 후 처리."""
        if self.notes is None:
            self.notes = []


class MarketDataCollector:
    """시장 데이터 수집기."""

    def __init__(self) -> None:
        """수집기 초기화."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        # 심볼 매핑
        self.symbols: dict[str, dict[str, str]] = {
            'VIX': {'name': 'VIX (공포지수)', 'yahoo': '^VIX'},
            'MOVE': {'name': 'MOVE Index (채권 변동성)', 'yahoo': '^MOVE'},
            'GOLD': {'name': 'Gold (금)', 'yahoo': 'GC=F'},
            'EUR_USD': {'name': 'EUR/USD (유로/달러)', 'yahoo': 'EURUSD=X'},
            'USD_JPY': {'name': 'USD/JPY (달러/엔)', 'yahoo': 'USDJPY=X'},
            'NASDAQ': {'name': 'NASDAQ (NQ)', 'yahoo': 'NQ=F'},
            'SP500': {'name': 'S&P 500 (ES)', 'yahoo': 'ES=F'},
            'BITCOIN': {'name': 'Bitcoin (BTC/USD)', 'coingecko': 'bitcoin'},
        }

    def _fetch_url(self, url: str, timeout: int = 30) -> str | None:
        """URL에서 데이터 가져오기."""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            logger.error(f"URL 요청 실패: {url[:50]}... - {e}")
            return None

    def get_yahoo_quote(self, symbol: str) -> MarketQuote | None:
        """Yahoo Finance에서 시세 가져오기."""
        try:
            # Yahoo Finance API (비공식)
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"

            data = self._fetch_url(url)
            if not data:
                return None

            result = json.loads(data)
            chart = result.get('chart', {}).get('result', [{}])[0]
            meta = chart.get('meta', {})

            price = meta.get('regularMarketPrice', 0)
            # chartPreviousClose가 실제 전일 종가 (previousClose는 종종 현재가와 동일)
            prev_close = meta.get('chartPreviousClose', meta.get('previousClose', price))
            change = price - prev_close if prev_close else 0
            change_pct = (change / prev_close * 100) if prev_close else 0

            return MarketQuote(
                symbol=symbol,
                name=self.symbols.get(symbol, {}).get('name', symbol),
                price=round(price, 2),
                change=round(change, 2),
                change_pct=round(change_pct, 2),
                timestamp=datetime.now().isoformat(),
                source="Yahoo Finance"
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Yahoo 시세 파싱 실패: {symbol} - {e}")
            return None
        except Exception as e:
            logger.exception(f"Yahoo 시세 조회 실패: {symbol}")
            return None

    def get_bitcoin_price(self) -> MarketQuote | None:
        """CoinGecko에서 비트코인 가격 가져오기."""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"

            data = self._fetch_url(url)
            if not data:
                return None

            result = json.loads(data)
            btc = result.get('bitcoin', {})

            price = btc.get('usd', 0)
            change_pct = btc.get('usd_24h_change', 0)

            return MarketQuote(
                symbol='BTC',
                name='Bitcoin (BTC/USD)',
                price=round(price, 2),
                change=None,  # CoinGecko는 절대 변화량 미제공
                change_pct=round(change_pct, 2),
                timestamp=datetime.now().isoformat(),
                source="CoinGecko"
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"비트코인 가격 파싱 실패: {e}")
            return None
        except Exception as e:
            logger.exception("비트코인 가격 조회 실패")
            return None

    def get_sofr_data(self) -> SOFRData | None:
        """
        SOFR 데이터 가져오기 (NY Fed).

        ⚠️ NY Fed API는 약간의 지연이 있을 수 있음 (1-2 영업일)
        """
        try:
            # NY Fed SOFR API
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

            url = f"https://markets.newyorkfed.org/api/rates/secured/sofr/last/7.json"

            data = self._fetch_url(url)
            if not data:
                return None

            result = json.loads(data)
            rates = result.get('refRates', [])

            if rates:
                latest = rates[0]
                return SOFRData(
                    date=latest.get('effectiveDate', ''),
                    rate=float(latest.get('percentRate', 0)),
                    average_30d=float(latest.get('average30Day', 0)) if latest.get('average30Day') else None,
                    average_90d=float(latest.get('average90Day', 0)) if latest.get('average90Day') else None,
                    source="NY Fed (공식)"
                )
            return None
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"SOFR 데이터 파싱 실패: {e}")
            return None
        except Exception as e:
            logger.exception("SOFR 데이터 조회 실패")
            return None

    def get_sofr_weekly_trend(self) -> list[dict[str, Any]]:
        """SOFR 일주일 추이."""
        try:
            url = "https://markets.newyorkfed.org/api/rates/secured/sofr/last/7.json"

            data = self._fetch_url(url)
            if not data:
                return []

            result = json.loads(data)
            rates = result.get('refRates', [])

            trend = []
            for rate in reversed(rates):  # 오래된 것부터
                trend.append({
                    'date': rate.get('effectiveDate', ''),
                    'rate': float(rate.get('percentRate', 0)),
                    'source': 'NY Fed'
                })

            return trend
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"SOFR 추이 파싱 실패: {e}")
            return []
        except Exception as e:
            logger.exception("SOFR 추이 조회 실패")
            return []

    def get_move_index(self) -> MarketQuote | None:
        """
        MOVE Index (채권 변동성 지수) 가져오기.

        ICE BofAML MOVE Index - 채권 시장의 VIX
        출처: Yahoo Finance (^MOVE)
        원본: ICE/NYSE
        """
        return self.get_yahoo_quote('^MOVE')

    def get_move_weekly_trend(self) -> list[dict[str, Any]]:
        """MOVE Index 일주일 추이."""
        try:
            url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EMOVE?interval=1d&range=7d"

            data = self._fetch_url(url)
            if not data:
                return []

            result = json.loads(data)
            chart = result.get('chart', {}).get('result', [{}])[0]
            timestamps = chart.get('timestamp', [])
            quotes_data = chart.get('indicators', {}).get('quote', [{}])[0]
            closes = quotes_data.get('close', [])

            trend: list[dict[str, Any]] = []
            for ts, close in zip(timestamps, closes):
                if close:
                    trend.append({
                        'date': datetime.fromtimestamp(ts).strftime('%Y-%m-%d'),
                        'value': round(close, 2),
                        'source': 'Yahoo Finance (ICE BofAML)'
                    })

            return trend
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"MOVE 추이 파싱 실패: {e}")
            return []
        except Exception as e:
            logger.exception("MOVE 추이 조회 실패")
            return []

    def get_all_quotes(self) -> list[MarketQuote]:
        """모든 시세 수집."""
        quotes = []

        # Yahoo Finance 시세
        yahoo_symbols = [
            ('^VIX', 'VIX', 'VIX (공포지수)'),
            ('^MOVE', 'MOVE', 'MOVE Index (채권 변동성)'),
            ('GC=F', 'GOLD', 'Gold (금)'),
            ('EURUSD=X', 'EUR_USD', 'EUR/USD (유로/달러)'),
            ('USDJPY=X', 'USD_JPY', 'USD/JPY (달러/엔)'),
            ('NQ=F', 'NASDAQ', 'NASDAQ (NQ)'),
            ('ES=F', 'SP500', 'S&P 500 (ES)'),
        ]

        for yahoo_sym, key, name in yahoo_symbols:
            quote = self.get_yahoo_quote(yahoo_sym)
            if quote:
                quote.symbol = key
                quote.name = name
                quotes.append(quote)
            else:
                # 실패시 플레이스홀더 (데이터 없음 명시)
                quotes.append(MarketQuote(
                    symbol=key,
                    name=name,
                    price=0,
                    timestamp=datetime.now().isoformat(),
                    source="수집 실패 - 수동 입력 필요"
                ))

        # 비트코인
        btc = self.get_bitcoin_price()
        if btc:
            quotes.append(btc)
        else:
            quotes.append(MarketQuote(
                symbol='BTC',
                name='Bitcoin (BTC/USD)',
                price=0,
                timestamp=datetime.now().isoformat(),
                source="수집 실패 - 수동 입력 필요"
            ))

        return quotes

    def collect_snapshot(self) -> MarketDataSnapshot:
        """전체 시장 데이터 스냅샷."""
        logger.info("시장 데이터 스냅샷 생성 중...")

        quotes = self.get_all_quotes()
        logger.info(f"시세: {len([q for q in quotes if q.price > 0])}/{len(quotes)} 성공")

        sofr = self.get_sofr_data()
        logger.info(f"SOFR: {'성공' if sofr else '실패'}")

        # MOVE Index 추이
        move_trend = self.get_move_weekly_trend()
        move_current: float | None = None
        for q in quotes:
            if q.symbol == 'MOVE' and q.price > 0:
                move_current = q.price
                break

        logger.info(f"MOVE Index: {'성공' if move_current else '실패'}")

        notes = []

        # 선물 가격 주의사항
        notes.append("📌 선물 가격(ES, NQ, GC)은 Yahoo Finance 기준. 실시간 CME 데이터와 차이 있을 수 있음.")

        snapshot = MarketDataSnapshot(
            timestamp=datetime.now().isoformat(),
            quotes=quotes,
            sofr=sofr,
            move_index=move_current,
            move_source="Yahoo Finance (ICE BofAML MOVE Index)",
            notes=notes
        )

        return snapshot

    def format_quote_table(self, quotes: list[MarketQuote]) -> str:
        """시세표 마크다운 포맷."""
        lines = [
            "## 1️⃣ 시세표",
            "",
            "| # | 항목 | 가격 | 변동 | 출처 |",
            "|---|------|------|------|------|"
        ]

        for i, q in enumerate(quotes, 1):
            change_str = f"{q.change_pct:+.2f}%" if q.change_pct else "-"
            price_str = f"{q.price:,.2f}" if q.price > 0 else "⚠️ 수동 입력"
            lines.append(f"| {i} | {q.name} | {price_str} | {change_str} | {q.source} |")

        return "\n".join(lines)

    def format_sofr_section(self, sofr: SOFRData, trend: list[dict[str, Any]]) -> str:
        """SOFR 섹션 마크다운 포맷."""
        lines = [
            "## 2️⃣ SOFR / MOVE Index 일주일간 동향",
            "",
            "### SOFR (Secured Overnight Financing Rate)",
            f"- **최신 SOFR**: {sofr.rate:.2f}% ({sofr.date})",
        ]

        if sofr.average_30d:
            lines.append(f"- **30일 평균**: {sofr.average_30d:.2f}%")
        if sofr.average_90d:
            lines.append(f"- **90일 평균**: {sofr.average_90d:.2f}%")

        lines.append(f"- *출처: {sofr.source}*")
        lines.append("")

        # 일주일 추이
        if trend:
            lines.append("**일주일 추이:**")
            trend_str = ", ".join([f"{t['date'][-5:]}: {t['rate']:.2f}%" for t in trend[-5:]])
            lines.append(f"- {trend_str}")

        lines.extend([
            "",
            "### MOVE Index",
            "- **현재값**: `[수동 입력 필요]`",
            "- **일주일 변화**: `[수동 입력 필요]`",
            "- *출처: Bloomberg/ICE (유료 데이터)*",
            "",
            "> ⚠️ MOVE Index는 자동 수집이 불가능합니다. TradingView 또는 Bloomberg에서 확인 후 입력해주세요.",
        ])

        return "\n".join(lines)

    def save_snapshot(self, snapshot: MarketDataSnapshot) -> str:
        """스냅샷 저장."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = DATA_DIR / f"snapshot_{timestamp}.json"

        # dataclass를 dict로 변환
        data: dict[str, Any] = {
            'timestamp': snapshot.timestamp,
            'quotes': [asdict(q) for q in snapshot.quotes],
            'sofr': asdict(snapshot.sofr) if snapshot.sofr else None,
            'move_index': snapshot.move_index,
            'move_source': snapshot.move_source,
            'notes': snapshot.notes
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"저장 완료: {filename}")
        return str(filename)


# === 비동기 수집기 ===

class AsyncMarketDataCollector:
    """비동기 시장 데이터 수집기 (httpx 사용)."""

    def __init__(self) -> None:
        """비동기 수집기 초기화."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.symbols: dict[str, dict[str, str]] = {
            'VIX': {'name': 'VIX (공포지수)', 'yahoo': '^VIX'},
            'MOVE': {'name': 'MOVE Index (채권 변동성)', 'yahoo': '^MOVE'},
            'GOLD': {'name': 'Gold (금)', 'yahoo': 'GC=F'},
            'EUR_USD': {'name': 'EUR/USD (유로/달러)', 'yahoo': 'EURUSD=X'},
            'USD_JPY': {'name': 'USD/JPY (달러/엔)', 'yahoo': 'USDJPY=X'},
            'NASDAQ': {'name': 'NASDAQ (NQ)', 'yahoo': 'NQ=F'},
            'SP500': {'name': 'S&P 500 (ES)', 'yahoo': 'ES=F'},
            'BITCOIN': {'name': 'Bitcoin (BTC/USD)', 'coingecko': 'bitcoin'},
        }

    async def _fetch_url(self, client: Any, url: str) -> str | None:
        """비동기 URL 요청."""
        try:
            response = await client.get(url, headers=self.headers, timeout=30.0)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"URL 요청 실패: {url[:50]}... - {e}")
            return None

    async def get_yahoo_quote_async(self, client: Any, symbol: str) -> MarketQuote | None:
        """비동기 Yahoo Finance 시세 조회."""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
            data = await self._fetch_url(client, url)
            if not data:
                return None

            result = json.loads(data)
            chart = result.get('chart', {}).get('result', [{}])[0]
            meta = chart.get('meta', {})

            price = meta.get('regularMarketPrice', 0)
            # chartPreviousClose가 실제 전일 종가 (previousClose는 종종 현재가와 동일)
            prev_close = meta.get('chartPreviousClose', meta.get('previousClose', price))
            change = price - prev_close if prev_close else 0
            change_pct = (change / prev_close * 100) if prev_close else 0

            return MarketQuote(
                symbol=symbol,
                name=self.symbols.get(symbol, {}).get('name', symbol),
                price=round(price, 2),
                change=round(change, 2),
                change_pct=round(change_pct, 2),
                timestamp=datetime.now().isoformat(),
                source="Yahoo Finance"
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Yahoo 시세 파싱 실패: {symbol} - {e}")
            return None
        except Exception as e:
            logger.exception(f"Yahoo 시세 조회 실패: {symbol}")
            return None

    async def get_bitcoin_price_async(self, client: Any) -> MarketQuote | None:
        """비동기 비트코인 가격 조회."""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
            data = await self._fetch_url(client, url)
            if not data:
                return None

            result = json.loads(data)
            btc = result.get('bitcoin', {})

            price = btc.get('usd', 0)
            change_pct = btc.get('usd_24h_change', 0)

            return MarketQuote(
                symbol='BTC',
                name='Bitcoin (BTC/USD)',
                price=round(price, 2),
                change=None,
                change_pct=round(change_pct, 2),
                timestamp=datetime.now().isoformat(),
                source="CoinGecko"
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"비트코인 가격 파싱 실패: {e}")
            return None
        except Exception as e:
            logger.exception("비트코인 가격 조회 실패")
            return None

    async def get_sofr_data_async(self, client: Any) -> SOFRData | None:
        """비동기 SOFR 데이터 조회."""
        try:
            url = "https://markets.newyorkfed.org/api/rates/secured/sofr/last/7.json"
            data = await self._fetch_url(client, url)
            if not data:
                return None

            result = json.loads(data)
            rates = result.get('refRates', [])

            if rates:
                latest = rates[0]
                return SOFRData(
                    date=latest.get('effectiveDate', ''),
                    rate=float(latest.get('percentRate', 0)),
                    average_30d=float(latest.get('average30Day', 0)) if latest.get('average30Day') else None,
                    average_90d=float(latest.get('average90Day', 0)) if latest.get('average90Day') else None,
                    source="NY Fed (공식)"
                )
            return None
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"SOFR 데이터 파싱 실패: {e}")
            return None
        except Exception as e:
            logger.exception("SOFR 데이터 조회 실패")
            return None

    async def get_all_quotes_async(self) -> list[MarketQuote]:
        """모든 시세 병렬 수집 (약 8초 → 1-2초)."""
        try:
            import httpx
        except ImportError:
            logger.warning("httpx 미설치. 동기 수집기 사용 권장: pip install httpx")
            # 동기 수집기로 폴백
            sync_collector = MarketDataCollector()
            return sync_collector.get_all_quotes()

        yahoo_symbols = [
            ('^VIX', 'VIX', 'VIX (공포지수)'),
            ('^MOVE', 'MOVE', 'MOVE Index (채권 변동성)'),
            ('GC=F', 'GOLD', 'Gold (금)'),
            ('EURUSD=X', 'EUR_USD', 'EUR/USD (유로/달러)'),
            ('USDJPY=X', 'USD_JPY', 'USD/JPY (달러/엔)'),
            ('NQ=F', 'NASDAQ', 'NASDAQ (NQ)'),
            ('ES=F', 'SP500', 'S&P 500 (ES)'),
        ]

        quotes: list[MarketQuote] = []

        async with httpx.AsyncClient() as client:
            import asyncio

            # 모든 Yahoo 시세 병렬 요청
            yahoo_tasks = [
                self.get_yahoo_quote_async(client, yahoo_sym)
                for yahoo_sym, _, _ in yahoo_symbols
            ]

            # 비트코인도 병렬로
            btc_task = self.get_bitcoin_price_async(client)

            # 모든 태스크 동시 실행
            results = await asyncio.gather(*yahoo_tasks, btc_task, return_exceptions=True)

            # Yahoo 결과 처리
            for i, (yahoo_sym, key, name) in enumerate(yahoo_symbols):
                result = results[i]
                if isinstance(result, MarketQuote) and result:
                    result.symbol = key
                    result.name = name
                    quotes.append(result)
                else:
                    quotes.append(MarketQuote(
                        symbol=key,
                        name=name,
                        price=0,
                        timestamp=datetime.now().isoformat(),
                        source="수집 실패 - 수동 입력 필요"
                    ))

            # 비트코인 결과 처리
            btc_result = results[-1]
            if isinstance(btc_result, MarketQuote) and btc_result:
                quotes.append(btc_result)
            else:
                quotes.append(MarketQuote(
                    symbol='BTC',
                    name='Bitcoin (BTC/USD)',
                    price=0,
                    timestamp=datetime.now().isoformat(),
                    source="수집 실패 - 수동 입력 필요"
                ))

        return quotes

    async def collect_snapshot_async(self) -> MarketDataSnapshot:
        """비동기 전체 시장 데이터 스냅샷."""
        try:
            import httpx
        except ImportError:
            logger.warning("httpx 미설치. 동기 수집기로 폴백")
            sync_collector = MarketDataCollector()
            return sync_collector.collect_snapshot()

        import asyncio

        logger.info("비동기 시장 데이터 스냅샷 생성 중...")

        async with httpx.AsyncClient() as client:
            # 모든 데이터 병렬 수집
            quotes_task = self.get_all_quotes_async()
            sofr_task = self.get_sofr_data_async(client)

            quotes, sofr = await asyncio.gather(quotes_task, sofr_task)

        logger.info(f"시세: {len([q for q in quotes if q.price > 0])}/{len(quotes)} 성공")
        logger.info(f"SOFR: {'성공' if sofr else '실패'}")

        # MOVE Index 추출
        move_current: float | None = None
        for q in quotes:
            if q.symbol == 'MOVE' and q.price > 0:
                move_current = q.price
                break

        logger.info(f"MOVE Index: {'성공' if move_current else '실패'}")

        notes: list[str] = [
            "📌 선물 가격(ES, NQ, GC)은 Yahoo Finance 기준. 실시간 CME 데이터와 차이 있을 수 있음."
        ]

        return MarketDataSnapshot(
            timestamp=datetime.now().isoformat(),
            quotes=quotes,
            sofr=sofr,
            move_index=move_current,
            move_source="Yahoo Finance (ICE BofAML MOVE Index)",
            notes=notes
        )


def collect_market_data() -> MarketDataSnapshot:
    """시장 데이터 수집 (외부 호출용 - 동기)."""
    collector = MarketDataCollector()
    snapshot = collector.collect_snapshot()
    collector.save_snapshot(snapshot)
    return snapshot


async def collect_market_data_async() -> MarketDataSnapshot:
    """시장 데이터 수집 (외부 호출용 - 비동기)."""
    collector = AsyncMarketDataCollector()
    snapshot = await collector.collect_snapshot_async()

    # 저장은 동기 수집기 사용
    sync_collector = MarketDataCollector()
    sync_collector.save_snapshot(snapshot)
    return snapshot


# CLI 실행
if __name__ == "__main__":
    collector = MarketDataCollector()

    print("=== 시장 데이터 수집 ===\n")

    snapshot = collector.collect_snapshot()

    print("\n" + "="*50)
    print(collector.format_quote_table(snapshot.quotes))

    if snapshot.sofr:
        trend = collector.get_sofr_weekly_trend()
        print("\n" + collector.format_sofr_section(snapshot.sofr, trend))

    print("\n=== 주의사항 ===")
    for note in snapshot.notes:
        print(f"  {note}")

    collector.save_snapshot(snapshot)
