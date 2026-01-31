#!/usr/bin/env python3
"""
컨텍스트 자동 정리 Hook (DCP)
- 컨텍스트 사용량 모니터링
- 임계치 도달 시 자동 정리
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# DCP 임계치
THRESHOLDS = {
    "warning": 75,    # 경고 표시
    "critical": 90,   # 자동 DCP 제안
    "emergency": 95   # 강제 압축
}

# 상태 파일
STATE_FILE = Path.home() / ".claude" / "cache" / "context-state.json"

def get_context_usage() -> int:
    """현재 컨텍스트 사용량 추정 (%)"""
    # 실제로는 Claude API에서 토큰 수를 가져와야 함
    # 여기서는 세션 파일 크기로 추정
    session_dir = Path.home() / ".claude" / "projects"

    if not session_dir.exists():
        return 0

    # 가장 최근 세션 파일
    jsonl_files = list(session_dir.rglob("*.jsonl"))
    if not jsonl_files:
        return 0

    latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
    size_mb = latest.stat().st_size / (1024 * 1024)

    # 대략적인 추정 (200KB = 약 10%)
    estimated_usage = min(int(size_mb * 50), 100)
    return estimated_usage

def check_and_alert():
    """컨텍스트 사용량 확인 및 알림"""
    usage = get_context_usage()

    if usage >= THRESHOLDS["emergency"]:
        print(f"🚨 CTX:{usage}% → /compact 필요")
    elif usage >= THRESHOLDS["critical"]:
        print(f"⚠️ CTX:{usage}%")
    # warning은 출력 생략

    # 상태 저장
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "usage": usage,
        "timestamp": datetime.now().isoformat(),
        "threshold_hit": None
    }

    if usage >= THRESHOLDS["emergency"]:
        state["threshold_hit"] = "emergency"
    elif usage >= THRESHOLDS["critical"]:
        state["threshold_hit"] = "critical"
    elif usage >= THRESHOLDS["warning"]:
        state["threshold_hit"] = "warning"

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

if __name__ == "__main__":
    check_and_alert()
