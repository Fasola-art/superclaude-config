#!/usr/bin/env python3
"""
Backfill historical Bun crash signatures into error-kb/pending.

Sources:
- ~/.claude/paste-cache/*.txt
- ~/.codex/sessions/**/*.jsonl
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

BUN_MARKERS = (
    "panic(main thread): Segmentation fault",
    "oh no: Bun has crashed",
    "bun.report/",
)


def has_bun_crash(text: str) -> bool:
    return all(m in text for m in BUN_MARKERS[:2]) and BUN_MARKERS[2] in text


def extract_excerpt(text: str) -> str:
    lines = text.splitlines()
    keep = []
    for idx, line in enumerate(lines):
        if "panic(main thread): Segmentation fault" in line:
            start = max(0, idx - 2)
            end = min(len(lines), idx + 10)
            keep = lines[start:end]
            break
    if not keep:
        keep = lines[:20]
    return "\n".join(keep)[:2000]


def collect_sources() -> list[tuple[Path, str]]:
    items: list[tuple[Path, str]] = []
    home = Path.home()

    paste_cache = home / ".claude" / "paste-cache"
    if paste_cache.exists():
        for p in paste_cache.glob("*.txt"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if has_bun_crash(text):
                items.append((p, text))

    codex_sessions = home / ".codex" / "sessions"
    if codex_sessions.exists():
        for p in codex_sessions.rglob("*.jsonl"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if has_bun_crash(text):
                items.append((p, text))
    return items


def write_pending(records: list[tuple[Path, str]]) -> tuple[int, int]:
    pending_dir = Path.home() / ".claude" / "error-kb" / "pending"
    pending_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0
    for src, text in records:
        excerpt = extract_excerpt(text)
        report_url = ""
        for line in text.splitlines():
            if "https://bun.report/" in line:
                m = re.search(r"https://bun\.report/\S+", line)
                if m:
                    report_url = m.group(0)
                else:
                    report_url = "https://bun.report/unknown"
                break
        message = report_url or "bun_canary_segfault"
        eid_seed = f"bun_canary_segfault:{message}".encode("utf-8")
        eid = hashlib.sha1(eid_seed).hexdigest()[:12]
        out = pending_dir / f"{eid}.json"

        if out.exists():
            skipped += 1
            continue

        rec = {
            "id": eid,
            "type": "bun_canary_segfault",
            "tool": "runtime",
            "message": message,
            "exitCode": 139,
            "timestamp": datetime.now().isoformat(),
            "raw_log": excerpt,
            "resolved": False,
            "resolution": None,
            "source": str(src),
        }
        out.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        created += 1

    return created, skipped


def main() -> None:
    records = collect_sources()
    created, skipped = write_pending(records)
    print(
        json.dumps(
            {"status": "ok", "found": len(records), "created": created, "skipped": skipped},
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
