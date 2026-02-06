#!/usr/bin/env python3
"""Diet Coach - 식단 기록 및 관리"""

from datetime import datetime
from .base import BaseCoach


class DietCoach(BaseCoach):
    """Diet Coach 클래스"""

    CALORIE_TARGET = 2000

    def log_meal(self, meal_type: str, foods: list[str], calories: int, notes: str = ""):
        """식사 기록"""
        log = {
            'timestamp': datetime.now().isoformat(),
            'meal_type': meal_type,
            'foods': foods,
            'calories': calories,
            'notes': notes
        }
        self.logs.append(log)
        self._save_data()
        return log

    def log_activity(self, **kwargs):
        return self.log_meal(**kwargs)

    def get_daily_intake(self):
        """오늘 섭취 칼로리"""
        today = datetime.now().date().isoformat()
        today_logs = [log for log in self.logs if log['timestamp'].startswith(today)]
        total_calories = sum(log['calories'] for log in today_logs)

        return {
            'date': today,
            'total_calories': total_calories,
            'target': self.CALORIE_TARGET,
            'remaining': self.CALORIE_TARGET - total_calories,
            'meals_logged': [log['meal_type'] for log in today_logs],
            'progress': f"{(total_calories / self.CALORIE_TARGET * 100):.1f}%"
        }

    def get_summary(self, days: int = 7):
        """주간 요약"""
        recent = self._filter_recent_logs(days)
        if not recent:
            return {"message": f"최근 {days}일간 식사 기록이 없습니다."}

        total_calories = sum(log['calories'] for log in recent)
        meal_counts = {}
        for log in recent:
            meal_counts[log['meal_type']] = meal_counts.get(log['meal_type'], 0) + 1

        return {
            'period': f'최근 {days}일',
            'total_calories': total_calories,
            'avg_calories_per_day': total_calories / days,
            'meal_distribution': meal_counts,
            'avg_deviation': abs(total_calories / days - self.CALORIE_TARGET)
        }

    def suggest_meal(self):
        """식사 추천"""
        remaining = self.get_daily_intake()['remaining']

        if remaining > 800:
            return {'suggestion': f"{remaining}kcal 남음. 든든한 식사 권장"}
        elif remaining > 300:
            return {'suggestion': f"{remaining}kcal 남음. 가벼운 식사 권장"}
        return {'suggestion': "목표 달성! 무칼로리 음료 권장"}

    def suggest(self):
        return self.suggest_meal()
