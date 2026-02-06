#!/usr/bin/env python3
"""
Pattern Analyzer
사용 패턴 분석 및 제안
"""

from __future__ import annotations
from typing import Any

from .manager import UsagePatternTracker


class PatternAnalyzer:
    """패턴 분석기"""

    @staticmethod
    def get_peak_hours(work_type: str | None = None) -> list[dict[str, Any]]:
        """특정 작업 유형의 피크 시간대 분석"""
        patterns = UsagePatternTracker.get_patterns()

        if work_type:
            patterns = [p for p in patterns if p['work_type'] == work_type]

        # 시간대별 집계
        hour_totals = {}
        for p in patterns:
            hour = p['hour']
            if hour not in hour_totals:
                hour_totals[hour] = 0
            hour_totals[hour] += p['frequency']

        # 상위 시간대 반환
        sorted_hours = sorted(hour_totals.items(), key=lambda x: x[1], reverse=True)

        return [
            {'hour': h, 'frequency': f, 'period': PatternAnalyzer._hour_to_period(h)}
            for h, f in sorted_hours[:5]
        ]

    @staticmethod
    def get_weekly_pattern() -> dict[str, list[dict[str, Any]]]:
        """요일별 패턴 분석"""
        patterns = UsagePatternTracker.get_patterns()

        days = ['월', '화', '수', '목', '금', '토', '일']
        day_patterns: dict[str, list[dict[str, Any]]] = {day: [] for day in days}

        for p in patterns:
            day_name = days[p['day_of_week']]
            day_patterns[day_name].append({
                'hour': p['hour'],
                'work_type': p['work_type'],
                'frequency': p['frequency']
            })

        return day_patterns

    @staticmethod
    def suggest_next_action(predictor) -> str | None:
        """다음 작업 제안"""
        prediction = predictor.predict_work_type()

        if not prediction or prediction['confidence'] < 50:
            return None

        work_type = prediction['predicted_work_type']
        confidence = prediction['confidence']

        suggestions = {
            'code_editing': "코드 작성/수정 작업이 예상됩니다.",
            'testing': "테스트 관련 작업이 예상됩니다.",
            'version_control': "Git 작업이 예상됩니다.",
            'documentation': "문서 작업이 예상됩니다.",
            'debugging': "디버깅 작업이 예상됩니다.",
            'review': "코드 리뷰가 예상됩니다."
        }

        base_suggestion = suggestions.get(work_type, f"{work_type} 작업이 예상됩니다.")
        return f"{base_suggestion} (신뢰도: {confidence}%)"

    @staticmethod
    def _hour_to_period(hour: int) -> str:
        """시간을 시간대 문자열로 변환"""
        if 5 <= hour < 9:
            return "이른 아침"
        elif 9 <= hour < 12:
            return "오전"
        elif 12 <= hour < 14:
            return "점심"
        elif 14 <= hour < 18:
            return "오후"
        elif 18 <= hour < 21:
            return "저녁"
        elif 21 <= hour < 24:
            return "밤"
        else:
            return "새벽"
