#!/usr/bin/env python3
"""
Background Task Notification Hook
- Detect background task completion
- Send macOS notification
"""

import os
import subprocess
from pathlib import Path

def send_notification(title: str, message: str):
    """Send macOS notification"""
    try:
        script = f'''
        display notification "{message}" with title "{title}" sound name "Glass"
        '''
        subprocess.run(["osascript", "-e", script], capture_output=True)
    except:
        pass

def main():
    tool_name = os.environ.get("TOOL_NAME", "")
    exit_code = os.environ.get("EXIT_CODE", "0")

    # Only for Task tool (background agent)
    if tool_name != "Task":
        return

    # Check if running in background
    is_background = os.environ.get("RUN_IN_BACKGROUND", "false") == "true"

    if not is_background:
        return

    success = exit_code == "0"

    if success:
        send_notification(
            "Claude Code",
            "Background task completed"
        )
    else:
        send_notification(
            "Claude Code",
            "Background task failed"
        )

if __name__ == "__main__":
    main()
