#!/usr/bin/env python3
"""
다중 Intent 분류기 - 모든 매칭 Intent와 점수 반환
"""

from __future__ import annotations

import re

from .intent import INTENT_PATTERNS
from .types import Intent, IntentScore


def _calculate_score(match_count: int) -> float:
    """패턴 매칭 수에 따른 신뢰도 점수 계산"""
    score_map = {
        0: 0.0,
        1: 0.60,
        2: 0.75,
    }
    return score_map.get(match_count, 0.90)


def classify_multi(text: str) -> list[IntentScore]:
    """
    텍스트에서 모든 매칭 Intent + 점수 반환

    Args:
        text: 사용자 입력 텍스트

    Returns:
        IntentScore 리스트 (점수 내림차순 정렬)
    """
    text_lower = text.lower().strip()

    if not text_lower:
        return [IntentScore(intent=Intent.UNKNOWN, score=0.0)]

    results: list[IntentScore] = []

    for intent, patterns in INTENT_PATTERNS.items():
        matched: list[str] = []
        for pattern in patterns:
            if re.search(pattern, text_lower):
                matched.append(pattern)

        if matched:
            score = _calculate_score(len(matched))
            results.append(IntentScore(
                intent=intent,
                score=score,
                matched_patterns=matched,
            ))

    # 점수 내림차순 정렬
    results.sort(key=lambda r: r.score, reverse=True)

    # 매칭 없으면 UNKNOWN 반환
    if not results:
        return [IntentScore(intent=Intent.UNKNOWN, score=0.0)]

    return results


def get_top_intent(text: str) -> IntentScore:
    """최고 점수 Intent 1개 반환"""
    results = classify_multi(text)
    return results[0]


def get_confidence_gap(results: list[IntentScore]) -> float:
    """상위 2개 Intent 간 점수 차이 반환 (모호성 판단용)"""
    if len(results) < 2:
        return 1.0  # Intent 1개면 모호하지 않음
    return abs(results[0].score - results[1].score)
