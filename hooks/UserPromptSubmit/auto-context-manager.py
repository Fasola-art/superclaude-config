#!/usr/bin/env python3
"""
Auto Context Manager Hook
- 주제 변화 감지 시 /clear 권장
- 컨텍스트 70% 이상 시 /compact 권장
"""

import re
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.home() / ".claude" / "hooks"))
from _shared.hook_utils import get_input_data, load_state, save_state, extract_keywords, jaccard_similarity

HISTORY_SIZE = 5
SIMILARITY_THRESHOLD = 0.08
CONTEXT_THRESHOLD_PERCENT = 70
SESSION_THRESHOLD_MINUTES = 30
STATE_NAME = "context-manager-state"

NEW_FEATURE_PATTERNS = [
    r"새\s*(기능|feature)", r"new\s*feature", r"기능\s*개발",
    r"새로\s*만들", r"처음부터", r"from\s*scratch", r"새\s*프로젝트", r"new\s*project",
]


def estimate_context_usage() -> int:
    """컨텍스트 사용량 추정 (%)"""
    session_dir = Path.home() / ".claude" / "projects"
    if not session_dir.exists():
        return 0
    jsonl_files = list(session_dir.rglob("*.jsonl"))
    if not jsonl_files:
        return 0
    latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
    return min(int(latest.stat().st_size / (1024 * 1024) * 50), 100)


def get_session_duration(state: dict) -> int:
    """세션 경과 시간 (분)"""
    try:
        start = datetime.fromisoformat(state.get("session_start", datetime.now().isoformat()))
        return int((datetime.now() - start).total_seconds() / 60)
    except (ValueError, TypeError):
        return 0


def detect_topic_change(keywords: set, state: dict) -> bool:
    """주제 변화 감지 (Jaccard 유사도 기반)"""
    recent = state.get("recent_keywords", [])
    if len(recent) < 2:
        return False
    topic = set()
    for kw_list in recent[-HISTORY_SIZE:]:
        topic.update(kw_list)
    return jaccard_similarity(keywords, topic) < SIMILARITY_THRESHOLD and len(keywords) >= 2


def main() -> None:
    input_data = get_input_data()
    prompt = input_data.get("prompt", "")
    if not prompt:
        return

    state = load_state(STATE_NAME)
    if not state:
        state = {"session_start": datetime.now().isoformat(), "recent_keywords": []}

    messages = []
    keywords = extract_keywords(prompt)

    # 1. 새 기능 키워드 또는 주제 변화 감지
    is_new = any(re.search(p, prompt, re.IGNORECASE) for p in NEW_FEATURE_PATTERNS)
    if is_new:
        messages.append("New feature keyword → /clear recommended")
        state["session_start"] = datetime.now().isoformat()
        state["recent_keywords"] = []
    elif detect_topic_change(keywords, state):
        messages.append("Topic change detected → /clear recommended")
        state["session_start"] = datetime.now().isoformat()
        state["recent_keywords"] = []

    # 2. 컨텍스트 사용량 체크
    duration = get_session_duration(state)
    usage = estimate_context_usage()
    if duration >= SESSION_THRESHOLD_MINUTES and usage >= CONTEXT_THRESHOLD_PERCENT:
        last = state.get("last_compact_suggestion")
        suggest = True
        if last:
            try:
                if (datetime.now() - datetime.fromisoformat(last)).total_seconds() < 600:
                    suggest = False
            except (ValueError, TypeError):
                pass
        if suggest:
            messages.append(f"CTX:{usage}% ({duration}min) → /compact")
            state["last_compact_suggestion"] = datetime.now().isoformat()

    # 키워드 히스토리 업데이트
    recent = state.get("recent_keywords", [])
    recent.append(list(keywords))
    state["recent_keywords"] = recent[-HISTORY_SIZE:]
    save_state(STATE_NAME, state)

    if messages:
        print(" | ".join(messages))


if __name__ == "__main__":
    main()
