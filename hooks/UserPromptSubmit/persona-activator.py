#!/usr/bin/env python3
"""
Persona Auto-Activation Hook (v2.0)
- loader.py + index.json 기반 57개 전체 페르소나 지원
- 카테고리: dev(14), finance(12), education(4), ideation(27)
- 최대 동시 활성화: 8개 (index.json 설정)
"""

import os
import sys
from pathlib import Path

# Windows UTF-8 출력 강제
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PERSONAS_DIR = Path.home() / ".claude" / "personas"
sys.path.insert(0, str(PERSONAS_DIR))

from loader import activate_personas, load_persona


def main() -> None:
    prompt = os.environ.get("PROMPT", "")

    if not prompt and not sys.stdin.isatty():
        prompt = sys.stdin.read()

    if not prompt or len(prompt.strip()) < 3:
        return

    activated = activate_personas(prompt)

    if not activated:
        return

    # 카테고리별 그룹핑하여 출력
    by_cat: dict[str, list[str]] = {}
    for p in activated:
        cat = p.get("category", "etc")
        name = p.get("name", p.get("id", "unknown"))
        by_cat.setdefault(cat, []).append(name)

    parts = []
    for cat, names in by_cat.items():
        parts.append(f"{cat}:[{','.join(names)}]")

    print(f"Personas: {' | '.join(parts)}")


if __name__ == "__main__":
    main()
