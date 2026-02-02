#!/usr/bin/env python3
"""
UsagePattern 모델
"""

from __future__ import annotations

from datetime import datetime

from ..db import get_db


class UsagePatternTracker:
    """사용 패턴 추적"""

    @staticmethod
    def record_usage(work_type: str) -> None:
        """사용 패턴 기록"""
        now = datetime.now()
        day_of_week = now.weekday()
        hour = now.hour

        with get_db() as conn:
            cursor = conn.cursor()

            # 기존 패턴 확인
            cursor.execute(
                """
                SELECT id, frequency FROM usage_patterns
                WHERE day_of_week = ? AND hour = ? AND work_type = ?
                """,
                (day_of_week, hour, work_type),
            )

            row = cursor.fetchone()

            if row:
                cursor.execute(
                    """
                    UPDATE usage_patterns
                    SET frequency = frequency + 1, last_updated = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (row["id"],),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO usage_patterns (day_of_week, hour, work_type)
                    VALUES (?, ?, ?)
                    """,
                    (day_of_week, hour, work_type),
                )

    @staticmethod
    def get_patterns() -> list[dict]:
        """패턴 조회"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM usage_patterns
                ORDER BY frequency DESC
                """
            )
            return [dict(row) for row in cursor.fetchall()]
