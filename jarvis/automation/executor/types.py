#!/usr/bin/env python3
"""
TaskExecutor 타입 정의
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IntentResult:
    """의도 분석 결과"""
    intent: str
    command: str
    confidence: float


@dataclass
class ExecuteResult:
    """실행 결과"""
    success: bool
    message: str
    data: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """딕셔너리로 변환"""
        result = {"success": self.success, "message": self.message}
        if self.data:
            result.update(self.data)
        return result
