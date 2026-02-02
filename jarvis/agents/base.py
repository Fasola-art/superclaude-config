#!/usr/bin/env python3
"""
Agent 기본 추상 클래스
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Generic, TypeVar


class AgentRole(Enum):
    """에이전트 역할"""

    WRITER = auto()      # 코드/문서 작성
    REVIEWER = auto()    # 검토
    EXECUTOR = auto()    # 실행
    COORDINATOR = auto() # 조율


class AgentStatus(Enum):
    """에이전트 상태"""

    IDLE = auto()
    WORKING = auto()
    WAITING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class AgentTask:
    """에이전트 작업"""

    id: str
    description: str
    context: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentResult:
    """에이전트 실행 결과"""

    task_id: str
    success: bool
    output: Any
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


T = TypeVar("T")


class BaseAgent(ABC, Generic[T]):
    """에이전트 기본 클래스"""

    def __init__(self, name: str, role: AgentRole) -> None:
        self.name = name
        self.role = role
        self.status = AgentStatus.IDLE
        self._task_history: list[AgentResult] = []

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """작업 실행"""
        pass

    @abstractmethod
    def can_handle(self, task: AgentTask) -> bool:
        """작업 처리 가능 여부"""
        pass

    def get_history(self, limit: int = 10) -> list[AgentResult]:
        """작업 이력"""
        return self._task_history[-limit:]

    def _record_result(self, result: AgentResult) -> None:
        """결과 기록"""
        self._task_history.append(result)


class ReviewFeedback:
    """리뷰 피드백"""

    def __init__(
        self,
        reviewer: str,
        approved: bool,
        comments: list[str] | None = None,
        suggestions: list[str] | None = None,
    ) -> None:
        self.reviewer = reviewer
        self.approved = approved
        self.comments = comments or []
        self.suggestions = suggestions or []

    @property
    def has_issues(self) -> bool:
        """이슈 존재 여부"""
        return not self.approved or bool(self.comments)
