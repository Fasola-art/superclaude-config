#!/usr/bin/env python3
"""
설정 파일 분석기 (Server, Other)
"""

from __future__ import annotations

from pathlib import Path

from .base import BaseAnalyzer, AnalysisResult


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
