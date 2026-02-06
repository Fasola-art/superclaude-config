#!/usr/bin/env python3
"""PT Coach - 운동 기록 및 관리"""

from datetime import datetime
from collections import Counter
from .base import BaseCoach


class PTCoach(BaseCoach):
    """PT Coach 클래스"""

    def log_workout(self, exercise: str, sets: int, reps: int, weight: float = 0.0, notes: str = ""):
        """운동 기록"""
        log = {
            'timestamp': datetime.now().isoformat(),
            'exercise': exercise,
            'sets': sets,
            'reps': reps,
            'weight': weight,
            'volume': sets * reps * weight,
            'notes': notes
        }
        self.logs.append(log)
        self._save_data()
        return log

    def log_activity(self, **kwargs):
        return self.log_workout(**kwargs)

    def get_weekly_summary(self):
        """주간 요약"""
        return self._get_summary(7)

    def get_summary(self, days: int = 7):
        return self._get_summary(days)

    def _get_summary(self, days: int):
        """N일 요약"""
        recent = self._filter_recent_logs(days)
        if not recent:
            return {"message": f"최근 {days}일간 운동 기록이 없습니다."}

        exercises = Counter(log['exercise'] for log in recent)
        total_volume = sum(log['volume'] for log in recent)
        workout_days = len(set(log['timestamp'][:10] for log in recent))

        return {
            'period': f'최근 {days}일',
            'workout_days': workout_days,
            'total_volume': total_volume,
            'exercises': dict(exercises.most_common()),
            'avg_volume_per_day': total_volume / days if workout_days > 0 else 0
        }

    def suggest_workout(self):
        """운동 추천"""
        recent = self._filter_recent_logs(7)
        if not recent:
            return {"suggestion": "스쿼트 3세트 x 10회로 시작하세요!"}

        exercises = Counter(log['exercise'] for log in recent)
        least_done = exercises.most_common()[-1][0] if exercises else "스쿼트"

        return {
            'suggestion': f"{least_done}가 부족합니다. 오늘은 {least_done}를 중점으로!",
            'recent_exercises': dict(exercises.most_common())
        }

    def suggest(self):
        return self.suggest_workout()
