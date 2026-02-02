#!/usr/bin/env python3
"""
파일 변경 분석기
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


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


class ServerAnalyzer(BaseAnalyzer):
    """서버 설정 분석기"""

    @property
    def category(self) -> str:
        return "server"

    def can_analyze(self, file_path: str) -> bool:
        config_files = {
            "docker-compose.yml",
            "dockerfile",
            "nginx.conf",
            ".env",
            "config.yaml",
        }
        return Path(file_path).name.lower() in config_files

    def analyze(self, file_path: str, content: str) -> AnalysisResult:
        issues: list[str] = []
        suggestions: list[str] = []
        file_name = Path(file_path).name.lower()

        if file_name == ".env" and ("password" in content.lower() or "secret" in content.lower()):
            issues.append("민감 정보가 .env에 하드코딩됨")
            suggestions.append("시크릿 매니저 사용 권장")
        if "dockerfile" in file_name and "root" in content.lower():
            issues.append("컨테이너가 root로 실행될 수 있음")
            suggestions.append("non-root 사용자 설정 추가")

        return self._make_result(file_path, issues, suggestions, "error" if issues else "info")


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


class OtherAnalyzer(BaseAnalyzer):
    """기타 파일 분석기"""

    @property
    def category(self) -> str:
        return "other"

    def can_analyze(self, file_path: str) -> bool:
        return True  # 폴백

    def analyze(self, file_path: str, content: str) -> AnalysisResult:
        issues: list[str] = []
        suggestions: list[str] = []

        if len(content) > 100000:
            issues.append("파일 크기가 너무 큼")
            suggestions.append("파일 분할 고려")

        return self._make_result(file_path, issues, suggestions, "info")
