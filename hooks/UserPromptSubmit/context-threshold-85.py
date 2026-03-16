#!/usr/bin/env python3
"""
컨텍스트 85% 임계값 훅
- 70% 훅(auto-context-manager.py)이 경고만 한다면 이 훅은 /handoff 실행 권장
- 기존 훅과 충돌 없음 (다른 임계값, 다른 액션)
"""

import json
import os
import sys
from pathlib import Path

CLAUDE_DIR = Path("C:/Users/MSI/.claude")
THRESHOLD_85 = 85
JSONL_SIZE_PER_PCT = 1024 * 1024 / 50  # 1MB ≈ 50% (추정)


def estimate_context_pct() -> int:
    """JSONL 파일 크기로 컨텍스트 사용량 추정"""
    projects_dir = CLAUDE_DIR / "projects"
    if not projects_dir.exists():
        return 0

    files = list(projects_dir.rglob("*.jsonl"))
    if not files:
        return 0

    latest = max(files, key=lambda f: f.stat().st_mtime)
    size_bytes = latest.stat().st_size
    pct = int(size_bytes / JSONL_SIZE_PER_PCT)
    return min(pct, 100)


def main() -> None:
    # stdin에서 훅 입력 읽기 (Claude Code 훅 프로토콜)
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    ctx_pct = estimate_context_pct()

    if ctx_pct >= THRESHOLD_85:
        warning = {
            "type": "warning",
            "message": (
                f"⚠️  컨텍스트 {ctx_pct}% 도달 (임계값: {THRESHOLD_85}%)\n"
                f"권장 조치:\n"
                f"  1. /handoff  → 인수인계 문서 생성 후 세션 종료\n"
                f"  2. /half-clone → 핵심 추출 후 /compact\n"
                f"  3. 계속 진행 → 품질 저하 위험"
            )
        }
        # Claude Code 훅은 stdout에 JSON 출력으로 메시지 전달
        print(json.dumps(warning, ensure_ascii=False))


if __name__ == "__main__":
    main()
