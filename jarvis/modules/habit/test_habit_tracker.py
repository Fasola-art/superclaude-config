#!/usr/bin/env python3
"""
HabitTracker 통합 테스트
"""

from __future__ import annotations

import sys
from pathlib import Path

# JARVIS root 경로 추가
_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from modules.habit import HabitTracker, HabitAnalytics, HabitSummary, HabitFrequency


def test_basic_workflow() -> None:
    """기본 워크플로우 테스트"""
    tracker = HabitTracker()
    analytics = HabitAnalytics(tracker)
    summary = HabitSummary(tracker)

    # 1. 습관 추가
    habit_id = tracker.add_habit(
        name="독서",
        description="매일 30분 독서하기",
        frequency=HabitFrequency.DAILY,
    )
    print(f"✅ 습관 추가 완료 (ID: {habit_id})")

    # 2. 오늘 할 습관 조회
    today_habits = tracker.get_today_habits()
    print(f"✅ 오늘 할 습관: {len(today_habits)}개")
    for habit, completed in today_habits:
        print(f"   - {habit.name}: {'완료' if completed else '미완료'}")

    # 3. 습관 완료 기록
    tracker.complete_habit(habit_id, notes="30분 소설 읽기")
    print("✅ 습관 완료 기록")

    # 4. 연속 기록 확인
    streak = tracker.get_streak(habit_id)
    print(f"✅ 연속 기록: 현재 {streak.current}일, 최장 {streak.longest}일")

    # 5. 통계 조회
    stats = analytics.get_habit_stats(habit_id)
    if stats:
        print(f"✅ 통계:")
        print(f"   - 7일 완료율: {stats.completion_rate_7d}%")
        print(f"   - 30일 완료율: {stats.completion_rate_30d}%")

    # 6. 동기부여 메시지
    message = summary.get_motivation_message(habit_id)
    print(f"✅ 메시지: {message}")


def test_weekly_summary() -> None:
    """주간 요약 테스트"""
    tracker = HabitTracker()
    summary = HabitSummary(tracker)

    # 여러 습관 추가
    tracker.add_habit("운동", frequency=HabitFrequency.DAILY)
    tracker.add_habit("명상", frequency=HabitFrequency.DAILY)
    tracker.add_habit("일기", frequency=HabitFrequency.DAILY)

    # 주간 요약
    result = summary.get_weekly_summary()
    print(f"\n✅ 주간 요약:")
    print(f"   - 주 시작: {result['week_start']}")
    print(f"   - 전체 완료율: {result['total_completion_rate']}%")
    print(f"   - 최고 습관: {result['best_habit']}")
    print(f"   - 주의 필요: {result['needs_attention']}")


if __name__ == "__main__":
    print("=" * 60)
    print("HabitTracker 통합 테스트")
    print("=" * 60)

    test_basic_workflow()
    print("\n" + "=" * 60)
    test_weekly_summary()
    print("=" * 60)
    print("\n✅ 모든 테스트 완료")
