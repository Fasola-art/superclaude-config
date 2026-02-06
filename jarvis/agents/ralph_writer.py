#!/usr/bin/env python3
"""
Ralph Writer Agent
초안 생성 및 수정 에이전트
"""

from __future__ import annotations
from typing import Any, Callable, Awaitable

from .base import (
    BaseAgent,
    AgentRole,
    AgentStatus,
    AgentTask,
    AgentResult,
    ReviewFeedback,
)


class Draft:
    """초안 클래스"""
    def __init__(self, content: Any, version: int = 1, metadata: dict | None = None):
        self.content = content
        self.version = version
        self.metadata = metadata or {}


class WriterAgent(BaseAgent):
    """Writer 에이전트"""

    def __init__(
        self,
        name: str = "Writer",
        generator: Callable[[AgentTask], Awaitable[Any]] | None = None,
        reviser: Callable[[Any, list[ReviewFeedback]], Awaitable[Any]] | None = None,
    ) -> None:
        super().__init__(name, AgentRole.WRITER)
        self._generator = generator
        self._reviser = reviser

    async def execute(self, task: AgentTask) -> AgentResult:
        """초안 생성"""
        self.status = AgentStatus.WORKING

        try:
            if self._generator:
                output = await self._generator(task)
            else:
                output = await self._default_generate(task)

            self.status = AgentStatus.COMPLETED
            result = AgentResult(
                task_id=task.id,
                success=True,
                output=Draft(content=output),
            )
            self._record_result(result)
            return result

        except Exception as e:
            self.status = AgentStatus.FAILED
            return AgentResult(
                task_id=task.id,
                success=False,
                output=None,
                errors=[str(e)],
            )

    async def revise(self, draft: Draft, feedbacks: list[ReviewFeedback]) -> Draft:
        """피드백 기반 수정"""
        self.status = AgentStatus.WORKING

        if self._reviser:
            revised_content = await self._reviser(draft.content, feedbacks)
        else:
            revised_content = await self._default_revise(draft, feedbacks)

        self.status = AgentStatus.COMPLETED
        return Draft(
            content=revised_content,
            version=draft.version + 1,
            metadata={"previous_version": draft.version},
        )

    async def _default_generate(self, task: AgentTask) -> Any:
        """기본 생성 로직"""
        return {"task": task.description, "generated": True}

    async def _default_revise(
        self,
        draft: Draft,
        feedbacks: list[ReviewFeedback],
    ) -> Any:
        """기본 수정 로직"""
        suggestions = []
        for fb in feedbacks:
            suggestions.extend(fb.suggestions)
        return {
            **draft.content,
            "revised": True,
            "applied_suggestions": suggestions,
        }

    def can_handle(self, task: AgentTask) -> bool:
        return True
