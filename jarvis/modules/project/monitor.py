"""Project monitoring module."""

from pathlib import Path
from typing import Dict, Optional
from collections import defaultdict

from .scanner import ProjectScanner
from .types import ProjectState, FileInfo


class ProjectMonitor:
    """프로젝트 모니터링."""

    def __init__(self):
        self.scanner = ProjectScanner()
        self._states: Dict[Path, ProjectState] = {}
        self._file_cache: Dict[Path, list[FileInfo]] = {}

    def scan_project(self, path: str | Path) -> ProjectState:
        """프로젝트 구조 스캔."""
        project_path = Path(path).resolve()

        if not project_path.exists():
            raise FileNotFoundError(f"프로젝트 경로가 존재하지 않습니다: {project_path}")

        # 파일 스캔
        files = self.scanner.scan(project_path)
        self._file_cache[project_path] = files

        # 통계 계산
        total_size = sum(f.size for f in files)
        file_types = defaultdict(int)
        for f in files:
            file_types[f.file_type] += 1

        last_modified = max((f.modified for f in files), default=0.0)

        # 상태 생성
        state = ProjectState(
            path=project_path,
            total_files=len(files),
            total_size=total_size,
            file_types=dict(file_types),
            last_modified=last_modified
        )

        self._states[project_path] = state
        return state

    def get_status(self, path: str | Path) -> Optional[ProjectState]:
        """현재 상태 조회."""
        project_path = Path(path).resolve()
        return self._states.get(project_path)

    def detect_changes(self, path: str | Path) -> Dict[str, int]:
        """변경사항 감지."""
        project_path = Path(path).resolve()

        # 이전 상태 확인
        old_state = self._states.get(project_path)
        if not old_state:
            raise ValueError(f"이전 스캔 기록이 없습니다: {project_path}")

        # 이전 파일 목록 저장
        old_files = {f.path: f for f in self._file_cache.get(project_path, [])}

        # 새로운 스캔
        new_files = self.scanner.scan(project_path)
        new_files_dict = {f.path: f for f in new_files}

        # 변경사항 계산
        added = len(new_files_dict.keys() - old_files.keys())
        removed = len(old_files.keys() - new_files_dict.keys())
        modified = sum(
            1 for fpath, old_file in old_files.items()
            if fpath in new_files_dict and new_files_dict[fpath].modified > old_file.modified
        )

        # 상태 및 캐시 업데이트
        new_state = self.scan_project(project_path)

        return {
            'added': added,
            'removed': removed,
            'modified': modified,
            'total_files': new_state.total_files,
            'size_change': new_state.total_size - old_state.total_size
        }

    def get_file_type_stats(self, path: str | Path) -> Dict[str, int]:
        """파일 타입별 통계."""
        state = self.get_status(path)
        return state.file_types if state else {}
