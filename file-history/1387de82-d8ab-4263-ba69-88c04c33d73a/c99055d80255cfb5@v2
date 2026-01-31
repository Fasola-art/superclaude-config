#!/usr/bin/env python3
"""
Ralph Loop - 에러 자동 해결 Hook
- 에러 감지 시 Error KB 검색
- 유사 에러 해결책 적용
- 최대 10회 자동 재시도
"""

import os
import sys
import json
import hashlib
from pathlib import Path

ERROR_KB_DIR = Path.home() / ".claude" / "error-kb"
RESOLVED_DIR = ERROR_KB_DIR / "resolved"
STATE_FILE = Path.home() / ".claude" / "cache" / "ralph-state.json"

MAX_RETRIES = 10
SIMILARITY_THRESHOLD = 0.70

def jaccard_similarity(str1: str, str2: str) -> float:
    """Jaccard 유사도 계산"""
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())

    if not set1 or not set2:
        return 0.0

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union if union > 0 else 0.0

def search_similar_errors(error_message: str) -> list:
    """유사 에러 검색"""
    if not RESOLVED_DIR.exists():
        return []

    similar = []
    for error_file in RESOLVED_DIR.glob("*.json"):
        try:
            with open(error_file, 'r') as f:
                error_data = json.load(f)

            similarity = jaccard_similarity(error_message, error_data.get("message", ""))

            if similarity >= SIMILARITY_THRESHOLD:
                similar.append({
                    "id": error_data.get("id"),
                    "message": error_data.get("message"),
                    "resolution": error_data.get("resolution"),
                    "similarity": similarity
                })
        except:
            continue

    return sorted(similar, key=lambda x: x["similarity"], reverse=True)

def load_state() -> dict:
    """Ralph Loop 상태 로드"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"retry_count": 0, "last_error": None}

def save_state(state: dict):
    """상태 저장"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def handle_error(error_message: str):
    """에러 처리"""
    state = load_state()

    # 같은 에러인지 확인
    error_hash = hashlib.md5(error_message.encode()).hexdigest()[:12]

    if state.get("last_error") == error_hash:
        state["retry_count"] += 1
    else:
        state["last_error"] = error_hash
        state["retry_count"] = 1

    if state["retry_count"] > MAX_RETRIES:
        print(f"🛑 Ralph:{MAX_RETRIES}회 초과 → 수동 개입")
        state["retry_count"] = 0
        save_state(state)
        return

    similar = search_similar_errors(error_message)
    if similar:
        print(f"🔧 Ralph:{state['retry_count']}/{MAX_RETRIES} 유사도:{similar[0]['similarity']:.0%}")
    else:
        print(f"❓ Ralph:{state['retry_count']}/{MAX_RETRIES} 신규에러")

    save_state(state)

def main():
    # 환경변수에서 에러 정보 가져오기
    tool_result = os.environ.get("TOOL_RESULT", "")
    exit_code = os.environ.get("EXIT_CODE", "0")

    # 에러 감지 (exit code != 0 또는 결과에 error 포함)
    is_error = exit_code != "0" or "error" in tool_result.lower()

    if is_error and tool_result:
        handle_error(tool_result)

if __name__ == "__main__":
    main()
