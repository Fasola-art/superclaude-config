#!/usr/bin/env python3
"""
News Collector Module
SuperClaude v2.0.9 뉴스 수집 모듈

기능:
- 다중 소스 뉴스 수집
- 키워드 필터링
- 알림 시스템
- 아카이브 관리
"""

import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
from urllib.parse import urlparse

MODULE_DIR = Path.home() / '.claude' / 'modules' / 'news-collector'
CONFIG_FILE = MODULE_DIR / 'config.json'
SOURCES_DIR = MODULE_DIR / 'sources'
FILTERS_DIR = MODULE_DIR / 'filters'
ALERTS_DIR = MODULE_DIR / 'alerts'
ARCHIVE_DIR = MODULE_DIR / 'archive'


class NewsPriority(Enum):
    CRITICAL = 'critical'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class NewsCategory(Enum):
    TECHNOLOGY = 'technology'
    FINANCE = 'finance'
    CRYPTO = 'crypto'
    AI = 'ai'
    MARKET = 'market'
    GENERAL = 'general'


@dataclass
class NewsArticle:
    """뉴스 기사"""
    id: str
    title: str
    url: str
    source: str
    category: NewsCategory
    summary: Optional[str]
    content: Optional[str]
    publishedAt: str
    collectedAt: str
    keywords: List[str]
    priority: NewsPriority
    sentiment: Optional[float]  # -1.0 ~ 1.0


@dataclass
class NewsFilter:
    """뉴스 필터"""
    id: str
    name: str
    keywords: List[str]
    excludeKeywords: List[str]
    sources: List[str]
    categories: List[NewsCategory]
    minPriority: NewsPriority
    enabled: bool


def load_config() -> Dict:
    """설정 로드"""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {
        'sources': [
            {'name': 'techcrunch', 'type': 'rss', 'url': 'https://techcrunch.com/feed/'},
            {'name': 'hackernews', 'type': 'api', 'url': 'https://hacker-news.firebaseio.com/v0/'},
            {'name': 'coindesk', 'type': 'rss', 'url': 'https://www.coindesk.com/arc/outboundfeeds/rss/'}
        ],
        'filters': {
            'defaultKeywords': ['AI', 'GPT', 'LLM', 'Claude', 'OpenAI', 'Anthropic'],
            'excludeKeywords': ['광고', 'sponsored']
        },
        'alerts': {
            'enabled': True,
            'criticalKeywords': ['breaking', '속보', 'urgent'],
            'notifyOn': ['critical', 'high']
        },
        'archive': {
            'retentionDays': 30,
            'maxItems': 10000
        }
    }


def ensure_dirs():
    """디렉토리 생성"""
    for dir_path in [SOURCES_DIR, FILTERS_DIR, ALERTS_DIR, ARCHIVE_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)


# ============ 뉴스 수집 ============

