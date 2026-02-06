#!/usr/bin/env python3
"""
코드 분석기 (Frontend, Backend, API)
"""

from __future__ import annotations

import re
from pathlib import Path

from .base import BaseAnalyzer, AnalysisResult


class FrontendAnalyzer(BaseAnalyzer):
    """프론트엔드 분석기"""

    @property
    def category(self) -> str:
        return "frontend"

    def can_analyze(self, file_path: str) -> bool:
        extensions = {".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte"}
        return Path(file_path).suffix in extensions

    def analyze(self, file_path: str, content: str) -> AnalysisResult:
        issues: list[str] = []
        suggestions: list[str] = []

        if "console.log" in content:
            issues.append("console.log 발견 - 프로덕션 코드에서 제거 필요")
            suggestions.append("console.log를 제거하거나 로거로 교체")
        if re.search(r"(TODO|FIXME)", content):
            issues.append("TODO/FIXME 주석 발견")
            suggestions.append("해당 작업 완료 후 주석 제거")
        lines = content.count("\n")
        if lines > 200:
            issues.append(f"컴포넌트 크기 초과: {lines}줄")
            suggestions.append("컴포넌트 분할 권장")
        if re.search(r"from ['\"]@/components['\"]", content):
            issues.append("barrel import 감지 - 번들 크기 증가 위험")
            suggestions.append("직접 import로 변경")

        return self._make_result(file_path, issues, suggestions)


class BackendAnalyzer(BaseAnalyzer):
    """백엔드 분석기"""

    @property
    def category(self) -> str:
        return "backend"

    def can_analyze(self, file_path: str) -> bool:
        path = Path(file_path)
        backend_patterns = ["api", "server", "routes", "controllers", "services"]
        return any(p in str(path).lower() for p in backend_patterns)

    def analyze(self, file_path: str, content: str) -> AnalysisResult:
        issues: list[str] = []
        suggestions: list[str] = []

        if "try" not in content and "catch" not in content:
            if any(kw in content for kw in ["fetch", "async", "await", "axios"]):
                issues.append("비동기 코드에 에러 핸들링 없음")
                suggestions.append("try-catch 블록 추가")

        if re.search(r"(SELECT|INSERT|UPDATE|DELETE).*\+.*\$", content, re.IGNORECASE):
            issues.append("SQL Injection 위험 감지")
            suggestions.append("parameterized query 사용")
            return self._make_result(file_path, issues, suggestions, "error")

        return self._make_result(file_path, issues, suggestions)


class APIAnalyzer(BaseAnalyzer):
    """API 분석기"""

    @property
    def category(self) -> str:
        return "api"

    def can_analyze(self, file_path: str) -> bool:
        api_patterns = ["api", "routes", "endpoints", "handlers"]
        return any(p in str(file_path).lower() for p in api_patterns)

    def analyze(self, file_path: str, content: str) -> AnalysisResult:
        issues: list[str] = []
        suggestions: list[str] = []

        if re.search(r"(GET|POST|PUT|DELETE)", content):
            if "auth" not in content.lower() and "middleware" not in content.lower():
                issues.append("인증 미들웨어 미적용 가능성")
                suggestions.append("인증 확인 미들웨어 추가")
        if "rateLimit" not in content and "throttle" not in content.lower():
            issues.append("Rate limiting 미적용")
            suggestions.append("API rate limiting 추가 권장")

        return self._make_result(file_path, issues, suggestions)
