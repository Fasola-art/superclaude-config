#!/usr/bin/env python3
"""
File Change Handler
파일 시스템 변경 감지
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from watchdog.events import FileSystemEventHandler, FileSystemEvent  # type: ignore[import]


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