class NewsCollector:
    """뉴스 수집기"""

    def __init__(self):
        self.config = load_config()
        ensure_dirs()

    def generate_article_id(self, url: str) -> str:
        """기사 ID 생성"""
        return hashlib.md5(url.encode()).hexdigest()[:12]

    def extract_keywords(self, text: str) -> List[str]:
        """키워드 추출 (간단한 버전)"""
        # 영어 불용어
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at',
                     'to', 'for', 'of', 'and', 'or', 'but', 'with', 'by', 'from'}

        # 단어 추출
        words = re.findall(r'\b[A-Za-z가-힣]{3,}\b', text.lower())
        word_counts = {}

        for word in words:
            if word not in stopwords:
                word_counts[word] = word_counts.get(word, 0) + 1

        # 상위 10개 키워드
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:10]]

    def detect_category(self, title: str, content: str = '') -> NewsCategory:
        """카테고리 감지"""
        text = f"{title} {content}".lower()

        category_keywords = {
            NewsCategory.AI: ['ai', 'artificial intelligence', 'machine learning',
                             'deep learning', 'gpt', 'llm', 'neural', 'claude'],
            NewsCategory.CRYPTO: ['bitcoin', 'ethereum', 'crypto', 'blockchain',
                                  'defi', 'nft', 'web3', 'btc', 'eth'],
            NewsCategory.FINANCE: ['stock', 'market', 'investment', 'trading',
                                   'nasdaq', 'dow', 's&p', 'fed', 'interest rate'],
            NewsCategory.TECHNOLOGY: ['tech', 'software', 'hardware', 'startup',
                                      'app', 'platform', 'cloud', 'data']
        }

        for category, keywords in category_keywords.items():
            if any(kw in text for kw in keywords):
                return category

        return NewsCategory.GENERAL

    def detect_priority(self, title: str, content: str = '') -> NewsPriority:
        """우선순위 감지"""
        text = f"{title} {content}".lower()

        critical_keywords = self.config['alerts'].get('criticalKeywords', [])
        if any(kw.lower() in text for kw in critical_keywords):
            return NewsPriority.CRITICAL

        high_keywords = ['breaking', 'major', 'significant', 'important', 'exclusive']
        if any(kw in text for kw in high_keywords):
            return NewsPriority.HIGH

        medium_keywords = ['update', 'announce', 'launch', 'release', 'report']
        if any(kw in text for kw in medium_keywords):
            return NewsPriority.MEDIUM

        return NewsPriority.LOW

    def simple_sentiment(self, text: str) -> float:
        """간단한 감성 분석 (-1.0 ~ 1.0)"""
        positive_words = ['good', 'great', 'excellent', 'success', 'growth',
                         'gain', 'rise', 'surge', 'bullish', 'positive', '상승', '호재']
        negative_words = ['bad', 'fail', 'loss', 'decline', 'drop', 'crash',
                         'bearish', 'negative', 'concern', 'risk', '하락', '악재']

        text_lower = text.lower()
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)

        total = pos_count + neg_count
        if total == 0:
            return 0.0

        return round((pos_count - neg_count) / total, 2)

    def create_article(
        self,
        title: str,
        url: str,
        source: str,
        summary: str = None,
        content: str = None,
        published_at: str = None
    ) -> NewsArticle:
        """기사 객체 생성"""
        combined_text = f"{title} {summary or ''} {content or ''}"

        return NewsArticle(
            id=self.generate_article_id(url),
            title=title,
            url=url,
            source=source,
            category=self.detect_category(title, combined_text),
            summary=summary,
            content=content,
            publishedAt=published_at or datetime.now().isoformat(),
            collectedAt=datetime.now().isoformat(),
            keywords=self.extract_keywords(combined_text),
            priority=self.detect_priority(title, combined_text),
            sentiment=self.simple_sentiment(combined_text)
        )


# ============ 필터 시스템 ============

