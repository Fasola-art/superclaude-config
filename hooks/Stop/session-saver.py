#!/usr/bin/env python3
"""Session End State Saver + HANDOFF.md Generator"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.home() / ".claude" / "hooks"))
from _shared.hook_utils import get_todo_title

CLAUDE_DIR = Path.home() / ".claude"
SESSION_STATE_DIR = CLAUDE_DIR / "session-env"
TODO_FILE = CLAUDE_DIR / "todos" / "active.json"
HANDOFF_FILE = CLAUDE_DIR / "HANDOFF.md"


def run_git(cmd: str) -> str:
    """Git 명령 실행, 실패 시 빈 문자열 반환"""
    try:
        r = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def get_incomplete_todos() -> list[dict]:
    """미완료 TODO 항목 로드"""
    if not TODO_FILE.exists():
        return []
    try:
        todos = json.loads(TODO_FILE.read_text()).get("todos", [])
        return [t for t in todos if t.get("status") != "completed"]
    except Exception:
        return []


def generate_handoff(state: dict) -> None:
    """HANDOFF.md 마크다운 생성"""
    now = datetime.now()
    branch = run_git("git branch --show-current") or "N/A"
    commit_h = run_git("git rev-parse --short HEAD")
    commit_m = run_git("git log -1 --format=%s")
    changed = set()
    for cmd in ("git diff --name-only", "git diff --cached --name-only"):
        out = run_git(cmd)
        if out:
            changed.update(out.split("\n"))

    lines = [
        f"# Session Handoff — {now.strftime('%Y-%m-%d %H:%M')}",
        "", "## 작업 상태",
        f"- **Branch**: {branch}",
        f"- **Last Commit**: {commit_h} — {commit_m}" if commit_h else "- **Last Commit**: N/A",
        f"- **CWD**: {state.get('cwd', 'N/A')}",
    ]

    if changed:
        files = sorted(changed)[:10]
        lines.append(f"- **Working Files** ({len(changed)}):")
        lines.extend(f"  - `{f}`" for f in files)
        if len(changed) > 10:
            lines.append(f"  - ... +{len(changed) - 10} more")

    todos = state.get("incomplete_todos", [])
    if todos:
        lines.extend(["", "## 미완료 작업"])
        for t in todos[:10]:
            icon = "🔄" if t.get("status") == "in_progress" else "⬜"
            lines.append(f"- {icon} {get_todo_title(t)}")

    lines.extend(["", "## 다음 단계", "- `cc` (--continue) 또는 `cr` (--resume)로 재개"])
    HANDOFF_FILE.write_text("\n".join(lines) + "\n")


def save_session_state() -> None:
    """세션 상태 저장 + HANDOFF.md 생성"""
    SESSION_STATE_DIR.mkdir(parents=True, exist_ok=True)

    state = {
        "ended_at": datetime.now().isoformat(),
        "cwd": os.getcwd(),
        "incomplete_todos": get_incomplete_todos(),
        "last_tool": os.environ.get("LAST_TOOL", ""),
        "context_usage": os.environ.get("CONTEXT_USAGE", "unknown"),
    }

    # last-session.json 저장
    session_file = SESSION_STATE_DIR / "last-session.json"
    with open(session_file, "w") as f:
        json.dump(state, f, indent=2)

    # HANDOFF.md 생성
    generate_handoff(state)

    # 요약 출력
    todo_count = len(state["incomplete_todos"])
    if todo_count:
        print(f"\nSession saved | {todo_count} incomplete tasks | HANDOFF.md generated")


def main() -> None:
    save_session_state()


if __name__ == "__main__":
    main()
