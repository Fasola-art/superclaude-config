#!/usr/bin/env python3
"""
숫자/텍스트 엔티티 추출
"""

from __future__ import annotations

import re

from .types import Entity


def extract_numbers(text: str) -> list[Entity]:
    """숫자/ID 엔티티 추출"""
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
        return entities

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


def extract_quoted_text(text: str) -> list[Entity]:
    """따옴표 텍스트 추출"""
    entities: list[Entity] = []

    match = re.search(r'["\'](.+?)["\']', text)
    if match:
        entities.append(Entity(
            type="title",
            value=match.group(1),
            start=match.start(),
            end=match.end(),
        ))

    return entities
