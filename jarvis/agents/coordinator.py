#!/usr/bin/env python3
"""
에이전트 조율 모듈
"""

from __future__ import annotations

from .base import BaseAgent, AgentTask, AgentResult
from .ralph_loop import RalphLoop
from .coordinator_models import Workflow
from .coordinator_execution import WorkflowExecutor


class AgentCoordinator:
    """에이전트 조율기"""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._ralph_loops: dict[str, RalphLoop] = {}
        self._task_results: dict[str, AgentResult] = {}

    def register_agent(self, name: str, agent: BaseAgent) -> None:
        """에이전트 등록"""
        self._agents[name] = agent

    def register_ralph_loop(self, name: str, ralph_loop: RalphLoop) -> None:
        """Ralph Loop 등록"""
        self._ralph_loops[name] = ralph_loop

    def get_agent(self, name: str) -> BaseAgent | None:
        """에이전트 조회"""
        return self._agents.get(name)

    async def execute_task(self, agent_name: str, task: AgentTask) -> AgentResult:
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

    async def execute_ralph_loop(self, loop_name: str, task: AgentTask) -> AgentResult:
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
        executor = WorkflowExecutor(self._agents, self._ralph_loops, self._task_results)
        return await executor.execute_workflow(workflow)

    def get_status(self) -> dict[str, str]:
        """전체 상태"""
        return {
            name: agent.status.name
            for name, agent in self._agents.items()
        }
