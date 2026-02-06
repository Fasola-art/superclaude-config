"""Project monitoring types."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass
class FileInfo:
    """파일 정보."""
    path: Path
    size: int
    modified: float
    file_type: str


@dataclass
class ProjectState:
    """프로젝트 상태."""
    path: Path
    total_files: int
    total_size: int
    file_types: Dict[str, int]
    last_modified: float
