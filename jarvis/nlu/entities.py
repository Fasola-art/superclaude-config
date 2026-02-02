#!/usr/bin/env python3
"""
엔티티 추출 모듈
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta

from .types import Entity


def extract_entities(text: str) -> list[Entity]:
    """
    텍스트에서 엔티티 추출

    Args:
        text: 입력 텍스트

    Returns:
        추출된 엔티티 리스트
    """
    entities: list[Entity] = []

    # 날짜 추출
    entities.extend(_extract_dates(text))

    # 시간 추출
    entities.extend(_extract_times(text))

    # 숫자/ID 추출
    entities.extend(_extract_numbers(text))

    # 따옴표 텍스트 추출
    entities.extend(_extract_quoted_text(text))

    return entities


def _extract_dates(text: str) -> list[Entity]:
    """날짜 추출"""
    entities: list[Entity] = []
    now = datetime.now()

    # "내일" 패턴
    if "내일" in text:
        tomorrow = now + timedelta(days=1)
        entities.append(Entity(
            type="date",
            value=tomorrow.strftime("%Y-%m-%d"),
        ))

    # "모레" 패턴
    if "모레" in text:
        day_after = now + timedelta(days=2)
        entities.append(Entity(
            type="date",
            value=day_after.strftime("%Y-%m-%d"),
        ))

    # "다음주 X요일" 패턴
    weekdays = {
        "월요일": 0, "화요일": 1, "수요일": 2, "목요일": 3,
        "금요일": 4, "토요일": 5, "일요일": 6,
    }
    match = re.search(r"다음\s*주\s*([월화수목금토일]요일)", text)
    if match:
        target_weekday = weekdays.get(match.group(1), 0)
        days_ahead = target_weekday - now.weekday() + 7
        if days_ahead <= 0:
            days_ahead += 7
        next_week = now + timedelta(days=days_ahead)
        entities.append(Entity(
            type="date",
            value=next_week.strftime("%Y-%m-%d"),
        ))

    # "M월 D일" 패턴
    match = re.search(r"(\d{1,2})월\s*(\d{1,2})일", text)
    if match:
        month, day = int(match.group(1)), int(match.group(2))
        year = now.year
        # 과거 날짜면 내년으로
        target_date = datetime(year, month, day)
        if target_date < now:
            target_date = datetime(year + 1, month, day)
        entities.append(Entity(
            type="date",
            value=target_date.strftime("%Y-%m-%d"),
            start=match.start(),
            end=match.end(),
        ))

    return entities


def _extract_times(text: str) -> list[Entity]:
    """시간 추출"""
    entities: list[Entity] = []

    # "오전/오후 N시" 패턴
    match = re.search(r"(오전|오후)?\s*(\d{1,2})\s*시", text)
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


def _extract_numbers(text: str) -> list[Entity]:
    """숫자/ID 추출"""
    entities: list[Entity] = []

    # "N번 작업" 패턴 (task_id)
    match = re.search(r"(\d+)\s*번?\s*(작업|태스크|task)", text)
    if match:
        entities.append(Entity(
            type="task_id",
            value=int(match.group(1)),
            start=match.start(),
            end=match.end(),
        ))
        return entities  # task_id가 있으면 number는 추출하지 않음

    # "N명" 패턴
    match = re.search(r"(\d+)\s*명", text)
    if match:
        entities.append(Entity(
            type="number",
            value=int(match.group(1)),
            start=match.start(),
            end=match.end(),
        ))

    return entities


def _extract_quoted_text(text: str) -> list[Entity]:
    """따옴표 텍스트 추출"""
    entities: list[Entity] = []

    # 큰따옴표 또는 작은따옴표
    match = re.search(r'["\'](.+?)["\']', text)
    if match:
        entities.append(Entity(
            type="title",
            value=match.group(1),
            start=match.start(),
            end=match.end(),
        ))

    return entities
