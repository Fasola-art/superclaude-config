#!/usr/bin/env python3
"""
날짜 엔티티 추출
"""

from __future__ import annotations

from datetime import datetime

from jarvis.utils.datetime_helpers import get_tomorrow_str, get_date_n_days_later, format_datetime, get_next_weekday
from jarvis.utils.patterns import extract_date_match, NEXT_WEEK_PATTERN, WEEKDAY_MAP
from .types import Entity


def extract_dates(text: str) -> list[Entity]:
    """날짜 엔티티 추출"""
    entities: list[Entity] = []
    now = datetime.now()

    # "내일" 패턴
    if "내일" in text:
        entities.append(Entity(type="date", value=get_tomorrow_str()))

    # "모레" 패턴
    if "모레" in text:
        entities.append(Entity(type="date", value=get_date_n_days_later(2)))

    # "다음주 X요일" 패턴
    match = NEXT_WEEK_PATTERN.search(text)
    if match:
        target_weekday = WEEKDAY_MAP.get(match.group(1), 0)
        next_week = get_next_weekday(target_weekday)
        entities.append(Entity(type="date", value=format_datetime(next_week)))

    # "M월 D일" 패턴
    match = extract_date_match(text)
    if match:
        month, day = int(match.group(1)), int(match.group(2))
        year = now.year
        target_date = datetime(year, month, day)
        if target_date < now:
            target_date = datetime(year + 1, month, day)
        entities.append(Entity(
            type="date",
            value=format_datetime(target_date),
            start=match.start(),
            end=match.end(),
        ))

    return entities
