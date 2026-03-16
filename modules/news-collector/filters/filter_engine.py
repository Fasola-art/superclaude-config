#!/usr/bin/env python3
"""
뉴스 필터 엔진
규칙 기반 뉴스 필터링 및 분류

기능:
- 키워드 기반 필터링
- 정규식 패턴 매칭
- 우선순위 설정
- 카테고리 자동 분류
- 중복 제거
"""

import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


MODULE_DIR = Path(__file__).parent.parent
RULES_FILE = Path(__file__).parent / 'filter_rules.json'


class FilterAction(Enum):
    """필터 액션"""
    ACCEPT = 'accept'      # 수락
    REJECT = 'reject'      # 거부
    MODIFY = 'modify'      # 수정 (우선순위, 카테고리 등)


class MatchMode(Enum):
    """매칭 모드"""
    ANY = 'any'           # 하나라도 매칭
    ALL = 'all'           # 모두 매칭


@dataclass
class FilterRule:
    """필터 규칙"""
    id: str
    name: str
    description: str
    enabled: bool
    priority: int
    include_keywords: List[str]
    exclude_keywords: List[str]
    include_match_mode: MatchMode
    exclude_match_mode: MatchMode
    exclude_patterns: List[str]
    min_title_length: int
    max_title_length: int
    actions: Dict


@dataclass
class FilterResult:
    """필터링 결과"""
    accepted: bool
    matched_rules: List[str]
    applied_actions: Dict
    reason: str


