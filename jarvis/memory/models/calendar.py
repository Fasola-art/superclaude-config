#!/usr/bin/env python3
"""
Calendar 모델
"""

from __future__ import annotations

from datetime import datetime, timedelta

from ..db import get_db


class CalendarManager:
    """일정 관리"""

    @staticmethod
    def add_event(
        title: str,
        event_time: str,
        location: str = "",
        event_type: str = "reminder",
        notes: str = "",
    ) -> int:
        """일정 추가"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO calendar_events (title, event_time, location, event_type, notes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, event_time, location, event_type, notes),
            )
            return cursor.lastrowid or 0

    @staticmethod
    def get_today_events() -> list[dict]:
        """오늘 일정 조회"""
        with get_db() as conn:
            cursor = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                """
                SELECT * FROM calendar_events
                WHERE DATE(event_time) = ?
                ORDER BY event_time ASC
                """,
                (today,),
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_upcoming_events(days: int = 7) -> list[dict]:
        """다가오는 일정 조회"""
        with get_db() as conn:
            cursor = conn.cursor()
            end_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            cursor.execute(
                """
                SELECT * FROM calendar_events
                WHERE DATE(event_time) <= ?
                AND DATE(event_time) >= DATE('now')
                ORDER BY event_time ASC
                """,
                (end_date,),
            )
            return [dict(row) for row in cursor.fetchall()]
