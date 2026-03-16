#!/usr/bin/env python3
"""
Background Task Notification Hook
- Detect background task completion
- Send desktop notification (Windows / macOS)
"""

import os
import platform
import subprocess


def send_notification(title: str, message: str):
    """Send desktop notification (cross-platform)"""
    try:
        system = platform.system()
        if system == "Darwin":
            script = f'display notification "{message}" with title "{title}" sound name "Glass"'
            subprocess.run(["osascript", "-e", script], capture_output=True)
        elif system == "Windows":
            ps_script = f'''
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$template = @"
<toast>
    <visual>
        <binding template="ToastGeneric">
            <text>{title}</text>
            <text>{message}</text>
        </binding>
    </visual>
</toast>
"@
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code").Show($toast)
'''
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
    except Exception:
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
