#!/usr/bin/env python3
"""
Ralph Loop: Writer-Reviewer 4-Agent Pattern
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from .base import AgentTask, AgentResult, ReviewFeedback
from .ralph_agents import WriterAgent, ReviewerAgent


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
