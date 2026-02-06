#!/usr/bin/env python3
"""
Autonomous Agent: 자율 실행 에이전트
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

from watchdog.observers import Observer  # type: ignore[import]
from watchdog.events import FileSystemEventHandler, FileSystemEvent  # type: ignore[import]

from .base import BaseAgent, AgentRole, AgentStatus, AgentTask, AgentResult
from .analyzers import BaseAnalyzer, AnalysisResult
from .file_analyzers import get_analyzers
from .file_change_handler import FileChangeHandler, FileChange


class AutonomousAgent(BaseAgent):
    """자율 실행 에이전트"""

    def __init__(
        self,
        name: str = "Autonomous",
        watch_paths: list[str] | None = None,
    ) -> None:
        super().__init__(name, AgentRole.EXECUTOR)
        self.watch_paths = watch_paths or ["."]
        self._observer: Observer | None = None  # type: ignore[valid-type]
        self._pending_changes: list[FileChange] = []
        self._analyzers = get_analyzers()

    def start_watching(self) -> None:
        """파일 감시 시작"""
        self._observer = Observer()
        handler = FileChangeHandler(self._on_file_change)

        for path in self.watch_paths:
            self._observer.schedule(handler, path, recursive=True)

        self._observer.start()
        self.status = AgentStatus.WORKING

    def stop_watching(self) -> None:
        """파일 감시 중지"""
        if self._observer:
            self._observer.stop()  # type: ignore[attr-defined]
            self._observer.join()  # type: ignore[attr-defined]
            self._observer = None

        self.status = AgentStatus.IDLE

    def _on_file_change(self, change: FileChange) -> None:
        """파일 변경 콜백"""
        self._pending_changes.append(change)

    async def execute(self, task: AgentTask) -> AgentResult:
        """변경 분석 및 처리"""
        self.status = AgentStatus.WORKING

        if not self._pending_changes:
            return AgentResult(
                task_id=task.id,
                success=True,
                output={"message": "No pending changes"},
            )

        # 대기 중인 변경 처리
        results: list[AnalysisResult] = []
        processed_paths: set[str] = set()

        for change in self._pending_changes:
            if change.path in processed_paths:
                continue

            analysis = await self._analyze_file(change.path)
            if analysis:
                results.append(analysis)
                processed_paths.add(change.path)

        self._pending_changes.clear()
        self.status = AgentStatus.COMPLETED

        return AgentResult(
            task_id=task.id,
            success=True,
            output={
                "analyzed_files": len(results),
                "results": [r.__dict__ for r in results],
                "issues": [r for r in results if r.issues],
            },
        )

    async def _analyze_file(self, file_path: str) -> AnalysisResult | None:
        """파일 분석"""
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return None

        # 적합한 분석기 선택
        for analyzer in self._analyzers.values():
            if analyzer.can_analyze(file_path):
                return analyzer.analyze(file_path, content)

        # 폴백
        return self._analyzers["other"].analyze(file_path, content)

    def can_handle(self, task: AgentTask) -> bool:
        return True
