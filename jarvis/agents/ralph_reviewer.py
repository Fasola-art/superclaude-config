#!/usr/bin/env python3
"""
Ralph Reviewer Agent
리뷰 에이전트
"""

from __future__ import annotations
from typing import Callable, Awaitable

from .base import (
    BaseAgent,
    AgentRole,
    AgentStatus,
    AgentTask,
    AgentResult,
    ReviewFeedback,
)
from .ralph_writer import Draft


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
