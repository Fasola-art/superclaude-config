#!/usr/bin/env python3
"""
사용 패턴 추적
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Dict

from .db import get_db


class UsagePatternTracker:
    """사용 패턴 추적"""

    @staticmethod
    def record_usage(work_type: str) -> None:
        now = datetime.now()
        day_of_week = now.weekday()
        hour = now.hour

        with get_db() as conn:
            cursor = conn.execute(
                "SELECT id, frequency FROM usage_patterns WHERE day_of_week = ? AND hour = ? AND work_type = ?",
                (day_of_week, hour, work_type)
            )
            row = cursor.fetchone()

            if row:
                conn.execute(
                    "UPDATE usage_patterns SET frequency = frequency + 1, last_updated = CURRENT_TIMESTAMP WHERE id = ?",
                    (row['id'],)
                )
            else:
                conn.execute(
                    "INSERT INTO usage_patterns (day_of_week, hour, work_type) VALUES (?, ?, ?)",
                    (day_of_week, hour, work_type)
                )

    @staticmethod
    def get_patterns() -> List[Dict]:
        with get_db() as conn:
            cursor = conn.execute("SELECT * FROM usage_patterns ORDER BY frequency DESC")
            return [dict(row) for row in cursor.fetchall()]
