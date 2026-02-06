#!/usr/bin/env python3
"""
Habit 분석 - 요약 및 메시지
"""

from __future__ import annotations

from datetime import date, timedelta

from .tracker import HabitTracker
from .analytics_core import HabitAnalytics as CoreAnalytics


class HabitSummary:
    """습관 요약 및 동기부여"""

    def __init__(self, tracker: HabitTracker) -> None:
        self.tracker = tracker
        self.analytics = CoreAnalytics(tracker)

    def get_weekly_summary(self) -> dict:
        """주간 요약"""
        habits = self.tracker.get_habits()
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

        summary: dict[str, object] = {
            "week_start": week_start.isoformat(),
            "habits": [],
            "total_completion_rate": 0.0,
            "best_habit": None,
            "needs_attention": [],
        }
        habits_list: list[dict[str, object]] = []
        needs_attention_list: list[str] = []
        rates: list[tuple[str, float]] = []

        for habit in habits:
            rate = self.analytics._calculate_completion_rate(habit.id, 7)
            streak = self.tracker.get_streak(habit.id)

            habit_summary = {
                "name": habit.name,
                "completion_rate": rate,
                "current_streak": streak.current,
            }
            habits_list.append(habit_summary)
            rates.append((habit.name, rate))

            if rate < 50:
                needs_attention_list.append(habit.name)

        summary["habits"] = habits_list
        summary["needs_attention"] = needs_attention_list

        if rates:
            summary["total_completion_rate"] = round(sum(r for _, r in rates) / len(rates), 1)
            summary["best_habit"] = max(rates, key=lambda x: x[1])[0]

        return summary

    def get_motivation_message(self, habit_id: int) -> str:
        """동기부여 메시지"""
        streak = self.tracker.get_streak(habit_id)
        stats = self.analytics.get_habit_stats(habit_id)

        if not stats:
            return "습관을 시작해보세요! 💪"

        if streak.current >= 7:
            return f"대단해요! {streak.current}일 연속 달성 중! 🔥"
        elif streak.current >= 3:
            return f"{streak.current}일 연속! 계속 유지해보세요! ⭐"
        elif streak.current == 0:
            if streak.longest > 0:
                return f"다시 시작해요! 최장 기록 {streak.longest}일을 깨보세요! 💪"
            return "오늘부터 시작! 한 걸음씩 나아가요! 🌱"
        else:
            return f"{streak.current}일째! 좋은 시작이에요! 👍"
