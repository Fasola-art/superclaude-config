#!/usr/bin/env python3
"""
Ralph Loop: Writer-Reviewer 4-Agent Pattern
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable

from .base import (
    BaseAgent,
    AgentRole,
    AgentStatus,
    AgentTask,
    AgentResult,
    ReviewFeedback,
)


@dataclass
class Draft:
    """작성된 초안"""

    content: Any
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RalphLoopConfig:
    """Ralph Loop 설정"""

    max_iterations: int = 3  # 최대 반복 횟수
    min_approvals: int = 3   # 필요한 최소 승인 수 (4명 중)
    timeout: float = 60.0    # 타임아웃 (초)


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


class ReviewerAgent(BaseAgent):
    """Reviewer 에이전트"""

    def __init__(
        self,
        name: str,
        review_fn: Callable[[Draft], Awaitable[ReviewFeedback]] | None = None,
    ) -> None:
        super().__init__(name, AgentRole.REVIEWER)
        self._review_fn = review_fn

    async def execute(self, task: AgentTask) -> AgentResult:
        """리뷰는 review 메서드로"""
        return AgentResult(
            task_id=task.id,
            success=False,
            output=None,
            errors=["Use review() method instead"],
        )

    async def review(self, draft: Draft) -> ReviewFeedback:
        """초안 리뷰"""
        self.status = AgentStatus.WORKING

        if self._review_fn:
            feedback = await self._review_fn(draft)
        else:
            feedback = await self._default_review(draft)

        self.status = AgentStatus.COMPLETED
        return feedback

    async def _default_review(self, draft: Draft) -> ReviewFeedback:
        """기본 리뷰 로직 (항상 승인)"""
        return ReviewFeedback(
            reviewer=self.name,
            approved=True,
            comments=[],
        )

    def can_handle(self, task: AgentTask) -> bool:
        return True


class RalphLoop:
    """4-Agent Parallel Review Pattern"""

    def __init__(
        self,
        writer: WriterAgent | None = None,
        reviewers: list[ReviewerAgent] | None = None,
        config: RalphLoopConfig | None = None,
    ) -> None:
        self.writer = writer or WriterAgent()
        self.reviewers = reviewers or [
            ReviewerAgent(f"Reviewer-{i+1}") for i in range(4)
        ]
        self.config = config or RalphLoopConfig()
        self._iteration = 0

    async def execute(self, task: AgentTask) -> AgentResult:
        """Ralph Loop 실행"""
        self._iteration = 0

        # 초안 생성
        draft_result = await self.writer.execute(task)
        if not draft_result.success:
            return draft_result

        draft = draft_result.output

        # 반복 리뷰/수정
        while self._iteration < self.config.max_iterations:
            self._iteration += 1

            # 병렬 리뷰
            reviews = await asyncio.gather(*[
                r.review(draft) for r in self.reviewers
            ])

            # 승인 확인
            approvals = sum(1 for r in reviews if r.approved)
            if approvals >= self.config.min_approvals:
                return AgentResult(
                    task_id=task.id,
                    success=True,
                    output=draft.content,
                    metadata={
                        "iterations": self._iteration,
                        "final_approvals": approvals,
                        "final_version": draft.version,
                    },
                )

            # 수정 필요
            draft = await self.writer.revise(draft, reviews)

        # 최대 반복 도달
        return AgentResult(
            task_id=task.id,
            success=False,
            output=draft.content,
            errors=["Max iterations reached without approval"],
            metadata={
                "iterations": self._iteration,
                "final_version": draft.version,
            },
        )

    @property
    def iteration_count(self) -> int:
        """현재 반복 횟수"""
        return self._iteration
