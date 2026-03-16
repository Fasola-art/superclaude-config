#!/usr/bin/env python3
"""
Collect failed tool executions into a JSONL stream for later triage.
Trigger: PostToolUseFailure
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

BUN_MARKERS = (
    "panic(main thread): segmentation fault",
    "oh no: bun has crashed",
    "bun.report/",
    "0xffffffffffffffff",
)


def _read_stdin_json() -> dict[str, Any]:
    try:
        import sys
        raw = sys.stdin.read().strip()
        if not raw:
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def _detect_type(text: str) -> str:
    low = text.lower()
    if any(m in low for m in BUN_MARKERS):
        return "bun_canary_segfault"
    return "tool_failure"


def _error_id(err_type: str, tool: str, text: str) -> str:
    seed = f"{err_type}:{tool}:{text[:500]}".encode("utf-8")
    return hashlib.sha1(seed).hexdigest()[:12]


def main() -> None:
    payload = _read_stdin_json()

    stdout = payload.get("stdout") or os.environ.get("CLAUDE_TOOL_OUTPUT", "")
    stderr = payload.get("stderr") or ""
    combined = f"{stderr}\n{stdout}".strip()
    tool = payload.get("tool") or os.environ.get("TOOL_NAME", "")
    exit_code = payload.get("exitCode") or os.environ.get("EXIT_CODE", "")
    err_type = _detect_type(combined)
    eid = _error_id(err_type, str(tool), combined)

    record = {
        "timestamp": datetime.now().isoformat(),
        "event": "PostToolUseFailure",
        "errorId": eid,
        "errorType": err_type,
        "tool": tool,
        "exitCode": exit_code,
        "command": payload.get("command") or os.environ.get("CLAUDE_TOOL_COMMAND", ""),
        "stderr": stderr,
        "stdout": stdout,
    }

    out_dir = Path.home() / ".claude" / "cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "tool-failures.jsonl"

    with out_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Also mirror into error-kb/pending for unified triage.
    kb_pending = Path.home() / ".claude" / "error-kb" / "pending"
    kb_pending.mkdir(parents=True, exist_ok=True)
    kb_file = kb_pending / f"{eid}.json"
    if not kb_file.exists():
        kb_record = {
            "id": eid,
            "type": err_type,
            "tool": tool,
            "message": (combined.splitlines()[0] if combined else "unknown failure"),
            "exitCode": exit_code,
            "timestamp": datetime.now().isoformat(),
            "raw_log": combined[:2000],
            "resolved": False,
            "resolution": None,
            "source": "PostToolUseFailure/error-collector.py",
        }
        kb_file.write_text(json.dumps(kb_record, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "collected",
                "file": str(out_file),
                "kb_file": str(kb_file),
                "tool": record["tool"],
                "errorType": err_type,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
