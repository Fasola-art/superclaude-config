#!/usr/bin/env python3
"""book.py 테스트"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# 현재 디렉토리를 sys.path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis.actions.book import book_reservation, get_bookings, cancel_booking


def test_book():
    """예약 시스템 테스트"""
    print("=== Book 테스트 시작 ===\n")

    # 1. 예약 생성
    tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
    booking_id = book_reservation(
        service="식당",
        datetime_str=tomorrow,
        details="4인 예약 - 창가 자리 요청",
        location="강남구 레스토랑 ABC"
    )
    print(f"✅ 예약 생성: ID={booking_id}")

    # 2. 예약 목록 조회
    bookings = get_bookings()
    print(f"✅ 예약 목록 조회: {len(bookings)}건")
    for b in bookings:
        print(f"  - [{b['service']}] {b['datetime']}: {b['details']}")

    # 3. 예약 취소
    success = cancel_booking(booking_id)
    print(f"✅ 예약 취소: {'성공' if success else '실패'}")

    # 4. 취소 확인
    active = get_bookings(status="pending")
    cancelled = get_bookings(status="cancelled")
    print(f"✅ 활성 예약: {len(active)}건, 취소: {len(cancelled)}건")

    print("\n=== Book 테스트 완료 ===")


if __name__ == "__main__":
    test_book()
