#!/usr/bin/env python3
"""
뉴스 소스 관리자
RSS, API, 스크래핑 등 다양한 소스에서 뉴스 수집

기능:
- 다중 소스 타입 지원 (RSS, API, Scrape)
- 소스 우선순위 관리
- 자동 새로고침 스케줄링
- 중복 제거
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error


MODULE_DIR = Path(__file__).parent.parent
SOURCES_FILE = Path(__file__).parent / 'rss_sources.json'
CACHE_DIR = MODULE_DIR / 'cache'


class SourceType(Enum):
    """소스 타입"""
    RSS = 'rss'
    API = 'api'
    SCRAPE = 'scrape'


@dataclass
class NewsSource:
    """뉴스 소스 정보"""
    id: str
    name: str
    source_type: SourceType
    url: str
    category: str
    language: str
    enabled: bool
    priority: int
    refresh_interval: int  # 초 단위
    description: str = ''
    last_fetch: Optional[str] = None
    last_error: Optional[str] = None


@dataclass
class FetchedArticle:
    """수집된 기사"""
    id: str
    source_id: str
    title: str
    url: str
    summary: Optional[str]
    published_at: str
    fetched_at: str
    content_hash: str


class SourceManager:
    """뉴스 소스 관리자"""

    def __init__(self):
        """초기화"""
        self.sources: Dict[str, NewsSource] = {}
        self.cache: Dict[str, List[FetchedArticle]] = {}
        self._load_sources()
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """캐시 디렉토리 생성"""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _load_sources(self):
        """소스 설정 로드"""
        if not SOURCES_FILE.exists():
            return

        try:
            data = json.loads(SOURCES_FILE.read_text())
            for src in data.get('sources', []):
                self.sources[src['id']] = NewsSource(
                    id=src['id'],
                    name=src['name'],
                    source_type=SourceType(src['type']),
                    url=src['url'],
                    category=src['category'],
                    language=src['language'],
                    enabled=src.get('enabled', True),
                    priority=src.get('priority', 5),
                    refresh_interval=src.get('refreshInterval', 3600),
                    description=src.get('description', '')
                )
        except Exception as e:
            print(f"소스 로드 오류: {e}")

    def save_sources(self):
        """소스 설정 저장"""
        data = {
            'sources': [
                {
                    'id': s.id,
                    'name': s.name,
                    'type': s.source_type.value,
                    'url': s.url,
                    'category': s.category,
                    'language': s.language,
                    'enabled': s.enabled,
                    'priority': s.priority,
                    'refreshInterval': s.refresh_interval,
                    'description': s.description
                }
                for s in self.sources.values()
            ],
            'metadata': {
                'version': '1.0.0',
                'lastUpdated': datetime.now().strftime('%Y-%m-%d'),
                'totalSources': len(self.sources),
                'enabledSources': sum(1 for s in self.sources.values() if s.enabled)
            }
        }
        SOURCES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def get_enabled_sources(self) -> List[NewsSource]:
        """활성화된 소스 목록 반환 (우선순위 순)"""
        return sorted(
            [s for s in self.sources.values() if s.enabled],
            key=lambda x: x.priority,
            reverse=True
        )

    def add_source(self, source_config: Dict) -> NewsSource:
        """
        새 소스 추가

        Args:
            source_config: 소스 설정

        Returns:
            생성된 NewsSource 객체
        """
        source = NewsSource(
            id=source_config.get('id', f"src_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
            name=source_config['name'],
            source_type=SourceType(source_config.get('type', 'rss')),
            url=source_config['url'],
            category=source_config.get('category', 'general'),
            language=source_config.get('language', 'en'),
            enabled=source_config.get('enabled', True),
            priority=source_config.get('priority', 5),
            refresh_interval=source_config.get('refreshInterval', 3600),
            description=source_config.get('description', '')
        )
        self.sources[source.id] = source
        self.save_sources()
        return source

    def remove_source(self, source_id: str) -> bool:
        """소스 삭제"""
        if source_id in self.sources:
            del self.sources[source_id]
            self.save_sources()
            return True
        return False

    def toggle_source(self, source_id: str) -> bool:
        """소스 활성화/비활성화 토글"""
        if source_id in self.sources:
            self.sources[source_id].enabled = not self.sources[source_id].enabled
            self.save_sources()
            return self.sources[source_id].enabled
        return False

    def _generate_article_id(self, url: str) -> str:
        """기사 ID 생성"""
        return hashlib.md5(url.encode()).hexdigest()[:12]

    def _generate_content_hash(self, title: str, url: str) -> str:
        """콘텐츠 해시 생성 (중복 제거용)"""
        content = f"{title}|{url}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def fetch_rss(self, source: NewsSource) -> List[FetchedArticle]:
        """
        RSS 피드 수집

        Args:
            source: 뉴스 소스

        Returns:
            수집된 기사 목록
        """
        articles = []
        try:
            # URL 요청
            req = urllib.request.Request(
                source.url,
                headers={'User-Agent': 'SuperClaude NewsCollector/1.0'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                xml_content = response.read().decode('utf-8')

            # XML 파싱
            root = ET.fromstring(xml_content)

            # RSS 2.0 또는 Atom 처리
            items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')

            for item in items[:50]:  # 최대 50개
                # 제목
                title_elem = item.find('title') or item.find('{http://www.w3.org/2005/Atom}title')
                title = title_elem.text if title_elem is not None else ''

                # URL
                link_elem = item.find('link') or item.find('{http://www.w3.org/2005/Atom}link')
                if link_elem is not None:
                    url = link_elem.text or link_elem.get('href', '')
                else:
                    url = ''

                # 요약
                desc_elem = (
                    item.find('description') or
                    item.find('{http://www.w3.org/2005/Atom}summary') or
                    item.find('{http://www.w3.org/2005/Atom}content')
                )
                summary = desc_elem.text if desc_elem is not None else None

                # 발행일
                pub_elem = (
                    item.find('pubDate') or
                    item.find('{http://www.w3.org/2005/Atom}published') or
                    item.find('{http://www.w3.org/2005/Atom}updated')
                )
                published_at = pub_elem.text if pub_elem is not None else datetime.now().isoformat()

                if title and url:
                    articles.append(FetchedArticle(
                        id=self._generate_article_id(url),
                        source_id=source.id,
                        title=title.strip(),
                        url=url.strip(),
                        summary=summary[:500] if summary else None,
                        published_at=published_at,
                        fetched_at=datetime.now().isoformat(),
                        content_hash=self._generate_content_hash(title, url)
                    ))

            source.last_fetch = datetime.now().isoformat()
            source.last_error = None

        except Exception as e:
            source.last_error = str(e)
            print(f"RSS 수집 오류 [{source.id}]: {e}")

        return articles

    def fetch_api(self, source: NewsSource) -> List[FetchedArticle]:
        """
        API에서 뉴스 수집

        Args:
            source: 뉴스 소스

        Returns:
            수집된 기사 목록
        """
        articles = []
        try:
            req = urllib.request.Request(
                source.url,
                headers={'User-Agent': 'SuperClaude NewsCollector/1.0'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))

            # Hacker News API 처리
            if source.id == 'hackernews':
                story_ids = data[:30]  # 상위 30개

                for story_id in story_ids:
                    try:
                        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                        req = urllib.request.Request(story_url)
                        with urllib.request.urlopen(req, timeout=10) as resp:
                            story = json.loads(resp.read().decode('utf-8'))

                        if story and story.get('title'):
                            url = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                            articles.append(FetchedArticle(
                                id=self._generate_article_id(url),
                                source_id=source.id,
                                title=story['title'],
                                url=url,
                                summary=None,
                                published_at=datetime.fromtimestamp(
                                    story.get('time', datetime.now().timestamp())
                                ).isoformat(),
                                fetched_at=datetime.now().isoformat(),
                                content_hash=self._generate_content_hash(story['title'], url)
                            ))
                    except Exception:
                        continue

            source.last_fetch = datetime.now().isoformat()
            source.last_error = None

        except Exception as e:
            source.last_error = str(e)
            print(f"API 수집 오류 [{source.id}]: {e}")

        return articles

    def fetch_source(self, source: NewsSource) -> List[FetchedArticle]:
        """
        소스에서 뉴스 수집

        Args:
            source: 뉴스 소스

        Returns:
            수집된 기사 목록
        """
        if source.source_type == SourceType.RSS:
            return self.fetch_rss(source)
        elif source.source_type == SourceType.API:
            return self.fetch_api(source)
        else:
            return []  # 스크래핑은 별도 구현 필요

    def fetch_all(self, force: bool = False) -> Dict[str, List[FetchedArticle]]:
        """
        모든 활성 소스에서 뉴스 수집

        Args:
            force: True면 새로고침 간격 무시

        Returns:
            {source_id: [articles]}
        """
        results = {}
        now = datetime.now()

        for source in self.get_enabled_sources():
            # 새로고침 간격 체크
            if not force and source.last_fetch:
                try:
                    last = datetime.fromisoformat(source.last_fetch)
                    if (now - last).total_seconds() < source.refresh_interval:
                        continue
                except ValueError:
                    pass

            articles = self.fetch_source(source)
            if articles:
                results[source.id] = articles
                self.cache[source.id] = articles

        return results

    def get_status(self) -> Dict:
        """소스 상태 조회"""
        return {
            'total_sources': len(self.sources),
            'enabled_sources': sum(1 for s in self.sources.values() if s.enabled),
            'sources': [
                {
                    'id': s.id,
                    'name': s.name,
                    'type': s.source_type.value,
                    'enabled': s.enabled,
                    'priority': s.priority,
                    'last_fetch': s.last_fetch,
                    'last_error': s.last_error
                }
                for s in sorted(self.sources.values(), key=lambda x: x.priority, reverse=True)
            ]
        }


# 테스트
if __name__ == '__main__':
    manager = SourceManager()

    print("=== 뉴스 소스 관리자 테스트 ===\n")

    # 상태 확인
    status = manager.get_status()
    print(f"총 소스: {status['total_sources']}개")
    print(f"활성 소스: {status['enabled_sources']}개\n")

    # 활성 소스 목록
    print("활성 소스 목록:")
    for source in manager.get_enabled_sources()[:5]:
        print(f"  - {source.name} ({source.source_type.value}, P{source.priority})")

    # 테스트 수집 (하나만)
    print("\n첫 번째 소스에서 수집 테스트...")
    first_source = manager.get_enabled_sources()[0]
    articles = manager.fetch_source(first_source)
    print(f"수집된 기사: {len(articles)}개")

    if articles:
        print(f"\n최신 기사: {articles[0].title[:50]}...")
