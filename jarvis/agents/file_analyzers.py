#!/usr/bin/env python3
"""
File Analyzers
파일 유형별 분석기 팩토리
"""

from pathlib import Path
from .analyzers import (
    BaseAnalyzer,
    AnalysisResult,
    FrontendAnalyzer,
    BackendAnalyzer,
    ServerAnalyzer,
    APIAnalyzer,
    OtherAnalyzer,
)


def get_analyzers() -> dict[str, BaseAnalyzer]:
    """분석기 딕셔너리 반환"""
    return {
        "frontend": FrontendAnalyzer(),
        "backend": BackendAnalyzer(),
        "server": ServerAnalyzer(),
        "api": APIAnalyzer(),
        "other": OtherAnalyzer(),
    }


def analyze_directory(path: str) -> list[AnalysisResult]:
    """디렉토리 분석"""
    results = []
    path_obj = Path(path)
    analyzers = get_analyzers()

    for file_path in path_obj.rglob("*"):
        if file_path.is_file():
            str_path = str(file_path)

            # 무시 패턴
            if any(p in str_path for p in ["node_modules", ".git", "__pycache__"]):
                continue

            for analyzer in analyzers.values():
                if analyzer.can_analyze(str_path):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        result = analyzer.analyze(str_path, content)
                        if result.issues:
                            results.append(result)
                    except Exception:
                        pass
                    break

    return results