class FilterEngine:
    """뉴스 필터 엔진"""

    def __init__(self):
        """초기화"""
        self.rules: List[FilterRule] = []
        self.global_settings: Dict = {}
        self._seen_hashes: Set[str] = set()
        self._seen_time: Dict[str, datetime] = {}
        self._load_rules()

    def _load_rules(self):
        """규칙 로드"""
        if not RULES_FILE.exists():
            return

        try:
            data = json.loads(RULES_FILE.read_text())

            self.global_settings = data.get('globalSettings', {})

            for rule_data in data.get('filters', []):
                rules_config = rule_data.get('rules', {})
                include_config = rules_config.get('include', {})
                exclude_config = rules_config.get('exclude', {})

                rule = FilterRule(
                    id=rule_data['id'],
                    name=rule_data['name'],
                    description=rule_data.get('description', ''),
                    enabled=rule_data.get('enabled', True),
                    priority=rule_data.get('priority', 5),
                    include_keywords=include_config.get('keywords', []),
                    exclude_keywords=exclude_config.get('keywords', []),
                    include_match_mode=MatchMode(include_config.get('matchMode', 'any')),
                    exclude_match_mode=MatchMode(exclude_config.get('matchMode', 'any')),
                    exclude_patterns=rules_config.get('excludePatterns', []),
                    min_title_length=rules_config.get('minTitleLength', 0),
                    max_title_length=rules_config.get('maxTitleLength', 1000),
                    actions=rule_data.get('actions', {})
                )
                self.rules.append(rule)

            # 우선순위 순으로 정렬 (높은 순)
            self.rules.sort(key=lambda x: x.priority, reverse=True)

        except Exception as e:
            print(f"규칙 로드 오류: {e}")

    def _generate_content_hash(self, title: str, url: str) -> str:
        """콘텐츠 해시 생성"""
        content = f"{title.lower().strip()}|{url.lower().strip()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _check_duplicate(self, title: str, url: str) -> bool:
        """
        중복 체크

        Returns:
            True면 중복
        """
        if not self.global_settings.get('deduplicationEnabled', True):
            return False

        content_hash = self._generate_content_hash(title, url)

        # 오래된 해시 정리
        window = self.global_settings.get('deduplicationWindow', 86400)
        cutoff = datetime.now() - timedelta(seconds=window)
        expired = [h for h, t in self._seen_time.items() if t < cutoff]
        for h in expired:
            self._seen_hashes.discard(h)
            del self._seen_time[h]

        if content_hash in self._seen_hashes:
            return True

        self._seen_hashes.add(content_hash)
        self._seen_time[content_hash] = datetime.now()
        return False

    def _match_keywords(
        self,
        text: str,
        keywords: List[str],
        mode: MatchMode
    ) -> Tuple[bool, List[str]]:
        """
        키워드 매칭

        Args:
            text: 검색할 텍스트
            keywords: 키워드 목록
            mode: 매칭 모드

        Returns:
            (매칭 여부, 매칭된 키워드 목록)
        """
        if not keywords:
            return False, []

        text_lower = text.lower()
        matched = []

        for keyword in keywords:
            if keyword.lower() in text_lower:
                matched.append(keyword)

        if mode == MatchMode.ANY:
            return len(matched) > 0, matched
        else:  # ALL
            return len(matched) == len(keywords), matched

    def _match_patterns(self, text: str, patterns: List[str]) -> Tuple[bool, List[str]]:
        """
        정규식 패턴 매칭

        Args:
            text: 검색할 텍스트
            patterns: 패턴 목록

        Returns:
            (매칭 여부, 매칭된 패턴 목록)
        """
        if not patterns:
            return False, []

        matched = []
        for pattern in patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    matched.append(pattern)
            except re.error:
                continue

        return len(matched) > 0, matched

    def apply_rule(self, rule: FilterRule, article: Dict) -> Optional[FilterResult]:
        """
        단일 규칙 적용

        Args:
            rule: 필터 규칙
            article: 기사 데이터 {title, url, summary, ...}

        Returns:
            FilterResult 또는 None (규칙 미적용)
        """
        if not rule.enabled:
            return None

        title = article.get('title', '')
        summary = article.get('summary', '') or ''
        combined_text = f"{title} {summary}"

        matched_rules = []
        actions = {}

        # 제목 길이 체크
        if len(title) < rule.min_title_length:
            return FilterResult(
                accepted=False,
                matched_rules=[rule.id],
                applied_actions={'reject': True},
                reason=f"제목이 너무 짧음 ({len(title)} < {rule.min_title_length})"
            )

        if len(title) > rule.max_title_length:
            return FilterResult(
                accepted=False,
                matched_rules=[rule.id],
                applied_actions={'reject': True},
                reason=f"제목이 너무 긺 ({len(title)} > {rule.max_title_length})"
            )

        # 제외 키워드 체크 (먼저 실행)
        if rule.exclude_keywords:
            excluded, matched_kw = self._match_keywords(
                combined_text, rule.exclude_keywords, rule.exclude_match_mode
            )
            if excluded:
                return FilterResult(
                    accepted=False,
                    matched_rules=[rule.id],
                    applied_actions={'reject': True},
                    reason=f"제외 키워드 매칭: {matched_kw}"
                )

        # 제외 패턴 체크
        if rule.exclude_patterns:
            pattern_matched, matched_patterns = self._match_patterns(
                combined_text, rule.exclude_patterns
            )
            if pattern_matched:
                return FilterResult(
                    accepted=False,
                    matched_rules=[rule.id],
                    applied_actions={'reject': True},
                    reason=f"제외 패턴 매칭: {matched_patterns}"
                )

        # 포함 키워드 체크
        if rule.include_keywords:
            included, matched_kw = self._match_keywords(
                combined_text, rule.include_keywords, rule.include_match_mode
            )
            if included:
                matched_rules.append(rule.id)
                actions.update(rule.actions)
                return FilterResult(
                    accepted=True,
                    matched_rules=matched_rules,
                    applied_actions=actions,
                    reason=f"포함 키워드 매칭: {matched_kw}"
                )

        # 거부 액션 체크
        if rule.actions.get('reject'):
            return FilterResult(
                accepted=False,
                matched_rules=[rule.id],
                applied_actions={'reject': True},
                reason="규칙에 의해 거부됨"
            )

        return None

    def filter_article(self, article: Dict) -> FilterResult:
        """
        기사 필터링

        Args:
            article: 기사 데이터 {title, url, summary, source, ...}

        Returns:
            FilterResult
        """
        title = article.get('title', '')
        url = article.get('url', '')

        # 중복 체크
        if self._check_duplicate(title, url):
            return FilterResult(
                accepted=False,
                matched_rules=['deduplication'],
                applied_actions={'reject': True},
                reason="중복 기사"
            )

        # 언어 필터
        allowed_langs = self.global_settings.get('languageFilter', [])
        if allowed_langs:
            article_lang = article.get('language', 'en')
            if article_lang not in allowed_langs:
                return FilterResult(
                    accepted=False,
                    matched_rules=['language_filter'],
                    applied_actions={'reject': True},
                    reason=f"언어 필터링: {article_lang}"
                )

        # 규칙 적용
        all_matched_rules = []
        all_actions = {}

        for rule in self.rules:
            result = self.apply_rule(rule, article)
            if result:
                if not result.accepted:
                    return result  # 거부되면 즉시 반환

                all_matched_rules.extend(result.matched_rules)
                all_actions.update(result.applied_actions)

        # 기본 액션
        default_action = self.global_settings.get('defaultAction', 'accept')
        accepted = default_action == 'accept'

        return FilterResult(
            accepted=accepted,
            matched_rules=all_matched_rules,
            applied_actions=all_actions,
            reason="기본 정책 적용" if not all_matched_rules else "규칙 매칭"
        )

    def filter_articles(self, articles: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        기사 목록 필터링

        Args:
            articles: 기사 목록

        Returns:
            (수락된 기사, 거부된 기사)
        """
        accepted = []
        rejected = []

        for article in articles:
            result = self.filter_article(article)

            if result.accepted:
                # 액션 적용
                if result.applied_actions.get('setCategory'):
                    article['category'] = result.applied_actions['setCategory']
                if result.applied_actions.get('setPriority'):
                    article['priority'] = result.applied_actions['setPriority']
                if result.applied_actions.get('boostPriority'):
                    current = article.get('priority_boost', 0)
                    article['priority_boost'] = current + result.applied_actions['boostPriority']

                article['matched_filters'] = result.matched_rules
                accepted.append(article)
            else:
                article['rejection_reason'] = result.reason
                rejected.append(article)

        # 우선순위로 정렬
        accepted.sort(
            key=lambda x: x.get('priority_boost', 0),
            reverse=True
        )

        return accepted, rejected

    def get_stats(self) -> Dict:
        """필터 통계 조회"""
        return {
            'total_rules': len(self.rules),
            'enabled_rules': sum(1 for r in self.rules if r.enabled),
            'seen_articles': len(self._seen_hashes),
            'rules': [
                {
                    'id': r.id,
                    'name': r.name,
                    'enabled': r.enabled,
                    'priority': r.priority
                }
                for r in self.rules
            ]
        }


# 테스트
if __name__ == '__main__':
    engine = FilterEngine()

    print("=== 필터 엔진 테스트 ===\n")

    # 통계
    stats = engine.get_stats()
    print(f"총 규칙: {stats['total_rules']}개")
    print(f"활성 규칙: {stats['enabled_rules']}개\n")

    # 테스트 기사
    test_articles = [
        {
            'title': 'OpenAI announces GPT-5 with major improvements',
            'url': 'https://example.com/gpt5',
            'summary': 'OpenAI has released GPT-5, featuring better reasoning capabilities.',
            'language': 'en'
        },
        {
            'title': 'BREAKING: Bitcoin surges above $100,000',
            'url': 'https://example.com/btc100k',
            'summary': 'Bitcoin reaches new all-time high amid institutional buying.',
            'language': 'en'
        },
        {
            'title': 'Buy now! Limited offer - 50% off',
            'url': 'https://example.com/spam',
            'summary': 'Get rich quick with this amazing offer.',
            'language': 'en'
        },
        {
            'title': 'A',
            'url': 'https://example.com/short',
            'summary': 'Too short title.',
            'language': 'en'
        }
    ]

    accepted, rejected = engine.filter_articles(test_articles)

    print("수락된 기사:")
    for article in accepted:
        print(f"  - {article['title'][:50]}...")
        print(f"    필터: {article.get('matched_filters', [])}")

    print(f"\n거부된 기사: {len(rejected)}개")
    for article in rejected:
        print(f"  - {article['title'][:50]}...")
        print(f"    사유: {article.get('rejection_reason', 'N/A')}")
