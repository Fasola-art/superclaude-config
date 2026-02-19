#!/usr/bin/env python3
"""리마인더 관리 모듈"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# 절대 경로 설정
sys.path.insert(0, str(Path(__file__).parent.parent))
from jarvis.memory.db import get_db


def add_reminder(
    message: str,
    remind_at: datetime | str,
    repeat: Optional[str] = None
) -> int:
    """리마인더 추가 (repeat: 'daily'|'weekly'|'monthly'|None)"""
    if isinstance(remind_at, str):
        remind_at = datetime.fromisoformat(remind_at)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO reminders (message, remind_at, repeat_interval)
               VALUES (?, ?, ?)""",
            (message, remind_at.isoformat(), repeat)
        )
        return cursor.lastrowid


def get_pending_reminders() -> list[dict]:
    """현재 시간 기준 대기 중인 리마인더 조회"""
    now = datetime.now().isoformat()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, message, remind_at, repeat_interval, snoozed_until
               FROM reminders
               WHERE is_dismissed = 0
                 AND (snoozed_until IS NULL OR snoozed_until <= ?)
                 AND remind_at <= ?
               ORDER BY remind_at""",
            (now, now)
        )
        return [dict(row) for row in cursor.fetchall()]


def dismiss_reminder(reminder_id: int) -> bool:
    """리마인더 해제"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reminders SET is_dismissed = 1 WHERE id = ?",
            (reminder_id,)
        )
        return cursor.rowcount > 0


def snooze_reminder(reminder_id: int, minutes: int = 10) -> bool:
    """리마인더 스누즈 (기본 10분)"""
    snooze_until = (datetime.now() + timedelta(minutes=minutes)).isoformat()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reminders SET snoozed_until = ? WHERE id = ?",
            (snooze_until, reminder_id)
        )
        return cursor.rowcount > 0
