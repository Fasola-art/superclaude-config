#!/usr/bin/env python3
"""
Ralph preflight guard.

Blocks high-risk Task tool calls while a Ralph guard window is active.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GUARD_FILE = Path.home() / ".claude" / "cache" / "ralph-guard.json"


def _read_stdin_json() -> dict[str, Any]:
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def _load_guard() -> dict[str, Any]:
    try:
        return json.loads(GUARD_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _is_active(guard: dict[str, Any]) -> bool:
    if not guard or not guard.get("active"):
        return False
    try:
        expires_at = datetime.fromisoformat(str(guard.get("expires_at")))
    except Exception:
        return False
    return expires_at > datetime.now(timezone.utc)


def main() -> None:
    payload = _read_stdin_json()
    tool_name = str(payload.get("tool_name", "")).strip()
    if tool_name != "Task":
        return

    guard = _load_guard()
    if not _is_active(guard):
        return

    reason = guard.get("reason", "Ralph guard active")
    expires_at = guard.get("expires_at", "")
    msg = (
        f"Ralph preflight blocked Task call: {reason}. "
        f"Expires: {expires_at}. "
        "Use smaller prompts, reduce parallel agents, then retry after cooldown."
    )
    print(msg)
    sys.exit(2)


if __name__ == "__main__":
    main()
