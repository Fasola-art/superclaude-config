#!/usr/bin/env python3
"""
Bloomberg 뉴스 수집기
- 시장 뉴스
- 경제 뉴스
- 기업 뉴스
- 오피니언/분석

Note: Bloomberg API는 유료($2000+/월)이므로 RSS 피드와 웹 스크래핑 사용
"""

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import urllib.request
import urllib.parse
from email.utils import parsedate_to_datetime

# 설정
ARCHIVE_DIR = Path.home() / ".claude" / "modules" / "news-collector" / "archive" / "bloomberg"

# Bloomberg RSS 피드 URL
BLOOMBERG_FEEDS = {
    "markets": "https://feeds.bloomberg.com/markets/news.rss",
    "technology": "https://feeds.bloomberg.com/technology/news.rss",
    "politics": "https://feeds.bloomberg.com/politics/news.rss",
    "wealth": "https://feeds.bloomberg.com/wealth/news.rss",
    "economics": "https://feeds.bloomberg.com/economics/news.rss",
    "industries": "https://feeds.bloomberg.com/industries/news.rss",
}


@dataclass
class BloombergArticle:
    """Bloomberg 기사 데이터"""
    title: str
    description: str
    url: str
    category: str
    published: datetime
    author: Optional[str] = None
    tags: List[str] = None
    sentiment: Optional[str] = None
    importance: str = "normal"  # high, normal, low

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class MarketSummary:
    """시장 요약 데이터"""
    index: str
    value: float
    change: float
    change_percent: float
    timestamp: datetime


