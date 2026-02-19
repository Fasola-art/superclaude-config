#!/usr/bin/env python3
"""remind.py 테스트"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis.memory.db import init_database
from jarvis.actions.remind import (
    add_reminder,
    get_pending_reminders,
    dismiss_reminder,
    snooze_reminder
)


def test_remind():
    """리마인더 기능 통합 테스트"""
    init_database(force=True)

    # 1. 리마인더 추가
    past_time = datetime.now() - timedelta(minutes=5)
    future_time = datetime.now() + timedelta(hours=1)

    rid1 = add_reminder("회의 준비하기", past_time, repeat="daily")
    rid2 = add_reminder("보고서 작성", future_time)

    print(f"✅ 리마인더 추가: #{rid1}, #{rid2}")

    # 2. 대기 중인 리마인더 조회 (과거 시간만)
    pending = get_pending_reminders()
    assert len(pending) == 1, f"Expected 1, got {len(pending)}"
    assert pending[0]['message'] == "회의 준비하기"
    print(f"✅ 대기 중인 리마인더: {len(pending)}개")

    # 3. 스누즈
    success = snooze_reminder(rid1, minutes=30)
    assert success, "Snooze failed"
    pending_after_snooze = get_pending_reminders()
    assert len(pending_after_snooze) == 0, "Snoozed reminder still pending"
    print("✅ 스누즈 성공")

    # 4. 해제
    success = dismiss_reminder(rid1)
    assert success, "Dismiss failed"
    print("✅ 리마인더 해제 성공")

    print("\n🎉 모든 테스트 통과")


if __name__ == "__main__":
    test_remind()
