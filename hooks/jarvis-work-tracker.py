#!/usr/bin/env python3
"""
JARVIS Work Tracker Hook
Record tool usage in SQLite and learn patterns
Hook Type: PostToolUse
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add JARVIS module path
JARVIS_DIR = Path.home() / ".claude" / "jarvis"
sys.path.insert(0, str(JARVIS_DIR / "memory"))


def main():
    # Get tool information from environment variables
    tool_name = os.environ.get('CLAUDE_TOOL_NAME', '')
    tool_input = os.environ.get('CLAUDE_TOOL_INPUT', '{}')

    if not tool_name:
        return

    try:
        input_data = json.loads(tool_input)
    except:
        input_data = {}

    # Extract file path (parameter names used by various tools)
    file_path = (
        input_data.get('file_path', '') or
        input_data.get('path', '') or
        input_data.get('pattern', '') or
        ''
    )

    try:
        from manager import init_database, UsagePatternTracker
        from ml_predictor import classify_work_type

        init_database()

        # Classify work type
        work_type = classify_work_type(tool_name, file_path)

        # Record pattern
        UsagePatternTracker.record_usage(work_type)

    except Exception as e:
        # Hook failure handled silently (don't disrupt user experience)
        pass


if __name__ == "__main__":
    main()
