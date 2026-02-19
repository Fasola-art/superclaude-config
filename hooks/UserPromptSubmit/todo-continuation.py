#!/usr/bin/env python3
"""
Todo Persistence Verification Hook
- Check incomplete tasks
- Ensure continuity between sessions
"""

import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude" / "hooks"))
from _shared.hook_utils import get_todo_title
from datetime import datetime

TODO_FILE = Path.home() / ".claude" / "todos" / "active.json"
STATE_FILE = Path.home() / ".claude" / "cache" / "todo-state.json"

def load_todos() -> list:
    """Load active todos"""
    if not TODO_FILE.exists():
        return []

    try:
        with open(TODO_FILE, 'r') as f:
            data = json.load(f)
            return data.get("todos", [])
    except:
        return []

def get_incomplete_todos(todos: list) -> list:
    """Filter incomplete todos"""
    return [t for t in todos if t.get("status") != "completed"]

def main():
    todos = load_todos()
    incomplete = get_incomplete_todos(todos)

    if incomplete:
        high_priority = [t for t in incomplete if t.get("priority") == "high"]
        normal = [t for t in incomplete if t.get("priority") != "high"]

        print(f"Incomplete tasks: {len(incomplete)}")

        if high_priority:
            print(f"  High priority: {len(high_priority)}")
            for t in high_priority[:3]:
                print(f"     - {get_todo_title(t)}")

        if normal and len(high_priority) < 3:
            remaining = 3 - len(high_priority)
            for t in normal[:remaining]:
                print(f"  - {get_todo_title(t)}")

    # Save state
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
