#!/usr/bin/env python3
"""
Todo 지속성 검증 Hook
- 미완료 태스크 확인
- 세션 간 연속성 보장
"""

import os
import json
from pathlib import Path
from datetime import datetime

TODO_FILE = Path.home() / ".claude" / "todos" / "active.json"
STATE_FILE = Path.home() / ".claude" / "cache" / "todo-state.json"

def load_todos() -> list:
    """활성 Todo 로드"""
    if not TODO_FILE.exists():
        return []

    try:
        with open(TODO_FILE, 'r') as f:
            data = json.load(f)
            return data.get("todos", [])
    except:
        return []

def get_incomplete_todos(todos: list) -> list:
    """미완료 Todo 필터링"""
    return [t for t in todos if t.get("status") != "completed"]

def main():
    todos = load_todos()
    incomplete = get_incomplete_todos(todos)

    if incomplete:
        high_priority = [t for t in incomplete if t.get("priority") == "high"]
        normal = [t for t in incomplete if t.get("priority") != "high"]

        print(f"📋 미완료 태스크: {len(incomplete)}개")

        if high_priority:
            print(f"  🔴 높은 우선순위: {len(high_priority)}개")
            for t in high_priority[:3]:
                print(f"     • {t.get('title', 'Untitled')}")

        if normal and len(high_priority) < 3:
            remaining = 3 - len(high_priority)
            for t in normal[:remaining]:
                print(f"  ⚪ {t.get('title', 'Untitled')}")

    # 상태 저장
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "total": len(todos),
        "incomplete": len(incomplete),
        "checked_at": datetime.now().isoformat()
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

if __name__ == "__main__":
    main()
