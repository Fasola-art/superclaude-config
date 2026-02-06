#!/usr/bin/env python3
"""
NLU 타입 정의
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class Intent(Enum):
    """의도 유형"""

    ADD_TASK = auto()
    LIST_TASKS = auto()
    COMPLETE_TASK = auto()
    ADD_EVENT = auto()
    LIST_EVENTS = auto()
    REMEMBER = auto()
    RECALL = auto()
    BOOKING = auto()
    PLANNING = auto()
    UNKNOWN = auto()


@dataclass
class Entity:
    """추출된 엔티티"""

    type: str  # date, time, number, title, task_id 등
    value: Any
    start: int = 0  # 원본 텍스트 내 시작 위치
    end: int = 0  # 원본 텍스트 내 끝 위치


@dataclass
class ParseResult:
    """파싱 결과"""

    intent: Intent
    entities: list[Entity] = field(default_factory=list)
    confidence: float = 0.0
    raw_text: str = ""

    def get_entity(self, entity_type: str) -> Any | None:
        """특정 타입의 엔티티 값 반환"""
        for entity in self.entities:
            if entity.type == entity_type:
                return entity.value
        return None

    def get_entities(self, entity_type: str) -> list[Any]:
        """특정 타입의 모든 엔티티 값 반환"""
        return [e.value for e in self.entities if e.type == entity_type]


@dataclass
class IntentScore:
    """Intent 매칭 결과 (점수 포함)"""

    intent: Intent
    score: float
    matched_patterns: list[str] = field(default_factory=list)


@dataclass
class AmbiguityResult:
    """모호성 분석 결과"""

    score: float  # 0.0 (명확) ~ 1.0 (매우 모호)
    reason: str
    suggestions: list[str] = field(default_factory=list)
    top_intents: list[IntentScore] = field(default_factory=list)
