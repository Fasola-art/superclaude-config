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
from .analyzers import (
    BaseAnalyzer,
    AnalysisResult,
    FrontendAnalyzer,
    BackendAnalyzer,
    ServerAnalyzer,
    APIAnalyzer,
    OtherAnalyzer,
)


@dataclass
class FileChange:
    """파일 변경 정보"""

    path: str
    event_type: str  # modified, created, deleted
    timestamp: datetime = field(default_factory=datetime.now)


class FileChangeHandler(FileSystemEventHandler):
    """파일 변경 이벤트 핸들러"""

    def __init__(
        self,
        callback: Callable[[FileChange], None],
        patterns: list[str] | None = None,
        ignore_patterns: list[str] | None = None,
    ) -> None:
        self.callback = callback
        self.patterns = patterns or ["*.py", "*.ts", "*.tsx", "*.js", "*.jsx"]
        self.ignore_patterns = ignore_patterns or [
            "**/node_modules/**",
            "**/.git/**",
            "**/__pycache__/**",
            "**/dist/**",
            "**/build/**",
        ]

    def _should_process(self, path: str) -> bool:
        """처리 여부 확인"""
        from fnmatch import fnmatch

        # 무시 패턴 체크
        for pattern in self.ignore_patterns:
            if fnmatch(path, pattern):
                return False

        # 허용 패턴 체크
        for pattern in self.patterns:
            if fnmatch(path, pattern):
                return True

        return False

    def on_modified(self, event: FileSystemEvent) -> None:  # type: ignore[override]
        if event.is_directory:
            return

        src_path = str(event.src_path)
        if self._should_process(src_path):
            self.callback(FileChange(
                path=src_path,
                event_type="modified",
            ))


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
        self._analyzers: dict[str, BaseAnalyzer] = {
            "frontend": FrontendAnalyzer(),
            "backend": BackendAnalyzer(),
            "server": ServerAnalyzer(),
            "api": APIAnalyzer(),
            "other": OtherAnalyzer(),
        }

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

    def analyze_directory(self, path: str) -> list[AnalysisResult]:
        """디렉토리 분석"""
        results = []
        path_obj = Path(path)

        for file_path in path_obj.rglob("*"):
            if file_path.is_file():
                str_path = str(file_path)

                # 무시 패턴
                if any(p in str_path for p in ["node_modules", ".git", "__pycache__"]):
                    continue

                for analyzer in self._analyzers.values():
                    if analyzer.can_analyze(str_path):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                            result = analyzer.analyze(str_path, content)
                            if result.issues:
                                results.append(result)
                        except Exception:
                            pass
                        break

        return results
