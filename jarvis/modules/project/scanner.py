"""Project file system scanner."""

import os
from pathlib import Path
from typing import List, Set
from .types import FileInfo


DEFAULT_IGNORE = {
    '.git', '__pycache__', 'node_modules', '.venv', 'venv',
    '.pytest_cache', '.mypy_cache', '.ruff_cache',
    'dist', 'build', '*.pyc', '.DS_Store'
}


class ProjectScanner:
    """프로젝트 파일 시스템 스캐너."""

    def __init__(self, ignore_patterns: Set[str] | None = None):
        self.ignore_patterns = ignore_patterns or DEFAULT_IGNORE
        self._gitignore_patterns: Set[str] = set()

    def scan(self, project_path: Path) -> List[FileInfo]:
        """프로젝트 스캔."""
        self._load_gitignore(project_path)
        files = []

        for root, dirs, filenames in os.walk(project_path):
            # 무시할 디렉토리 제거
            dirs[:] = [d for d in dirs if not self._should_ignore(d)]

            for filename in filenames:
                if self._should_ignore(filename):
                    continue

                filepath = Path(root) / filename
                try:
                    stat = filepath.stat()
                    files.append(FileInfo(
                        path=filepath,
                        size=stat.st_size,
                        modified=stat.st_mtime,
                        file_type=filepath.suffix or 'no_ext'
                    ))
                except (OSError, PermissionError):
                    continue

        return files

    def _load_gitignore(self, project_path: Path) -> None:
        """gitignore 로드."""
        gitignore = project_path / '.gitignore'
        if gitignore.exists():
            try:
                content = gitignore.read_text()
                self._gitignore_patterns = {
                    line.strip() for line in content.splitlines()
                    if line.strip() and not line.startswith('#')
                }
            except (OSError, UnicodeDecodeError):
                pass

    def _should_ignore(self, name: str) -> bool:
        """무시 여부 확인."""
        if name in self.ignore_patterns:
            return True
        if name in self._gitignore_patterns:
            return True
        # 패턴 매칭
        for pattern in self.ignore_patterns | self._gitignore_patterns:
            if pattern.startswith('*') and name.endswith(pattern[1:]):
                return True
            # 디렉토리 패턴 (trailing slash)
            if pattern.endswith('/') and name == pattern[:-1]:
                return True
        return False
