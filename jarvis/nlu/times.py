#!/usr/bin/env python3
"""
시간 엔티티 추출
"""

from __future__ import annotations

from utils.patterns import extract_time_match
from .types import Entity


def extract_times(text: str) -> list[Entity]:
    """시간 엔티티 추출"""
    entities: list[Entity] = []

    # "오전/오후 N시" 패턴
    match = extract_time_match(text)
    if match:
        period = match.group(1)
        hour = int(match.group(2))

        # 오후 변환
        if period == "오후" and hour < 12:
            hour += 12
        elif period == "오전" and hour == 12:
            hour = 0

        entities.append(Entity(
            type="time",
            value=f"{hour:02d}:00",
            start=match.start(),
            end=match.end(),
        ))

    return entities
