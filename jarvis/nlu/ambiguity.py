#!/usr/bin/env python3
"""
모호성 점수 계산기 - 불명확한 프롬프트 감지

체크 함수는 ambiguity_checks.py에서 import
"""

from __future__ import annotations

from .ambiguity_checks import (
    AmbiguityFactor,
    check_broad_scope,
    check_keyword_shortage,
    check_low_confidence,
    check_multi_intent,
    generate_suggestions,
)
from .classifier import classify_multi
from .types import AmbiguityResult


def calculate_ambiguity(text: str, min_keywords: int = 2) -> AmbiguityResult:
    """
    텍스트 모호성 점수 계산

    Args:
        text: 사용자 입력 텍스트
        min_keywords: 최소 의미 키워드 수

    Returns:
        AmbiguityResult (score 0.0~1.0)
    """
    if not text or not text.strip():
        return AmbiguityResult(
            score=1.0,
            reason="빈 입력",
            suggestions=["무엇을 도와드릴까요?"],
        )

    # 모호성 요인 수집
    factors: list[AmbiguityFactor] = []
    checks = [
        check_multi_intent(text),
        check_low_confidence(text),
        check_keyword_shortage(text, min_keywords),
        check_broad_scope(text),
    ]

    for result in checks:
        if result is not None:
            factors.append(result)

    # 가중 합산 (최대 1.0)
    total_score = min(1.0, sum(f.weight for f in factors))

    # 이유 문자열 조합
    reason = "; ".join(f.reason for f in factors) if factors else "명확한 입력"

    # 제안 생성 + Intent 정보 첨부
    suggestions = generate_suggestions(factors)
    intent_results = classify_multi(text)

    return AmbiguityResult(
        score=round(total_score, 2),
        reason=reason,
        suggestions=suggestions,
        top_intents=intent_results[:3],
    )
