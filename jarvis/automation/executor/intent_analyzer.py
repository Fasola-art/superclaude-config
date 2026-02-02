#!/usr/bin/env python3
"""
의도 분석 모듈
"""

import re

from .patterns import INTENT_PATTERNS
from .types import IntentResult


def analyze_intent(command: str) -> IntentResult:
    """
    명령어 의도 분석

    Args:
        command: 사용자 명령어

    Returns:
        IntentResult: 분석된 의도 정보
    """
    command_lower = command.lower()

    for intent, pattern_list in INTENT_PATTERNS.items():
        for pattern in pattern_list:
            if re.search(pattern, command_lower):
                return IntentResult(
                    intent=intent,
                    command=command,
                    confidence=0.8,
                )

    return IntentResult(
        intent="unknown",
        command=command,
        confidence=0.0,
    )