class BloombergCollector:
    """Bloomberg 데이터 수집기"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

        # 중요 키워드 (하이라이트용)
        self.high_importance_keywords = [
            'fed', 'fomc', 'rate', 'inflation', 'cpi', 'gdp', 'recession',
            'earnings', 'guidance', 'merger', 'acquisition', 'ipo',
            'crash', 'surge', 'plunge', 'record', 'breaking'
        ]

    def _fetch_rss(self, url: str) -> str:
        """RSS 피드 가져오기"""
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"[에러] RSS 요청 실패: {url} - {e}")
            return ""

    def get_news(self, category: str = "markets", limit: int = 50) -> List[BloombergArticle]:
        """
        카테고리별 뉴스 수집

        Args:
            category: markets, technology, politics, wealth, economics, industries
            limit: 최대 기사 수
        """
        articles = []

        feed_url = BLOOMBERG_FEEDS.get(category)
        if not feed_url:
            print(f"[경고] 알 수 없는 카테고리: {category}")
            return articles

        rss_content = self._fetch_rss(feed_url)
        if not rss_content:
            return articles

        try:
            root = ET.fromstring(rss_content)
            channel = root.find('channel')

            if channel is None:
                return articles

            for item in channel.findall('item')[:limit]:
                title = item.findtext('title', '')
                description = item.findtext('description', '')
                link = item.findtext('link', '')
                pub_date = item.findtext('pubDate', '')
                author = item.findtext('author', '')

                # 날짜 파싱
                try:
                    published = parsedate_to_datetime(pub_date) if pub_date else datetime.now()
                except:
                    published = datetime.now()

                # 태그 추출
                tags = []
                for tag_elem in item.findall('category'):
                    if tag_elem.text:
                        tags.append(tag_elem.text)

                article = BloombergArticle(
                    title=title,
                    description=self._clean_html(description),
                    url=link,
                    category=category,
                    published=published,
                    author=author,
                    tags=tags,
                    sentiment=self._analyze_sentiment(title + ' ' + description),
                    importance=self._assess_importance(title)
                )
                articles.append(article)

        except ET.ParseError as e:
            print(f"[에러] RSS 파싱 실패: {e}")

        return articles

    def get_all_news(self, limit_per_category: int = 20) -> Dict[str, List[BloombergArticle]]:
        """모든 카테고리 뉴스 수집"""
        all_news = {}

        for category in BLOOMBERG_FEEDS.keys():
            print(f"[수집] Bloomberg {category}...")
            articles = self.get_news(category, limit_per_category)
            all_news[category] = articles
            print(f"  → {len(articles)}개 기사")

        return all_news

    def get_breaking_news(self) -> List[BloombergArticle]:
        """속보/중요 뉴스만 필터링"""
        breaking = []

        for category in ['markets', 'economics']:
            articles = self.get_news(category, limit=30)
            for article in articles:
                if article.importance == 'high':
                    breaking.append(article)

        # 시간순 정렬 (최신 먼저)
        breaking.sort(key=lambda x: x.published, reverse=True)
        return breaking[:20]

    def search_news(self, keyword: str, hours: int = 24) -> List[BloombergArticle]:
        """
        키워드로 뉴스 검색

        Args:
            keyword: 검색 키워드
            hours: 최근 N시간 내 기사만
        """
        results = []
        cutoff = datetime.now() - timedelta(hours=hours)
        keyword_lower = keyword.lower()

        for category in BLOOMBERG_FEEDS.keys():
            articles = self.get_news(category, limit=50)
            for article in articles:
                if article.published.replace(tzinfo=None) < cutoff:
                    continue

                # 제목, 설명, 태그에서 검색
                searchable = (article.title + ' ' + article.description + ' ' + ' '.join(article.tags)).lower()
                if keyword_lower in searchable:
                    results.append(article)

        # 중복 제거 (URL 기준)
        seen_urls = set()
        unique_results = []
        for article in results:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_results.append(article)

        return unique_results

    def get_market_summary(self) -> List[MarketSummary]:
        """
        주요 지수 요약
        Note: Bloomberg 웹페이지 스크래핑 (변경 가능)
        """
        # Bloomberg API 없이는 정확한 실시간 데이터 어려움
        # 대안: Yahoo Finance API 또는 다른 소스 사용 권장

        indices = [
            ('S&P 500', 'SPX'),
            ('Dow Jones', 'DJIA'),
            ('Nasdaq', 'CCMP'),
            ('Russell 2000', 'RTY')
        ]

        summaries = []
        # 실제 구현시 WebFetch나 다른 API 사용

        return summaries

    def _clean_html(self, text: str) -> str:
        """HTML 태그 제거"""
        clean = re.sub(r'<[^>]+>', '', text)
        clean = re.sub(r'\s+', ' ', clean)
        return clean.strip()

    def _analyze_sentiment(self, text: str) -> str:
        """감성 분석"""
        positive_words = [
            'surge', 'jump', 'gain', 'rise', 'rally', 'bull', 'growth',
            'beat', 'exceed', 'strong', 'positive', 'optimistic', 'boost'
        ]
        negative_words = [
            'drop', 'fall', 'decline', 'plunge', 'crash', 'bear', 'loss',
            'miss', 'weak', 'negative', 'pessimistic', 'fear', 'risk'
        ]

        text_lower = text.lower()
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)

        if pos_count > neg_count + 1:
            return 'positive'
        elif neg_count > pos_count + 1:
            return 'negative'
        return 'neutral'

    def _assess_importance(self, title: str) -> str:
        """중요도 평가"""
        title_lower = title.lower()

        for keyword in self.high_importance_keywords:
            if keyword in title_lower:
                return 'high'

        return 'normal'

    def save_to_archive(self, data: Dict[str, List[BloombergArticle]], prefix: str = "news"):
        """아카이브 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = ARCHIVE_DIR / f"{prefix}_{timestamp}.json"

        # dataclass를 dict로 변환
        serializable = {}
        for category, articles in data.items():
            serializable[category] = [asdict(a) for a in articles]

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, default=str, ensure_ascii=False)

        print(f"[저장] {filename}")
        return filename

    def generate_daily_digest(self) -> Dict[str, Any]:
        """일일 뉴스 다이제스트 생성"""
        all_news = self.get_all_news(limit_per_category=30)

        digest = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_articles': sum(len(v) for v in all_news.values()),
                'by_category': {k: len(v) for k, v in all_news.items()},
                'high_importance': 0,
                'sentiment_breakdown': {'positive': 0, 'negative': 0, 'neutral': 0}
            },
            'top_stories': [],
            'by_category': {}
        }

        # 통계 계산
        for category, articles in all_news.items():
            for article in articles:
                if article.importance == 'high':
                    digest['summary']['high_importance'] += 1
                    digest['top_stories'].append({
                        'title': article.title,
                        'category': category,
                        'url': article.url
                    })
                digest['summary']['sentiment_breakdown'][article.sentiment] += 1

            # 카테고리별 상위 5개
            digest['by_category'][category] = [
                {'title': a.title, 'url': a.url, 'sentiment': a.sentiment}
                for a in articles[:5]
            ]

        # 상위 스토리 10개로 제한
        digest['top_stories'] = digest['top_stories'][:10]

        return digest


# 사용 예시
if __name__ == "__main__":
    collector = BloombergCollector()

    # 시장 뉴스 수집
    print("=== Bloomberg 시장 뉴스 ===")
    news = collector.get_news("markets", limit=5)
    for article in news:
        importance = "🔥" if article.importance == 'high' else "  "
        sentiment = {"positive": "📈", "negative": "📉", "neutral": "➡️"}[article.sentiment]
        print(f"{importance} {sentiment} {article.title[:60]}...")

    # 속보 확인
    print("\n=== 속보 ===")
    breaking = collector.get_breaking_news()
    for article in breaking[:5]:
        print(f"  🚨 {article.title[:50]}...")

    # 키워드 검색
    print("\n=== 'Fed' 관련 뉴스 ===")
    fed_news = collector.search_news("fed", hours=48)
    for article in fed_news[:3]:
        print(f"  • {article.title[:50]}...")
