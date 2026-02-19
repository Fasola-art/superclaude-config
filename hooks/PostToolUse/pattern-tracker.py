#!/usr/bin/env python3
"""
Pattern Tracking/Learning Hook
- Record success/failure patterns
- Accumulate learning data
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PATTERNS_DIR = Path.home() / ".claude" / "patterns"
PATTERNS_FILE = PATTERNS_DIR / "learned-patterns.json"

def load_patterns() -> dict:
    """Load saved patterns"""
    if PATTERNS_FILE.exists():
        try:
            with open(PATTERNS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"success": [], "failure": [], "stats": {}}

def save_patterns(patterns: dict):
    """Save patterns"""
    PATTERNS_DIR.mkdir(parents=True, exist_ok=True)
    with open(PATTERNS_FILE, 'w') as f:
        json.dump(patterns, f, indent=2)

def record_pattern(tool_name: str, success: bool, context: dict = None):
    """Record pattern"""
    patterns = load_patterns()

    pattern = {
        "tool": tool_name,
        "timestamp": datetime.now().isoformat(),
        "context": context or {}
    }

    category = "success" if success else "failure"
    patterns[category].append(pattern)

    # Keep only recent 100 entries
    patterns[category] = patterns[category][-100:]

    # Update statistics
    if tool_name not in patterns["stats"]:
        patterns["stats"][tool_name] = {"success": 0, "failure": 0}

    if success:
        patterns["stats"][tool_name]["success"] += 1
    else:
        patterns["stats"][tool_name]["failure"] += 1

    save_patterns(patterns)

def main():
    tool_name = os.environ.get("TOOL_NAME", "unknown")
    exit_code = os.environ.get("EXIT_CODE", "0")

    success = exit_code == "0"

    context = {
        "cwd": os.getcwd(),
        "file": os.environ.get("FILE_PATH", "")
    }

    record_pattern(tool_name, success, context)

    # Warn if failure rate is high
    patterns = load_patterns()
    stats = patterns["stats"].get(tool_name, {})
    total = stats.get("success", 0) + stats.get("failure", 0)

    if total >= 10:  # Threshold raised
        failure_rate = stats.get("failure", 0) / total
        if failure_rate > 0.6:  # Only warn if above 60%
            print(f"Warning: {tool_name}: {failure_rate:.0%} failure rate")

if __name__ == "__main__":
    main()
