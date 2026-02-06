#!/usr/bin/env python3
"""
Habit Tracker
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from .models import Habit, Streak, HabitFrequency
from .db_queries import HabitDB


class HabitTracker:
    """습관 추적기"""

    def __init__(self) -> None:
        self.db = HabitDB()

    def add_habit(
        self,
        name: str,
        description: str = "",
        frequency: HabitFrequency = HabitFrequency.DAILY,
        target_days: Optional[list[int]] = None,
    ) -> int:
        """습관 추가"""
        return self.db.add_habit(name, description, frequency, target_days)

    def get_habits(self, active_only: bool = True) -> list[Habit]:
        """습관 목록 조회"""
        return self.db.get_habits(active_only)

    def complete_habit(self, habit_id: int, notes: str = "") -> None:
        """습관 완료 기록"""
        self.db.complete_habit(habit_id, notes)

    def is_completed_today(self, habit_id: int) -> bool:
        """오늘 완료 여부 확인"""
        return self.db.is_completed_today(habit_id)

    def get_streak(self, habit_id: int) -> Streak:
        """연속 기록 계산"""
        dates = self.db.get_completion_dates(habit_id)

        if not dates:
            return Streak(habit_id=habit_id)

        # 현재 연속일 계산
        current_streak = 0
        today = date.today()

        for i, completed_date in enumerate(dates):
            expected_date = today - timedelta(days=i)
            if completed_date == expected_date:
                current_streak += 1
            else:
                break

        # 최장 연속일 계산
        longest_streak = 0
        temp_streak = 1

        for i in range(1, len(dates)):
            if dates[i - 1] - dates[i] == timedelta(days=1):
                temp_streak += 1
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1

        longest_streak = max(longest_streak, temp_streak, current_streak)

        return Streak(
            habit_id=habit_id,
            current=current_streak,
            longest=longest_streak,
            total_completions=len(dates),
            last_completed=dates[0] if dates else None,
        )

    def get_today_habits(self) -> list[tuple[Habit, bool]]:
        """오늘 해야 할 습관과 완료 여부"""
        habits = self.get_habits()
        result = []

        for habit in habits:
            if habit.is_due_today:
                completed = self.is_completed_today(habit.id)
                result.append((habit, completed))

        return result
