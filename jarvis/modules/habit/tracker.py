#!/usr/bin/env python3
"""
Habit Tracker
"""

from __future__ import annotations

import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional

from .models import Habit, Streak, HabitFrequency

_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from memory.db import get_db  # noqa: E402


class HabitTracker:
    """습관 추적기"""

    def __init__(self) -> None:
        self._init_tables()

    def _init_tables(self) -> None:
        """테이블 초기화"""
        with get_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    frequency TEXT DEFAULT 'DAILY',
                    target_days TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active INTEGER DEFAULT 1
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT DEFAULT '',
                    FOREIGN KEY (habit_id) REFERENCES habits(id)
                )
            """)

    def add_habit(
        self,
        name: str,
        description: str = "",
        frequency: HabitFrequency = HabitFrequency.DAILY,
        target_days: Optional[list[int]] = None,
    ) -> int:
        """습관 추가"""
        with get_db() as conn:
            cursor = conn.cursor()
            target_days_str = ",".join(map(str, target_days or []))
            cursor.execute(
                """
                INSERT INTO habits (name, description, frequency, target_days)
                VALUES (?, ?, ?, ?)
                """,
                (name, description, frequency.name, target_days_str),
            )
            return cursor.lastrowid or 0

    def get_habits(self, active_only: bool = True) -> list[Habit]:
        """습관 목록 조회"""
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM habits"
            if active_only:
                query += " WHERE active = 1"
            cursor.execute(query)

            habits = []
            for row in cursor.fetchall():
                target_days = (
                    [int(d) for d in row["target_days"].split(",") if d]
                    if row["target_days"]
                    else []
                )
                habits.append(Habit(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    frequency=HabitFrequency[row["frequency"]],
                    target_days=target_days,
                    created_at=datetime.fromisoformat(row["created_at"]),
                    active=bool(row["active"]),
                ))
            return habits

    def complete_habit(self, habit_id: int, notes: str = "") -> None:
        """습관 완료 기록"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO habit_logs (habit_id, notes)
                VALUES (?, ?)
                """,
                (habit_id, notes),
            )

    def is_completed_today(self, habit_id: int) -> bool:
        """오늘 완료 여부 확인"""
        today = date.today().isoformat()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) as cnt FROM habit_logs
                WHERE habit_id = ? AND DATE(completed_at) = ?
                """,
                (habit_id, today),
            )
            row = cursor.fetchone()
            return row["cnt"] > 0 if row else False

    def get_streak(self, habit_id: int) -> Streak:
        """연속 기록 계산"""
        with get_db() as conn:
            cursor = conn.cursor()

            # 최근 완료 기록 조회
            cursor.execute(
                """
                SELECT DATE(completed_at) as completed_date
                FROM habit_logs
                WHERE habit_id = ?
                GROUP BY DATE(completed_at)
                ORDER BY completed_date DESC
                """,
                (habit_id,),
            )

            dates = [date.fromisoformat(row["completed_date"]) for row in cursor.fetchall()]

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
