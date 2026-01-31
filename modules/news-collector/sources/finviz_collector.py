#!/usr/bin/env python3
"""
Finviz 데이터 수집기
- 주식 스크리너
- 뉴스 피드
- 실시간 가격 데이터
"""

import json
import re
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import urllib.request
import urllib.parse
from html.parser import HTMLParser

# 설정
FINVIZ_BASE_URL = "https://finviz.com"
ARCHIVE_DIR = Path.home() / ".claude" / "modules" / "news-collector" / "archive" / "finviz"


@dataclass
class FinvizNews:
    """Finviz 뉴스 데이터"""
    ticker: str
    headline: str
    source: str
    url: str
    timestamp: datetime
    sentiment: Optional[str] = None  # positive, negative, neutral


@dataclass
class FinvizQuote:
    """Finviz 가격 데이터"""
    ticker: str
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[str] = None
    pe_ratio: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    timestamp: datetime = None


@dataclass
class ScreenerResult:
    """스크리너 결과"""
    ticker: str
    company: str
    sector: str
    industry: str
    country: str
    market_cap: str
    pe: Optional[float]
    price: float
    change: float
    volume: int


class FinvizHTMLParser(HTMLParser):
    """Finviz HTML 파서"""

    def __init__(self):
        super().__init__()
        self.data = []
        self.current_tag = None
        self.current_attrs = {}

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)

    def handle_data(self, data):
        if data.strip():
            self.data.append({
                'tag': self.current_tag,
                'attrs': self.current_attrs,
                'text': data.strip()
            })


