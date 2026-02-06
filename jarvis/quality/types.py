#!/usr/bin/env python3
"""
Quality 게이트 타입 정의
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class GateStatus(Enum):
    """게이트 실행 상태"""

    PASS = auto()
    FAIL = auto()
    SKIP = auto()
    ERROR = auto()


@dataclass
class CheckResult:
    """개별 검사 결과"""

    name: str
    status: GateStatus
    message: str = ""
    output: str = ""


@dataclass
class GateResult:
    """전체 게이트 실행 결과"""

    file_path: str
    file_type: str
    checks: list[CheckResult] = field(default_factory=list)
    score: float = 0.0

    @property
    def passed(self) -> bool:
        """모든 검사 통과 여부"""
        return self.score >= 0.90

    @property
    def failed_checks(self) -> list[CheckResult]:
        """실패한 검사 목록"""
        return [c for c in self.checks if c.status == GateStatus.FAIL]
