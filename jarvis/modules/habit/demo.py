#!/usr/bin/env python3
"""
HabitTracker 데모 스크립트
"""

from __future__ import annotations

import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from modules.habit import HabitTracker, HabitAnalytics, HabitSummary, HabitFrequency


def main() -> None:
    """메인 데모"""
    tracker = HabitTracker()
    analytics = HabitAnalytics(tracker)
    summary = HabitSummary(tracker)

    print("=" * 60)
    print("JARVIS HabitTracker 데모")
    print("=" * 60)

    # 1. 습관 추가
    print("\n[1] 습관 추가")
    h1 = tracker.add_habit("독서", "매일 30분", HabitFrequency.DAILY)
    h2 = tracker.add_habit("운동", "주 3회", HabitFrequency.WEEKLY, [0, 2, 4])
    print(f"   - 독서 (ID: {h1})")
    print(f"   - 운동 (ID: {h2})")

    # 2. 오늘 할 습관
    print("\n[2] 오늘 할 습관")
    for habit, completed in tracker.get_today_habits():
        status = "✅" if completed else "⬜"
        print(f"   {status} {habit.name}")

    # 3. 습관 완료
    print("\n[3] 습관 완료 기록")
    tracker.complete_habit(h1, "독서 완료!")
    print("   - 독서 완료 ✅")

    # 4. 연속 기록
    print("\n[4] 연속 기록")
    streak = tracker.get_streak(h1)
    print(f"   - 현재: {streak.current}일")
    print(f"   - 최장: {streak.longest}일")
    print(f"   - 총 완료: {streak.total_completions}회")

    # 5. 통계
    print("\n[5] 통계")
    stats = analytics.get_habit_stats(h1)
    if stats:
        print(f"   - 7일 완료율: {stats.completion_rate_7d}%")
        print(f"   - 30일 완료율: {stats.completion_rate_30d}%")

    # 6. 동기부여 메시지
    print("\n[6] 동기부여 메시지")
    msg = summary.get_motivation_message(h1)
    print(f"   {msg}")

    # 7. 주간 요약
    print("\n[7] 주간 요약")
    result = summary.get_weekly_summary()
    print(f"   - 전체 완료율: {result['total_completion_rate']}%")
    print(f"   - 최고 습관: {result['best_habit']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
