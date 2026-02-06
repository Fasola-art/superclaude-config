#!/usr/bin/env python3
"""plan.py 테스트"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from actions.plan import create_plan, add_plan_item, get_plan


def test_plan():
    """계획 시스템 테스트"""
    print("=== Plan 테스트 시작 ===\n")

    # 1. 계획 생성
    plan_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    plan_id = create_plan(
        event_name="제주도 여행",
        date=plan_date,
        description="3박 4일 가족 여행"
    )
    print(f"✅ 계획 생성: ID={plan_id}")

    # 2. 계획 아이템 추가
    items = [
        ("공항 도착", "09:00"),
        ("렌터카 픽업", "10:00"),
        ("호텔 체크인", "15:00"),
        ("성산일출봉 방문", "17:00")
    ]

    for item, time in items:
        item_id = add_plan_item(plan_id, item, time)
        print(f"✅ 아이템 추가: [{time}] {item} (ID={item_id})")

    # 3. 계획 조회
    plan = get_plan(plan_id)
    if plan:
        print(f"\n✅ 계획 조회:")
        print(f"  이벤트: {plan['event_name']}")
        print(f"  날짜: {plan['date']}")
        print(f"  설명: {plan['description']}")
        print(f"  아이템: {len(plan['items'])}개")
        for item in plan['items']:
            print(f"    - [{item['time']}] {item['item']}")

    print("\n=== Plan 테스트 완료 ===")


if __name__ == "__main__":
    test_plan()
