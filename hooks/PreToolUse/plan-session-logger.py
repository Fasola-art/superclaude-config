#!/usr/bin/env python3
"""Plan Mode 진입 시 세션 자동 기록

Hook Type: PreToolUse
Matcher: EnterPlanMode
목적: plan mode 진입 시 히스토리 자동 기록
출력: 없음 (조용히 기록만)
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

HISTORY_DIR = Path.home() / ".claude" / "history"
SESSIONS_FILE = HISTORY_DIR / "sessions.md"
MAX_ENTRIES = 50


def get_project_name() -> str:
    """현재 디렉토리에서 프로젝트명 추출"""
    cwd = Path(os.getcwd())
    pkg = cwd / "package.json"
    if pkg.exists():
        try:
            return json.loads(pkg.read_text()).get("name", cwd.name)
        except Exception:
            pass
    for marker in ["pyproject.toml", "go.mod", "Cargo.toml"]:
        if (cwd / marker).exists():
            return cwd.name
    return cwd.name


def init_file() -> None:
    """세션 파일 헤더 초기화"""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    if not SESSIONS_FILE.exists():
        SESSIONS_FILE.write_text(
            "# Session History\n\n"
            "| Date             | Project    | Path                | Type      |\n"
            "|------------------|------------|---------------------|-----------|\n"
        )


def append_entry() -> None:
    """세션 기록 1건 추가"""
    init_file()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    project = get_project_name()
    cwd = os.getcwd()
    with open(SESSIONS_FILE, "a") as f:
        f.write(f"| {now} | {project} | {cwd} | plan_mode |\n")
    trim_old()


def trim_old() -> None:
    """MAX_ENTRIES 초과 시 오래된 기록 제거"""
    lines = SESSIONS_FILE.read_text().splitlines()
    header, data = lines[:4], lines[4:]
    if len(data) > MAX_ENTRIES:
        SESSIONS_FILE.write_text(
            "\n".join(header + data[-MAX_ENTRIES:]) + "\n"
        )


def main() -> None:
    """EnterPlanMode 감지 시 세션 기록"""
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        sys.exit(0)
    if input_data.get("tool_name") != "EnterPlanMode":
        sys.exit(0)
    append_entry()
    sys.exit(0)


if __name__ == "__main__":
    main()
