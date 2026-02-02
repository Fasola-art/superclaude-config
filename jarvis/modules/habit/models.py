#!/usr/bin/env python3
"""
Habit Tracker 모델
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum, auto
from typing import Optional


class HabitFrequency(Enum):
    """습관 빈도"""

    DAILY = auto()
    WEEKLY = auto()
    WEEKDAYS = auto()  # 월-금
    CUSTOM = auto()


@dataclass
class Habit:
    """습관 정의"""

    id: int
    name: str
    description: str = ""
    frequency: HabitFrequency = HabitFrequency.DAILY
    target_days: list[int] = field(default_factory=list)  # 0=월, 6=일
    created_at: datetime = field(default_factory=datetime.now)
    active: bool = True

    @property
    def is_due_today(self) -> bool:
        """오늘 해야 하는 습관인지 확인"""
        today = datetime.now().weekday()

        if self.frequency == HabitFrequency.DAILY:
            return True
        elif self.frequency == HabitFrequency.WEEKDAYS:
            return today < 5  # 월-금
        elif self.frequency == HabitFrequency.WEEKLY:
            return today in self.target_days
        elif self.frequency == HabitFrequency.CUSTOM:
            return today in self.target_days

        return False


@dataclass
class HabitLog:
    """습관 기록"""

    id: int
    habit_id: int
    completed_at: datetime
    notes: str = ""


@dataclass
class Streak:
    """연속 기록"""

    habit_id: int
    current: int = 0  # 현재 연속일
    longest: int = 0  # 최장 연속일
    total_completions: int = 0  # 총 완료 횟수
    last_completed: Optional[date] = None


@dataclass
class HabitStats:
    """습관 통계"""

    habit: Habit
    streak: Streak
    completion_rate_7d: float = 0.0  # 최근 7일 완료율
    completion_rate_30d: float = 0.0  # 최근 30일 완료율
    best_day: Optional[int] = None  # 가장 잘 지키는 요일
    worst_day: Optional[int] = None  # 가장 잘 못 지키는 요일
