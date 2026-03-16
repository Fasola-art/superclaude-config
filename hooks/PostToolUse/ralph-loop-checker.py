#!/usr/bin/env python3
"""
Ralph loop checker.

Tracks repeated failures by signature and activates a temporary guard for Task
tool usage when recurrence is high.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

STATE_FILE = Path.home() / ".claude" / "cache" / "ralph-state.json"
GUARD_FILE = Path.home() / ".claude" / "cache" / "ralph-guard.json"

WINDOW_MINUTES = 30
GENERIC_THRESHOLD = 5
BUN_CRASH_THRESHOLD = 2
GUARD_HOURS = 6

BUN_MARKERS = (
    "panic(main thread): segmentation fault",
    "oh no: bun has crashed",
    "bun.report/",
    "0xffffffffffffffff",
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _read_stdin_json() -> dict[str, Any]:
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def _load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _extract_fields(payload: dict[str, Any]) -> tuple[str, int, str]:
    tool_name = (
        str(payload.get("tool") or payload.get("tool_name") or os.environ.get("TOOL_NAME", ""))
        .strip()
    )
    exit_code_raw = payload.get("exitCode")
    if exit_code_raw is None:
        exit_code_raw = payload.get("exit_code")
    if exit_code_raw is None:
        exit_code_raw = os.environ.get("EXIT_CODE", "0")

    try:
        exit_code = int(exit_code_raw)
    except Exception:
        exit_code = 0

    text_parts = [
        str(payload.get("stderr", "")),
        str(payload.get("stdout", "")),
        str(payload.get("output", "")),
        str(os.environ.get("CLAUDE_TOOL_OUTPUT", "")),
    ]
    combined = "\n".join(p for p in text_parts if p).strip()
    return tool_name, exit_code, combined


def _signature(tool_name: str, text: str, is_bun_crash: bool) -> str:
    if is_bun_crash:
        return "bun_canary_segfault"
    base = f"{tool_name}:{text[:400]}".strip()
    if not base:
        base = f"{tool_name}:unknown_failure"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:16]


def _is_bun_crash(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in BUN_MARKERS)


def _activate_guard(reason: str, signature: str, count: int) -> None:
    expires_at = (_now() + timedelta(hours=GUARD_HOURS)).isoformat()
    guard = {
        "active": True,
        "reason": reason,
        "signature": signature,
        "count": count,
        "created_at": _now().isoformat(),
        "expires_at": expires_at,
    }
    _save_json(GUARD_FILE, guard)


def main() -> None:
    payload = _read_stdin_json()
    tool_name, exit_code, output = _extract_fields(payload)

    if exit_code == 0:
        state = _load_json(STATE_FILE, {"events": []})
        cutoff = _now() - timedelta(minutes=WINDOW_MINUTES)
        kept = []
        for ev in state.get("events", []):
            try:
                t = datetime.fromisoformat(ev["time"])
                if t >= cutoff:
                    kept.append(ev)
            except Exception:
                continue
        state["events"] = kept
        _save_json(STATE_FILE, state)
        return

    bun_crash = _is_bun_crash(output)
    sig = _signature(tool_name, output, bun_crash)
    event = {
        "time": _now().isoformat(),
        "tool": tool_name,
        "exit_code": exit_code,
        "signature": sig,
        "bun_crash": bun_crash,
    }

    state = _load_json(STATE_FILE, {"events": []})
    cutoff = _now() - timedelta(minutes=WINDOW_MINUTES)
    events = []
    for ev in state.get("events", []):
        try:
            t = datetime.fromisoformat(ev["time"])
            if t >= cutoff:
                events.append(ev)
        except Exception:
            continue
    events.append(event)
    state["events"] = events
    _save_json(STATE_FILE, state)

    same_sig_count = sum(1 for ev in events if ev.get("signature") == sig)
    threshold = BUN_CRASH_THRESHOLD if bun_crash else GENERIC_THRESHOLD

    if same_sig_count >= threshold:
        reason = "Repeated Bun crash signature" if bun_crash else "Repeated tool failure signature"
        _activate_guard(reason, sig, same_sig_count)
        print(
            f"RalphGuard ON: {reason} ({same_sig_count}/{threshold}). "
            "Task tool will be temporarily gated."
        )
        return

    print(f"Ralph: {same_sig_count}/{threshold} signature={sig}")


if __name__ == "__main__":
    main()
