#!/usr/bin/env python3
"""
Rollback Guard Hook (PreToolUse)
- Git 저장소에서 파괴적 명령 전 자동 스냅샷 생성
- 비-Git 디렉토리에서는 스킵
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROLLBACK_DIR = Path.home() / ".claude" / "rollback"
SNAPSHOT_LOG = ROLLBACK_DIR / "sessions.jsonl"
DESTRUCTIVE_PATTERNS = [
    "rm ", "rm\t", "rmdir", "git reset", "git checkout -- ",
    "git clean", "git rebase", "git merge", "drop ", "truncate ",
    "delete from", "mv ", "cp ",
]


def is_destructive(command: str) -> bool:
    """파괴적 명령어 여부 판단"""
    return any(pat in command.lower().strip() for pat in DESTRUCTIVE_PATTERNS)


def get_git_root() -> str | None:
    """현재 디렉토리의 git root 반환"""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def create_snapshot(reason: str) -> str | None:
    """Git 태그 기반 스냅샷 생성"""
    git_root = get_git_root()
    if not git_root:
        return None

    sid = f"auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    tag = f"rollback/{sid}"
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=git_root, timeout=5,
        )
        commit = r.stdout.strip()
        subprocess.run(["git", "tag", tag, commit], capture_output=True, cwd=git_root, timeout=5)

        ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
        entry = {
            "id": sid, "tag": tag, "commit": commit,
            "cwd": os.getcwd(), "time": datetime.now(timezone.utc).isoformat(),
            "reason": reason[:60],
        }
        with open(SNAPSHOT_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return sid
    except Exception:
        return None


def cleanup_old_tags(max_tags: int = 50) -> None:
    """오래된 롤백 태그 정리"""
    git_root = get_git_root()
    if not git_root:
        return
    try:
        r = subprocess.run(
            ["git", "tag", "-l", "rollback/auto-*"],
            capture_output=True, text=True, cwd=git_root, timeout=5,
        )
        tags = sorted(r.stdout.strip().split("\n"))
        for old in tags[:-max_tags] if len(tags) > max_tags else []:
            subprocess.run(["git", "tag", "-d", old], capture_output=True, cwd=git_root, timeout=5)
    except Exception:
        pass


def main() -> None:
    tool_input = os.environ.get("TOOL_INPUT", "{}")
    try:
        data = json.loads(tool_input)
    except json.JSONDecodeError:
        return

    tool_name = os.environ.get("TOOL_NAME", "")

    if tool_name == "Bash":
        command = data.get("command", "")
        if is_destructive(command):
            if create_snapshot(command[:80]):
                cleanup_old_tags()
    elif tool_name in ("Write", "Edit", "MultiEdit"):
        fp = data.get("file_path", "")
        if fp and os.path.exists(fp):
            create_snapshot(f"{tool_name}: {fp}")


if __name__ == "__main__":
    main()
