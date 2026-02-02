#!/usr/bin/env python3
"""
Context Auto-Cleanup Hook (DCP)
- Monitor context usage
- Auto-cleanup when threshold reached
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# DCP thresholds
THRESHOLDS = {
    "warning": 75,    # Show warning
    "critical": 90,   # Suggest auto DCP
    "emergency": 95   # Force compression
}

# State file
STATE_FILE = Path.home() / ".claude" / "cache" / "context-state.json"

def get_context_usage() -> int:
    """Estimate current context usage (%)"""
    # In practice, should get token count from Claude API
    # Here we estimate based on session file size
    session_dir = Path.home() / ".claude" / "projects"

    if not session_dir.exists():
        return 0

    # Most recent session file
    jsonl_files = list(session_dir.rglob("*.jsonl"))
    if not jsonl_files:
        return 0

    latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
    size_mb = latest.stat().st_size / (1024 * 1024)

    # Rough estimate (200KB = about 10%)
    estimated_usage = min(int(size_mb * 50), 100)
    return estimated_usage

def check_and_alert():
    """Check context usage and alert"""
    usage = get_context_usage()

    if usage >= THRESHOLDS["emergency"]:
        print(f"CTX:{usage}% -> /compact needed")
    elif usage >= THRESHOLDS["critical"]:
        print(f"CTX:{usage}%")
    # Skip warning output

    # Save state
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
