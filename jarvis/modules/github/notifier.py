#!/usr/bin/env python3
"""
GitHub 알림 처리 모듈
"""

from __future__ import annotations

import subprocess
from typing import Callable

from .types import Notification


class GitHubNotifier:
    """GitHub 알림 전송"""

    def __init__(self) -> None:
        self._handlers: list[Callable[[Notification], None]] = []

    def add_handler(self, handler: Callable[[Notification], None]) -> None:
        """알림 핸들러 추가"""
        self._handlers.append(handler)

    def notify(self, notification: Notification) -> None:
        """알림 전송"""
        for handler in self._handlers:
            handler(notification)

    def notify_all(self, notifications: list[Notification]) -> None:
        """여러 알림 전송"""
        for notification in notifications:
            self.notify(notification)


def macos_notification_handler(notification: Notification) -> None:
    """macOS 알림 전송"""
    title = notification.type.replace("_", " ").title()
    message = notification.title

    # osascript로 알림 전송
    script = f'''
    display notification "{message}" with title "JARVIS GitHub" subtitle "{title}"
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True)


def console_notification_handler(notification: Notification) -> None:
    """콘솔 출력"""
    priority_emoji = {
        "low": "📝",
        "normal": "📬",
        "high": "⚠️",
        "urgent": "🚨",
    }
    emoji = priority_emoji.get(notification.priority, "📬")
    print(f"{emoji} [{notification.type}] {notification.title}")
    print(f"   {notification.url}")


def create_default_notifier() -> GitHubNotifier:
    """기본 설정의 Notifier 생성"""
    notifier = GitHubNotifier()
    notifier.add_handler(macos_notification_handler)
    notifier.add_handler(console_notification_handler)
    return notifier
