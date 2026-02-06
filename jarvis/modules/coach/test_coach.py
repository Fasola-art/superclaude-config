#!/usr/bin/env python3
"""Coach 모듈 테스트"""

import sys
from pathlib import Path
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent))
from coach import PTCoach, DietCoach


def test_pt_coach():
    """PT Coach 테스트"""
    print("=== PT Coach Test ===")
    temp_dir = Path(tempfile.mkdtemp())

    try:
        pt = PTCoach(temp_dir)

        # 운동 기록
        log1 = pt.log_workout("스쿼트", 3, 10, 60)
        print(f"✅ 운동 기록: {log1['exercise']} - {log1['volume']}kg")

        log2 = pt.log_workout("벤치프레스", 3, 8, 50)
        print(f"✅ 운동 기록: {log2['exercise']} - {log2['volume']}kg")

        # 요약
        summary = pt.get_weekly_summary()
        print(f"\n📊 주간 요약:")
        print(f"  - 운동일: {summary['workout_days']}일")
        print(f"  - 총 볼륨: {summary['total_volume']}kg")

        # 추천
        suggestion = pt.suggest_workout()
        print(f"\n💡 추천: {suggestion['suggestion']}")

    finally:
        shutil.rmtree(temp_dir)


def test_diet_coach():
    """Diet Coach 테스트"""
    print("\n=== Diet Coach Test ===")
    temp_dir = Path(tempfile.mkdtemp())

    try:
        diet = DietCoach(temp_dir)

        # 식사 기록
        log1 = diet.log_meal("breakfast", ["계란", "토스트"], 400)
        print(f"✅ 식사 기록: {log1['meal_type']} - {log1['calories']}kcal")

        log2 = diet.log_meal("lunch", ["치킨샐러드"], 600)
        print(f"✅ 식사 기록: {log2['meal_type']} - {log2['calories']}kcal")

        # 오늘 섭취량
        intake = diet.get_daily_intake()
        print(f"\n📊 오늘 섭취량:")
        print(f"  - 총 칼로리: {intake['total_calories']}kcal")
        print(f"  - 남은 칼로리: {intake['remaining']}kcal")
        print(f"  - 진행률: {intake['progress']}")

        # 추천
        suggestion = diet.suggest_meal()
        print(f"\n💡 추천: {suggestion['suggestion']}")

    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_pt_coach()
    test_diet_coach()
    print("\n✅ 모든 테스트 완료!")
