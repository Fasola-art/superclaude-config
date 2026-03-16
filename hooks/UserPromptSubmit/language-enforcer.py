#!/usr/bin/env python3
"""
Korean Response Enforcement Hook
- Check Korean response setting
- Code comments also in Korean
"""

import os
import json
from pathlib import Path

SETTINGS_FILE = Path.home() / ".claude" / "settings.json"

def check_language_setting():
    """Check language setting and notify"""
    # Show only on first prompt
    state_file = Path.home() / ".claude" / "cache" / "lang-reminded.json"

    if state_file.exists():
        return

    # Show notification
    print("Response language: Korean (including code comments)")

    # Save state
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump({"reminded": True}, f)

if __name__ == "__main__":
    check_language_setting()
