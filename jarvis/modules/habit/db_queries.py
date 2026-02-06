#!/usr/bin/env python3
"""
Habit DB - CRUD
"""

from __future__ import annotations

import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

from .models import Habit, HabitFrequency
from .db_schema import init_habit_tables

_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from memory.db import get_db  # noqa: E402


class HabitDB:
    """습관 데이터베이스"""

    def __init__(self) -> None:
        init_habit_tables()

    def add_habit(
        self, name: str, description: str = "",
        frequency: HabitFrequency = HabitFrequency.DAILY,
        target_days: Optional[list[int]] = None,
    ) -> int:
        """습관 추가"""
        with get_db() as conn:
            cursor = conn.cursor()
            target_days_str = ",".join(map(str, target_days or []))
            cursor.execute(
                "INSERT INTO habits (name, description, frequency, target_days) VALUES (?, ?, ?, ?)",
                (name, description, frequency.name, target_days_str),
            )
            return cursor.lastrowid or 0

    def get_habits(self, active_only: bool = True) -> list[Habit]:
        """습관 목록"""
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM habits"
            if active_only:
                query += " WHERE active = 1"
            cursor.execute(query)

            habits = []
            for row in cursor.fetchall():
                target_days = [int(d) for d in row["target_days"].split(",") if d] if row["target_days"] else []
                habits.append(Habit(
                    id=row["id"], name=row["name"], description=row["description"],
                    frequency=HabitFrequency[row["frequency"]], target_days=target_days,
                    created_at=datetime.fromisoformat(row["created_at"]), active=bool(row["active"]),
                ))
            return habits

    def complete_habit(self, habit_id: int, notes: str = "") -> None:
        """완료 기록"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO habit_logs (habit_id, notes) VALUES (?, ?)", (habit_id, notes))

    def is_completed_today(self, habit_id: int) -> bool:
        """오늘 완료?"""
        today = date.today().isoformat()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as cnt FROM habit_logs WHERE habit_id = ? AND DATE(completed_at) = ?",
                (habit_id, today),
            )
            row = cursor.fetchone()
            return row["cnt"] > 0 if row else False

    def get_completion_dates(self, habit_id: int) -> list[date]:
        """완료 날짜"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DATE(completed_at) as d FROM habit_logs WHERE habit_id = ? "
                "GROUP BY DATE(completed_at) ORDER BY d DESC",
                (habit_id,),
            )
            return [date.fromisoformat(row["d"]) for row in cursor.fetchall()]
