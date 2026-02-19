#!/usr/bin/env python3
"""
Writer-Reviewer Loop activation hook
Trigger: PreToolUse | Matcher: Edit|Write|MultiEdit
"""

import json
import re
import sys
from pathlib import Path

SETTINGS_FILE = Path.home() / ".claude" / "settings.json"

DEFAULT_CONFIG = {
    "targetScore": 0.85,
    "maxIterations": 10,
}

# 코드 타입별 가중치
CODE_WEIGHTS = {
    "frontend": {"quality": 0.25, "security": 0.25, "performance": 0.20, "accessibility": 0.30},
    "backend": {"quality": 0.25, "security": 0.40, "performance": 0.25, "accessibility": 0.10},
    "utility": {"quality": 0.35, "security": 0.25, "performance": 0.30, "accessibility": 0.10},
    "database": {"quality": 0.20, "security": 0.40, "performance": 0.35, "accessibility": 0.05},
}

CODE_PATTERNS = {
    "frontend": (["component", "tsx", "jsx", "ui", "form", "button"], [r"\.tsx$", r"\.jsx$"]),
    "backend": (["api", "route", "endpoint", "controller", "service"], [r"/api/", r"/routes/"]),
    "utility": (["util", "helper", "lib", "function", "hook"], [r"/utils/", r"/lib/"]),
    "database": (["query", "sql", "database", "migration", "schema"], [r"/db/", r"\.sql$"]),
}

SKIP_PATTERNS = ["git", "config", ".md", ".json", ".env", "package.json", ".lock"]


def detect_code_type(file_path: str, content: str = "") -> str:
    """파일 경로와 내용에서 코드 타입 감지"""
    combined = f"{file_path} {content}".lower()
    for code_type, (keywords, patterns) in CODE_PATTERNS.items():
        if any(kw in combined for kw in keywords):
            return code_type
        if any(re.search(p, file_path) for p in patterns):
            return code_type
    return "utility"


def main() -> None:
    try:
        data = json.loads(sys.stdin.read()) if sys.stdin.readable() else {}
    except (json.JSONDecodeError, ValueError):
        data = {}

    file_path = data.get("file_path", data.get("path", ""))

    # 스킵 조건 확인
    if any(skip in file_path.lower() for skip in SKIP_PATTERNS):
        print(json.dumps({"status": "skipped", "message": "config/doc file"}))
        return

    content = data.get("content", data.get("new_string", ""))
    code_type = detect_code_type(file_path, content)
    weights = CODE_WEIGHTS.get(code_type, CODE_WEIGHTS["utility"])

    # 설정 로드
    try:
        settings = json.loads(SETTINGS_FILE.read_text()).get("writerReviewer", DEFAULT_CONFIG)
    except Exception:
        settings = DEFAULT_CONFIG

    output = {
        "status": "enabled",
        "enabled": True,
        "codeType": code_type,
        "weights": weights,
        "targetScore": settings.get("targetScore", 0.85),
        "maxIterations": settings.get("maxIterations", 10),
        "message": f"Writer-Reviewer enabled: {code_type} type",
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
