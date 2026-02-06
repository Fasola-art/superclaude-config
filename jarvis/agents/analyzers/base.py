#!/usr/bin/env python3
"""
분석기 기본 클래스
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class AnalysisResult:
    """분석 결과"""

    category: str
    file_path: str
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    auto_fixable: bool = False
    fix_commands: list[str] = field(default_factory=list)
    severity: str = "info"  # info, warning, error


class BaseAnalyzer(ABC):
    """분석기 기본 클래스"""

    @property
    @abstractmethod
    def category(self) -> str:
        """분석 카테고리"""
        pass

    @abstractmethod
    def can_analyze(self, file_path: str) -> bool:
        """분석 가능 여부"""
        pass

    @abstractmethod
    def analyze(self, file_path: str, content: str) -> AnalysisResult:
        """파일 분석"""
        pass

    def _make_result(
        self, file_path: str, issues: list[str], suggestions: list[str],
        severity: str | None = None, fix_commands: list[str] | None = None
    ) -> AnalysisResult:
        """분석 결과 생성 헬퍼"""
        return AnalysisResult(
            category=self.category,
            file_path=file_path,
            issues=issues,
            suggestions=suggestions,
            severity=severity or ("warning" if issues else "info"),
            auto_fixable=bool(fix_commands),
            fix_commands=fix_commands or [],
        )