class FilterEngine:
    """필터 엔진"""

    def __init__(self):
        self.config = load_config()
        self.filters = self._load_filters()

    def _load_filters(self) -> List[NewsFilter]:
        """필터 로드"""
        filters = []
        filter_file = FILTERS_DIR / 'active_filters.json'

        if filter_file.exists():
            try:
                data = json.loads(filter_file.read_text())
                for f in data:
                    filters.append(NewsFilter(
                        id=f['id'],
                        name=f['name'],
                        keywords=f.get('keywords', []),
                        excludeKeywords=f.get('excludeKeywords', []),
                        sources=f.get('sources', []),
                        categories=[NewsCategory(c) for c in f.get('categories', [])],
                        minPriority=NewsPriority(f.get('minPriority', 'low')),
                        enabled=f.get('enabled', True)
                    ))
            except Exception:
                pass

        return filters

    def save_filters(self):
        """필터 저장"""
        filter_file = FILTERS_DIR / 'active_filters.json'
        data = [
            {
                'id': f.id,
                'name': f.name,
                'keywords': f.keywords,
                'excludeKeywords': f.excludeKeywords,
                'sources': f.sources,
                'categories': [c.value for c in f.categories],
                'minPriority': f.minPriority.value,
                'enabled': f.enabled
            }
            for f in self.filters
        ]
        filter_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def add_filter(self, filter_config: Dict) -> NewsFilter:
        """필터 추가"""
        new_filter = NewsFilter(
            id=f"filter_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=filter_config.get('name', 'Unnamed Filter'),
            keywords=filter_config.get('keywords', []),
            excludeKeywords=filter_config.get('excludeKeywords', []),
            sources=filter_config.get('sources', []),
            categories=[NewsCategory(c) for c in filter_config.get('categories', [])],
            minPriority=NewsPriority(filter_config.get('minPriority', 'low')),
            enabled=True
        )

        self.filters.append(new_filter)
        self.save_filters()
        return new_filter

    def apply_filter(self, article: NewsArticle, news_filter: NewsFilter) -> bool:
        """필터 적용 (통과하면 True)"""
        if not news_filter.enabled:
            return True

        text = f"{article.title} {article.summary or ''}"
        text_lower = text.lower()

        # 제외 키워드 체크
        for exclude in news_filter.excludeKeywords:
            if exclude.lower() in text_lower:
                return False

        # 포함 키워드 체크 (하나라도 있으면 통과)
        if news_filter.keywords:
            if not any(kw.lower() in text_lower for kw in news_filter.keywords):
                return False

        # 소스 체크
        if news_filter.sources:
            if article.source not in news_filter.sources:
                return False

        # 카테고리 체크
        if news_filter.categories:
            if article.category not in news_filter.categories:
                return False

        # 우선순위 체크
        priority_order = [NewsPriority.LOW, NewsPriority.MEDIUM,
                         NewsPriority.HIGH, NewsPriority.CRITICAL]
        if priority_order.index(article.priority) < priority_order.index(news_filter.minPriority):
            return False

        return True

    def filter_articles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """기사 목록 필터링"""
        result = []

        for article in articles:
            passes_all = True
            for news_filter in self.filters:
                if not self.apply_filter(article, news_filter):
                    passes_all = False
                    break

            if passes_all:
                result.append(article)

        return result


# ============ 알림 시스템 ============

class NewsAlertManager:
    """뉴스 알림 관리자"""

    def __init__(self):
        self.config = load_config()
        self.alerts_file = ALERTS_DIR / 'triggered_alerts.json'
        ensure_dirs()

    def load_alerts(self) -> List[Dict]:
        """알림 이력 로드"""
        if self.alerts_file.exists():
            return json.loads(self.alerts_file.read_text())
        return []

    def save_alert(self, alert: Dict):
        """알림 저장"""
        alerts = self.load_alerts()
        alerts.append(alert)
        # 최근 1000개만 유지
        alerts = alerts[-1000:]
        self.alerts_file.write_text(json.dumps(alerts, indent=2, ensure_ascii=False))

    def check_article(self, article: NewsArticle) -> Optional[Dict]:
        """기사에 대한 알림 체크"""
        if not self.config['alerts'].get('enabled', True):
            return None

        notify_priorities = self.config['alerts'].get('notifyOn', ['critical', 'high'])
        if article.priority.value not in notify_priorities:
            return None

        alert = {
            'timestamp': datetime.now().isoformat(),
            'articleId': article.id,
            'title': article.title,
            'url': article.url,
            'source': article.source,
            'category': article.category.value,
            'priority': article.priority.value,
            'sentiment': article.sentiment
        }

        self.save_alert(alert)
        return alert


# ============ 아카이브 관리 ============

