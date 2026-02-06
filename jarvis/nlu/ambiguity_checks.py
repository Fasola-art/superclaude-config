#!/usr/bin/env python3
"""
모호성 체크 함수 모음 - 개별 요인 감지
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .classifier import classify_multi, get_confidence_gap


# 의미어 추출용 불용어 (한국어 + 영어)
STOPWORDS = frozenset([
    "해", "줘", "해줘", "좀", "하고", "그", "이", "저", "것", "거",
    "은", "는", "이", "가", "을", "를", "에", "의", "로", "와", "과",
    "do", "the", "a", "an", "is", "it", "to", "and", "or", "in", "on",
    "please", "can", "you", "help", "me", "want", "need",
])

# 과도한 범위 지시어
BROAD_TERMS = frozenset([
    "전부", "다", "모든", "전체", "싹", "통째로", "everything",
    "all", "every", "entire", "whole", "completely",
])


@dataclass
class AmbiguityFactor:
    """개별 모호성 요인"""

    weight: float
    reason: str


def extract_meaningful_words(text: str) -> list[str]:
    """불용어 제거 후 의미어 추출"""
    words = re.findall(r"[가-힣]+|[a-zA-Z]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def check_broad_scope(text: str) -> AmbiguityFactor | None:
    """과도한 범위 지시어 감지"""
    text_lower = text.lower()
    found = [t for t in BROAD_TERMS if t in text_lower]
    if found:
        return AmbiguityFactor(
            weight=0.25,
            reason=f"과도한 범위 지시어 감지: {', '.join(found[:3])}",
        )
    return None


def check_keyword_shortage(text: str, min_keywords: int = 2) -> AmbiguityFactor | None:
    """의미 키워드 부족 감지"""
    meaningful = extract_meaningful_words(text)
    if len(meaningful) < min_keywords:
        return AmbiguityFactor(
            weight=0.30,
            reason=f"의미 키워드 부족 ({len(meaningful)}개, 최소 {min_keywords}개 필요)",
        )
    return None


def check_multi_intent(text: str) -> AmbiguityFactor | None:
    """다중 Intent 충돌 감지"""
    results = classify_multi(text)
    gap = get_confidence_gap(results)

    if gap < 0.15 and len(results) >= 2:
        top_two = [r.intent.name for r in results[:2]]
        return AmbiguityFactor(
            weight=0.35,
            reason=f"다중 Intent 매칭 (차이 {gap:.2f}): {top_two[0]} vs {top_two[1]}",
        )
    return None


def check_low_confidence(text: str) -> AmbiguityFactor | None:
    """최고 신뢰도 낮음 감지"""
    results = classify_multi(text)
    if results[0].score < 0.50:
        return AmbiguityFactor(
            weight=0.30,
            reason=f"Intent 신뢰도 낮음 ({results[0].score:.2f})",
        )
    return None


def generate_suggestions(factors: list[AmbiguityFactor]) -> list[str]:
    """모호성 요인에 따른 명확화 제안 생성"""
    suggestion_map = {
        "범위": "구체적인 대상을 지정해주세요 (예: 어떤 파일/기능?)",
        "키워드": "무엇을 하고 싶은지 구체적으로 알려주세요",
        "다중 Intent": "하나의 작업에 집중해주세요",
        "신뢰도": "어떤 종류의 작업인지 명시해주세요",
    }

    suggestions: list[str] = []
    for factor in factors:
        for key, suggestion in suggestion_map.items():
            if key in factor.reason:
                suggestions.append(suggestion)
                break

    return suggestions[:3]
