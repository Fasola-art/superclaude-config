#!/usr/bin/env python3
"""
Infinite Loop Detection Hook
- Detect consecutive failures
- Trigger forced stop
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

STATE_FILE = Path.home() / ".claude" / "cache" / "loop-state.json"
MAX_CONSECUTIVE_FAILURES = 5
TIME_WINDOW_MINUTES = 5

def load_state() -> dict:
    """Load state"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"failures": [], "warned": False}

def save_state(state: dict):
    """Save state"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def check_loop():
    """Check for infinite loop"""
    exit_code = os.environ.get("EXIT_CODE", "0")
    tool_name = os.environ.get("TOOL_NAME", "")

    # Reset state on success
    if exit_code == "0":
        save_state({"failures": [], "warned": False})
        return

    state = load_state()
    now = datetime.now()

    # Keep only failures within time window
    cutoff = now - timedelta(minutes=TIME_WINDOW_MINUTES)
    recent_failures = [
        f for f in state["failures"]
        if datetime.fromisoformat(f["time"]) > cutoff
    ]

    # Add current failure
    recent_failures.append({
        "time": now.isoformat(),
        "tool": tool_name
    })

    state["failures"] = recent_failures

    if len(recent_failures) >= MAX_CONSECUTIVE_FAILURES:
        if not state["warned"]:
            print(f"Loop: {len(recent_failures)} failures -> manual intervention needed")
            state["warned"] = True
    elif len(recent_failures) >= 3:
        print(f"Loop: {len(recent_failures)}/{MAX_CONSECUTIVE_FAILURES}")

    save_state(state)

if __name__ == "__main__":
    check_loop()