class ArchiveManager:
    """아카이브 관리자"""

    def __init__(self):
        self.config = load_config()
        ensure_dirs()

    def archive_article(self, article: NewsArticle):
        """기사 아카이브"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        archive_file = ARCHIVE_DIR / f"news_{date_str}.json"

        articles = []
        if archive_file.exists():
            articles = json.loads(archive_file.read_text())

        # 중복 체크
        if not any(a['id'] == article.id for a in articles):
            # Enum 값을 문자열로 변환
            article_dict = asdict(article)
            article_dict['category'] = article.category.value
            article_dict['priority'] = article.priority.value
            articles.append(article_dict)
            archive_file.write_text(json.dumps(articles, indent=2, ensure_ascii=False))

    def get_archive(
        self,
        start_date: str = None,
        end_date: str = None,
        category: NewsCategory = None
    ) -> List[Dict]:
        """아카이브 조회"""
        result = []

        for archive_file in ARCHIVE_DIR.glob('news_*.json'):
            try:
                file_date = archive_file.stem.replace('news_', '')

                # 날짜 필터
                if start_date and file_date < start_date:
                    continue
                if end_date and file_date > end_date:
                    continue

                articles = json.loads(archive_file.read_text())

                # 카테고리 필터
                if category:
                    articles = [a for a in articles if a.get('category') == category.value]

                result.extend(articles)
            except Exception:
                continue

        return sorted(result, key=lambda x: x.get('publishedAt', ''), reverse=True)

    def cleanup_old_archives(self):
        """오래된 아카이브 정리"""
        retention_days = self.config['archive'].get('retentionDays', 30)
        cutoff_date = datetime.now() - timedelta(days=retention_days)

        deleted_count = 0
        for archive_file in ARCHIVE_DIR.glob('news_*.json'):
            try:
                file_date = archive_file.stem.replace('news_', '')
                if datetime.strptime(file_date, '%Y-%m-%d') < cutoff_date:
                    archive_file.unlink()
                    deleted_count += 1
            except Exception:
                continue

        return deleted_count


# ============ 메인 API ============

def article_to_dict(article: NewsArticle) -> Dict:
    """NewsArticle을 JSON 직렬화 가능한 dict로 변환"""
    result = asdict(article)
    # Enum 값들을 문자열로 변환
    result['category'] = article.category.value
    result['priority'] = article.priority.value
    return result


def collect_news(articles: List[Dict]) -> List[Dict]:
    """뉴스 수집 API"""
    collector = NewsCollector()
    filter_engine = FilterEngine()
    alert_manager = NewsAlertManager()
    archive_manager = ArchiveManager()

    collected = []
    for item in articles:
        article = collector.create_article(
            title=item.get('title', ''),
            url=item.get('url', ''),
            source=item.get('source', 'unknown'),
            summary=item.get('summary'),
            content=item.get('content'),
            published_at=item.get('publishedAt')
        )

        # 필터 적용
        filtered = filter_engine.filter_articles([article])
        if filtered:
            # 알림 체크
            alert = alert_manager.check_article(article)

            # 아카이브
            archive_manager.archive_article(article)

            result = article_to_dict(article)
            result['alert'] = alert is not None
            collected.append(result)

    return collected


def search_archive(
    keywords: List[str] = None,
    category: str = None,
    start_date: str = None,
    end_date: str = None
) -> List[Dict]:
    """아카이브 검색 API"""
    archive_manager = ArchiveManager()

    cat = NewsCategory(category) if category else None
    articles = archive_manager.get_archive(start_date, end_date, cat)

    if keywords:
        keywords_lower = [k.lower() for k in keywords]
        articles = [
            a for a in articles
            if any(kw in f"{a.get('title', '')} {a.get('summary', '')}".lower()
                  for kw in keywords_lower)
        ]

    return articles[:100]  # 최대 100개


if __name__ == '__main__':
    # 테스트
    test_articles = [
        {
            'title': 'Breaking: OpenAI announces GPT-5 with major improvements',
            'url': 'https://example.com/news/gpt5',
            'source': 'techcrunch',
            'summary': 'OpenAI has released GPT-5, the latest version of their large language model.',
            'publishedAt': datetime.now().isoformat()
        },
        {
            'title': 'Bitcoin surges above $100,000 amid institutional buying',
            'url': 'https://example.com/news/btc100k',
            'source': 'coindesk',
            'summary': 'Bitcoin reaches new all-time high as major institutions increase holdings.',
            'publishedAt': datetime.now().isoformat()
        }
    ]

    results = collect_news(test_articles)
    print("=== 수집된 뉴스 ===")
    for article in results:
        print(f"[{article['priority']}] {article['title']}")
        print(f"  카테고리: {article['category']}, 감성: {article['sentiment']}")
        print(f"  키워드: {', '.join(article['keywords'][:5])}")
        print()
