#!/usr/bin/env python3
"""
Habit 분석 - 핵심 통계
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

from .models import HabitStats
from .tracker import HabitTracker

_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from memory.db import get_db  # noqa: E402


class HabitAnalytics:
    """습관 분석 - 통계 계산"""

    def __init__(self, tracker: HabitTracker) -> None:
        self.tracker = tracker

    def get_habit_stats(self, habit_id: int) -> HabitStats | None:
        """습관 통계"""
        habits = self.tracker.get_habits()
        habit = next((h for h in habits if h.id == habit_id), None)

        if not habit:
            return None

        streak = self.tracker.get_streak(habit_id)
        completion_7d = self._calculate_completion_rate(habit_id, 7)
        completion_30d = self._calculate_completion_rate(habit_id, 30)
        best_day, worst_day = self._analyze_by_weekday(habit_id)

        return HabitStats(
            habit=habit,
            streak=streak,
            completion_rate_7d=completion_7d,
            completion_rate_30d=completion_30d,
            best_day=best_day,
            worst_day=worst_day,
        )

    def _calculate_completion_rate(self, habit_id: int, days: int) -> float:
        """완료율 계산"""
        start_date = (date.today() - timedelta(days=days)).isoformat()

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(DISTINCT DATE(completed_at)) as completed_days
                FROM habit_logs
                WHERE habit_id = ? AND DATE(completed_at) >= ?
                """,
                (habit_id, start_date),
            )
            row = cursor.fetchone()
            completed_days = row["completed_days"] if row else 0

        return round(completed_days / days * 100, 1)

    def _analyze_by_weekday(self, habit_id: int) -> tuple[int | None, int | None]:
        """요일별 분석"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT strftime('%w', completed_at) as weekday, COUNT(*) as count
                FROM habit_logs
                WHERE habit_id = ?
                GROUP BY weekday
                ORDER BY count DESC
                """,
                (habit_id,),
            )

            rows = cursor.fetchall()
            if not rows:
                return None, None

            # SQLite %w: 0=일요일 → Python: 0=월요일
            weekday_map = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
            best_day = weekday_map.get(int(rows[0]["weekday"]), 0)
            worst_day = weekday_map.get(int(rows[-1]["weekday"]), 0)

            return best_day, worst_day
