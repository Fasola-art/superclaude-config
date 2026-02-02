#!/usr/bin/env python3
"""
Session End State Saver Hook
- Save incomplete todos
- Save session state
- Record recovery information
"""

import os
import json
from pathlib import Path
from datetime import datetime

SESSION_STATE_DIR = Path.home() / ".claude" / "session-env"
TODO_FILE = Path.home() / ".claude" / "todos" / "active.json"

def save_session_state():
    """Save session state"""
    SESSION_STATE_DIR.mkdir(parents=True, exist_ok=True)

    state = {
        "ended_at": datetime.now().isoformat(),
        "cwd": os.getcwd(),
        "incomplete_todos": [],
        "last_tool": os.environ.get("LAST_TOOL", ""),
        "context_usage": os.environ.get("CONTEXT_USAGE", "unknown")
    }

    # Save incomplete todos
    if TODO_FILE.exists():
        try:
            with open(TODO_FILE, 'r') as f:
                todos = json.load(f).get("todos", [])
                state["incomplete_todos"] = [
                    t for t in todos if t.get("status") != "completed"
                ]
        except:
            pass

    # Save session state file
    session_file = SESSION_STATE_DIR / "last-session.json"
    with open(session_file, 'w') as f:
        json.dump(state, f, indent=2)

    # Recovery information
    if state["incomplete_todos"]:
        print(f"\nSession saved")
        print(f"   Incomplete tasks: {len(state['incomplete_todos'])}")
        print(f"   Recovery: use 'continue' keyword")

def main():
    save_session_state()

if __name__ == "__main__":
    main()
