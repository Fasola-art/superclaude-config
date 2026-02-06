#!/usr/bin/env python3
"""
워크플로우 실행 로직
"""

from __future__ import annotations

import asyncio

from .base import AgentTask, AgentResult
from .coordinator_models import Workflow, WorkflowStep


class WorkflowExecutor:
    """워크플로우 실행기"""

    def __init__(
        self,
        agents: dict,
        ralph_loops: dict,
        task_results: dict
    ) -> None:
        self._agents = agents
        self._ralph_loops = ralph_loops
        self._task_results = task_results

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

    async def _execute_step_agent(self, step: WorkflowStep, task: AgentTask) -> AgentResult:
        """에이전트 단계 실행"""
        from .coordinator import AgentCoordinator
        # 순환 import 방지를 위해 동적 import
        coordinator = AgentCoordinator.__new__(AgentCoordinator)
        coordinator._agents = self._agents
        coordinator._ralph_loops = self._ralph_loops
        coordinator._task_results = self._task_results
        return await coordinator.execute_task(step.agent_type, task)

    async def _execute_step_ralph(self, step: WorkflowStep, task: AgentTask) -> AgentResult:
        """Ralph Loop 단계 실행"""
        from .coordinator import AgentCoordinator
        coordinator = AgentCoordinator.__new__(AgentCoordinator)
        coordinator._agents = self._agents
        coordinator._ralph_loops = self._ralph_loops
        coordinator._task_results = self._task_results
        loop_name = step.config.get("loop_name", "default")
        return await coordinator.execute_ralph_loop(loop_name, task)
