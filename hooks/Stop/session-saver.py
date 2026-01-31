#!/usr/bin/env python3
"""
세션 종료 시 상태 저장 Hook
- 미완료 Todo 저장
- 세션 상태 저장
- 복구 정보 기록
"""

import os
import json
from pathlib import Path
from datetime import datetime

SESSION_STATE_DIR = Path.home() / ".claude" / "session-env"
TODO_FILE = Path.home() / ".claude" / "todos" / "active.json"

def save_session_state():
    """세션 상태 저장"""
    SESSION_STATE_DIR.mkdir(parents=True, exist_ok=True)

    state = {
        "ended_at": datetime.now().isoformat(),
        "cwd": os.getcwd(),
        "incomplete_todos": [],
        "last_tool": os.environ.get("LAST_TOOL", ""),
        "context_usage": os.environ.get("CONTEXT_USAGE", "unknown")
    }

    # 미완료 Todo 저장
    if TODO_FILE.exists():
        try:
            with open(TODO_FILE, 'r') as f:
                todos = json.load(f).get("todos", [])
                state["incomplete_todos"] = [
                    t for t in todos if t.get("status") != "completed"
                ]
        except:
            pass

    # 세션 상태 파일 저장
    session_file = SESSION_STATE_DIR / "last-session.json"
    with open(session_file, 'w') as f:
        json.dump(state, f, indent=2)

    # 복구 정보
    if state["incomplete_todos"]:
        print(f"\n💾 세션 저장됨")
        print(f"   미완료 태스크: {len(state['incomplete_todos'])}개")
        print(f"   복구: '계속' 키워드 사용")

def main():
    save_session_state()

if __name__ == "__main__":
    main()
