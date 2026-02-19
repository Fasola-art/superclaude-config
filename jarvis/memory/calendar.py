#!/usr/bin/env python3
"""
일정 관리
"""

from __future__ import annotations

from typing import List, Dict

from jarvis.utils.db_helpers import execute_insert, execute_query_all
from jarvis.utils.datetime_helpers import get_today_str, get_date_n_days_later


class CalendarManager:
    """일정 관리"""

    @staticmethod
    def add_event(title: str, event_time: str, location: str = "",
                  event_type: str = "reminder", notes: str = "") -> int:
        return execute_insert(
            "INSERT INTO calendar_events (title, event_time, location, event_type, notes) VALUES (?, ?, ?, ?, ?)",
            (title, event_time, location, event_type, notes)
        )

    @staticmethod
    def get_today_events() -> List[Dict]:
        return execute_query_all(
            "SELECT * FROM calendar_events WHERE DATE(event_time) = ? ORDER BY event_time ASC",
            (get_today_str(),)
        )

    @staticmethod
    def get_upcoming_events(days: int = 7) -> List[Dict]:
        return execute_query_all(
            "SELECT * FROM calendar_events WHERE DATE(event_time) <= ? AND DATE(event_time) >= DATE('now') ORDER BY event_time ASC",
            (get_date_n_days_later(days),)
        )