class FinvizCollector:
    """Finviz 데이터 수집기"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    def _fetch_url(self, url: str) -> str:
        """URL에서 HTML 가져오기"""
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"[에러] URL 요청 실패: {url} - {e}")
            return ""

    def get_news(self, ticker: str = None, limit: int = 50) -> List[FinvizNews]:
        """
        뉴스 수집

        Args:
            ticker: 특정 종목 (None이면 전체 뉴스)
            limit: 최대 뉴스 수
        """
        news_list = []

        if ticker:
            url = f"{FINVIZ_BASE_URL}/quote.ashx?t={ticker}"
        else:
            url = f"{FINVIZ_BASE_URL}/news.ashx"

        html = self._fetch_url(url)
        if not html:
            return news_list

        # 뉴스 테이블 파싱 (간단한 정규식 사용)
        # 실제로는 BeautifulSoup 사용 권장
        news_pattern = r'<a[^>]*class="tab-link-news"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
        matches = re.findall(news_pattern, html, re.IGNORECASE)

        for url, headline in matches[:limit]:
            news = FinvizNews(
                ticker=ticker or "MARKET",
                headline=headline.strip(),
                source="Finviz",
                url=url,
                timestamp=datetime.now(),
                sentiment=self._analyze_sentiment(headline)
            )
            news_list.append(news)

        return news_list

    def get_quote(self, ticker: str) -> Optional[FinvizQuote]:
        """
        실시간 가격 데이터

        Args:
            ticker: 종목 코드
        """
        url = f"{FINVIZ_BASE_URL}/quote.ashx?t={ticker}"
        html = self._fetch_url(url)

        if not html:
            return None

        try:
            # 가격 파싱
            price_match = re.search(r'<span[^>]*class="quote-price_value"[^>]*>([0-9.,]+)</span>', html)
            change_match = re.search(r'<span[^>]*class="quote-price_change[^"]*"[^>]*>([+-]?[0-9.,]+)[^<]*\(([+-]?[0-9.,]+)%\)', html)

            price = float(price_match.group(1).replace(',', '')) if price_match else 0.0
            change = float(change_match.group(1).replace(',', '')) if change_match else 0.0
            change_pct = float(change_match.group(2).replace(',', '')) if change_match else 0.0

            return FinvizQuote(
                ticker=ticker.upper(),
                price=price,
                change=change,
                change_percent=change_pct,
                volume=0,  # 추가 파싱 필요
                timestamp=datetime.now()
            )
        except Exception as e:
            print(f"[에러] 가격 파싱 실패: {ticker} - {e}")
            return None

    def run_screener(self, filters: Dict[str, str] = None) -> List[ScreenerResult]:
        """
        주식 스크리너 실행

        Args:
            filters: 스크리너 필터 (예: {'v': '111', 'f': 'cap_largeover'})

        기본 필터 옵션:
        - cap_largeover: 대형주 ($10B 이상)
        - cap_midover: 중형주 이상
        - ta_sma20_pa: 20일 이평선 위
        - ta_change_u: 상승 종목
        """
        results = []

        params = filters or {'v': '111'}  # 기본: Overview 뷰
        query = urllib.parse.urlencode(params)
        url = f"{FINVIZ_BASE_URL}/screener.ashx?{query}"

        html = self._fetch_url(url)
        if not html:
            return results

        # 테이블 데이터 파싱 (간단한 버전)
        # 실제로는 더 정교한 파싱 필요
        row_pattern = r'<tr[^>]*class="screener-link-primary"[^>]*>(.*?)</tr>'
        rows = re.findall(row_pattern, html, re.DOTALL)

        for row in rows[:100]:  # 최대 100개
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 10:
                try:
                    ticker = re.sub(r'<[^>]+>', '', cells[1]).strip()
                    company = re.sub(r'<[^>]+>', '', cells[2]).strip()

                    results.append(ScreenerResult(
                        ticker=ticker,
                        company=company,
                        sector=re.sub(r'<[^>]+>', '', cells[3]).strip(),
                        industry=re.sub(r'<[^>]+>', '', cells[4]).strip(),
                        country=re.sub(r'<[^>]+>', '', cells[5]).strip(),
                        market_cap=re.sub(r'<[^>]+>', '', cells[6]).strip(),
                        pe=self._parse_float(re.sub(r'<[^>]+>', '', cells[7])),
                        price=self._parse_float(re.sub(r'<[^>]+>', '', cells[8])),
                        change=self._parse_float(re.sub(r'<[^>]+>', '', cells[9])),
                        volume=self._parse_int(re.sub(r'<[^>]+>', '', cells[10]))
                    ))
                except Exception:
                    continue

        return results

    def get_heatmap_data(self, timeframe: str = '1d') -> Dict[str, Any]:
        """
        섹터별 히트맵 데이터

        Args:
            timeframe: 1d, 1w, 1m, 3m, 6m, 1y
        """
        # Finviz 히트맵 API는 없으므로 스크래핑 필요
        # 여기서는 섹터별 변동률 계산

        sectors = {
            'Technology': ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META'],
            'Healthcare': ['JNJ', 'UNH', 'PFE', 'MRK', 'ABBV'],
            'Financial': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
            'Consumer': ['AMZN', 'TSLA', 'HD', 'NKE', 'MCD'],
            'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG']
        }

        heatmap = {}
        for sector, tickers in sectors.items():
            changes = []
            for ticker in tickers[:3]:  # 상위 3개만
                quote = self.get_quote(ticker)
                if quote:
                    changes.append(quote.change_percent)

            if changes:
                heatmap[sector] = {
                    'avg_change': sum(changes) / len(changes),
                    'tickers': tickers
                }

        return heatmap

    def _analyze_sentiment(self, text: str) -> str:
        """간단한 감성 분석"""
        positive_words = ['surge', 'jump', 'gain', 'rise', 'up', 'high', 'beat', 'strong', 'bull']
        negative_words = ['drop', 'fall', 'decline', 'down', 'low', 'miss', 'weak', 'bear', 'crash']

        text_lower = text.lower()
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)

        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        return 'neutral'

    def _parse_float(self, value: str) -> Optional[float]:
        """문자열을 float로 변환"""
        try:
            clean = value.replace(',', '').replace('%', '').strip()
            return float(clean) if clean and clean != '-' else None
        except:
            return None

    def _parse_int(self, value: str) -> int:
        """문자열을 int로 변환"""
        try:
            clean = value.replace(',', '').strip()
            # K, M, B 처리
            if 'K' in clean.upper():
                return int(float(clean.upper().replace('K', '')) * 1000)
            elif 'M' in clean.upper():
                return int(float(clean.upper().replace('M', '')) * 1000000)
            elif 'B' in clean.upper():
                return int(float(clean.upper().replace('B', '')) * 1000000000)
            return int(float(clean)) if clean else 0
        except:
            return 0

    def save_to_archive(self, data: List[Any], category: str):
        """데이터를 아카이브에 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = ARCHIVE_DIR / f"{category}_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([asdict(d) if hasattr(d, '__dataclass_fields__') else d for d in data],
                     f, indent=2, default=str, ensure_ascii=False)

        print(f"[저장] {filename}")
        return filename


# 사용 예시
if __name__ == "__main__":
    collector = FinvizCollector()

    # 뉴스 수집
    print("=== AAPL 뉴스 ===")
    news = collector.get_news("AAPL", limit=5)
    for n in news:
        print(f"  [{n.sentiment}] {n.headline}")

    # 가격 조회
    print("\n=== 가격 데이터 ===")
    for ticker in ["AAPL", "MSFT", "GOOGL"]:
        quote = collector.get_quote(ticker)
        if quote:
            print(f"  {ticker}: ${quote.price:.2f} ({quote.change_percent:+.2f}%)")

    # 스크리너
    print("\n=== 대형주 스크리너 ===")
    results = collector.run_screener({'v': '111', 'f': 'cap_largeover,ta_change_u'})
    for r in results[:5]:
        print(f"  {r.ticker}: {r.company} - ${r.price} ({r.change:+.2f}%)")
