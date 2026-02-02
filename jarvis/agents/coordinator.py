#!/usr/bin/env python3
"""
에이전트 조율 모듈
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from .base import (
    BaseAgent,
    AgentTask,
    AgentResult,
)
from .ralph_loop import RalphLoop


@dataclass
class WorkflowStep:
    """워크플로우 단계"""

    name: str
    agent_type: str
    config: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)


@dataclass
class Workflow:
    """워크플로우 정의"""

    name: str
    steps: list[WorkflowStep]
    description: str = ""


class AgentCoordinator:
    """에이전트 조율기"""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._ralph_loops: dict[str, RalphLoop] = {}
        self._task_results: dict[str, AgentResult] = {}

    def register_agent(self, name: str, agent: BaseAgent) -> None:
        """에이전트 등록"""
        self._agents[name] = agent

    def register_ralph_loop(
        self,
        name: str,
        ralph_loop: RalphLoop,
    ) -> None:
        """Ralph Loop 등록"""
        self._ralph_loops[name] = ralph_loop

    def get_agent(self, name: str) -> BaseAgent | None:
        """에이전트 조회"""
        return self._agents.get(name)

    async def execute_task(
        self,
        agent_name: str,
        task: AgentTask,
    ) -> AgentResult:
        """단일 에이전트 작업 실행"""
        agent = self._agents.get(agent_name)
        if not agent:
            return AgentResult(
                task_id=task.id,
                success=False,
                output=None,
                errors=[f"Agent not found: {agent_name}"],
            )

        if not agent.can_handle(task):
            return AgentResult(
                task_id=task.id,
                success=False,
                output=None,
                errors=[f"Agent cannot handle task: {agent_name}"],
            )

        result = await agent.execute(task)
        self._task_results[task.id] = result
        return result

    async def execute_ralph_loop(
        self,
        loop_name: str,
        task: AgentTask,
    ) -> AgentResult:
        """Ralph Loop 실행"""
        loop = self._ralph_loops.get(loop_name)
        if not loop:
            return AgentResult(
                task_id=task.id,
                success=False,
                output=None,
                errors=[f"Ralph Loop not found: {loop_name}"],
            )

        result = await loop.execute(task)
        self._task_results[task.id] = result
        return result

    async def execute_workflow(self, workflow: Workflow) -> dict[str, AgentResult]:
        """워크플로우 실행"""
        results: dict[str, AgentResult] = {}
        completed: set[str] = set()

        # 의존성 순서대로 실행
        while len(completed) < len(workflow.steps):
            # 실행 가능한 단계 찾기
            runnable = [
                step for step in workflow.steps
                if step.name not in completed
                and all(dep in completed for dep in step.depends_on)
            ]

            if not runnable:
                # 데드락
                remaining = [s.name for s in workflow.steps if s.name not in completed]
                for name in remaining:
                    results[name] = AgentResult(
                        task_id=name,
                        success=False,
                        output=None,
                        errors=["Workflow deadlock"],
                    )
                break

            # 병렬 실행
            tasks = []
            for step in runnable:
                # 이전 결과 컨텍스트 구성
                context = {
                    dep: results[dep].output
                    for dep in step.depends_on
                    if dep in results
                }

                agent_task = AgentTask(
                    id=step.name,
                    description=step.name,
                    context=context,
                )

                if step.agent_type == "ralph_loop":
                    tasks.append(self._execute_step_ralph(step, agent_task))
                else:
                    tasks.append(self._execute_step_agent(step, agent_task))

            step_results = await asyncio.gather(*tasks)

            for step, result in zip(runnable, step_results):
                results[step.name] = result
                completed.add(step.name)

        return results

    async def _execute_step_agent(
        self,
        step: WorkflowStep,
        task: AgentTask,
    ) -> AgentResult:
        """에이전트 단계 실행"""
        return await self.execute_task(step.agent_type, task)

    async def _execute_step_ralph(
        self,
        step: WorkflowStep,
        task: AgentTask,
    ) -> AgentResult:
        """Ralph Loop 단계 실행"""
        loop_name = step.config.get("loop_name", "default")
        return await self.execute_ralph_loop(loop_name, task)

    def get_status(self) -> dict[str, str]:
        """전체 상태"""
        return {
            name: agent.status.name
            for name, agent in self._agents.items()
        }
