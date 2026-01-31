#!/usr/bin/env python3
"""
백그라운드 작업 알림 Hook
- 백그라운드 작업 완료 감지
- macOS 알림 전송
"""

import os
import subprocess
from pathlib import Path

def send_notification(title: str, message: str):
    """macOS 알림 전송"""
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

    # Task 도구에서만 (백그라운드 에이전트)
    if tool_name != "Task":
        return

    # 백그라운드 실행 여부 확인
    is_background = os.environ.get("RUN_IN_BACKGROUND", "false") == "true"

    if not is_background:
        return

    success = exit_code == "0"

    if success:
        send_notification(
            "Claude Code",
            "✅ 백그라운드 작업 완료"
        )
    else:
        send_notification(
            "Claude Code",
            "❌ 백그라운드 작업 실패"
        )

if __name__ == "__main__":
    main()
