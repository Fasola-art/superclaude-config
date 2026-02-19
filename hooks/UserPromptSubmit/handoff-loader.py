#!/usr/bin/env python3
"""
HANDOFF.md 자동 로드 Hook
- 세션 시작 시 HANDOFF.md가 있으면 컨텍스트로 주입
- 로드 후 handoff-archive/로 이동
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HANDOFF_FILE = Path.home() / ".claude" / "HANDOFF.md"
ARCHIVE_DIR = Path.home() / ".claude" / "handoff-archive"


def main() -> None:
    if not HANDOFF_FILE.exists():
        return

    content = HANDOFF_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return

    # 컨텍스트로 주입
    output = {
        "result": f"[이전 세션 핸드오프]\n{content}",
        "suppressOutput": False,
    }
    print(json.dumps(output))

    # 아카이브로 이동
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = ARCHIVE_DIR / f"HANDOFF_{timestamp}.md"
    shutil.move(str(HANDOFF_FILE), str(archive_path))


if __name__ == "__main__":
    main()
