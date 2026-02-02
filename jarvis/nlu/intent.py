#!/usr/bin/env python3
"""
의도 분류 모듈
"""

from __future__ import annotations

import re
from typing import Tuple

from .types import Intent


# 의도별 패턴 (우선순위 순)
INTENT_PATTERNS: dict[Intent, list[str]] = {
    Intent.ADD_TASK: [
        r"할\s*일.*추가",
        r"작업.*추가",
        r"todo.*add",
        r"task.*create",
    ],
    Intent.LIST_TASKS: [
        r"할\s*일.*보여",
        r"작업.*목록",
        r"todo.*list",
        r"tasks?.*show",
    ],
    Intent.COMPLETE_TASK: [
        r"완료.*표시",
        r"(\d+)\s*번?.*완료",
        r"끝났",
        r"done",
        r"complete",
    ],
    Intent.ADD_EVENT: [
        r"일정.*추가",
        r"약속.*잡",
        r"미팅.*예약",
        r"event.*add",
    ],
    Intent.LIST_EVENTS: [
        r"일정.*보여",
        r"오늘.*일정",
        r"스케줄",
        r"calendar",
    ],
    Intent.REMEMBER: [
        r"기억해",
        r"저장해",
        r"컨텍스트.*저장",
        r"remember",
    ],
    Intent.RECALL: [
        r"어디까지",
        r"마지막.*작업",
        r"이어서",
        r"recall",
        r"continue.*work",
    ],
    Intent.BOOKING: [
        r"예약",
        r"예매",
        r"book",
        r"reservation",
    ],
    Intent.PLANNING: [
        r"계획.*짜",
        r"플랜",
        r"plan",
        r"일정.*짜",
    ],
}


def classify_intent(text: str) -> Tuple[Intent, float]:
    """
    텍스트에서 의도 분류

    Args:
        text: 입력 텍스트

    Returns:
        (Intent, 신뢰도) 튜플
    """
    text_lower = text.lower()

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return intent, 0.85

    return Intent.UNKNOWN, 0.0
