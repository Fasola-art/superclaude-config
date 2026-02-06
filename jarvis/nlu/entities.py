#!/usr/bin/env python3
"""
엔티티 추출 메인 모듈
"""

from __future__ import annotations

from .dates import extract_dates
from .numbers import extract_numbers, extract_quoted_text
from .times import extract_times
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

    entities.extend(extract_dates(text))
    entities.extend(extract_times(text))
    entities.extend(extract_numbers(text))
    entities.extend(extract_quoted_text(text))

    return entities
