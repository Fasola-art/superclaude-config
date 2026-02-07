"""
장소 추천/예약 기능 테스트
"""
import sys
import os
import sqlite3
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def create_test_db() -> str:
    """테스트용 임시 DB 생성"""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    conn = sqlite3.connect(db_path)
    schema_dir = Path(__file__).parent.parent / "schema"
    for sql_file in ["core.sql", "tasks.sql", "tracking.sql", "extended.sql", "places.sql"]:
        sql_path = schema_dir / sql_file
        if sql_path.exists():
            conn.executescript(sql_path.read_text())
    conn.close()
    return db_path


def test_imports():
    """모듈 임포트 테스트"""
    from jarvis import PlaceSearcher, PlaceManager
    from jarvis.modules.places import CATEGORY_KEYWORDS
    assert PlaceSearcher is not None
    assert PlaceManager is not None
    assert "restaurant" in CATEGORY_KEYWORDS
    return True


def test_place_manager_save_and_get():
    """장소 저장/조회 테스트"""
    db_path = create_test_db()
    try:
        from jarvis import PlaceManager
        pm = PlaceManager(db_path=db_path)
        place_id = pm.save_place({
            "name": "테스트 카페",
            "category": "cafe",
            "address": "서울시 강남구 역삼동 123",
            "rating": 4.5,
            "google_place_id": "ChIJtest123",
        }, bookmark=True)
        assert place_id > 0

        bookmarks = pm.get_bookmarks()
        assert len(bookmarks) == 1
        assert bookmarks[0]["name"] == "테스트 카페"

        # 카테고리 필터
        assert len(pm.get_bookmarks(category="cafe")) == 1
        assert len(pm.get_bookmarks(category="restaurant")) == 0

        pm.close()
        return True
    finally:
        os.unlink(db_path)


def test_reservation():
    """예약 관리 테스트"""
    db_path = create_test_db()
    try:
        from jarvis import PlaceManager
        pm = PlaceManager(db_path=db_path)
        place_id = pm.save_place({
            "name": "맛있는 식당",
            "category": "restaurant",
            "google_place_id": "ChIJrestaurant1",
        })

        res_id = pm.add_reservation(
            place_id=place_id,
            title="주말 저녁 식사",
            reserved_date="2026-02-14",
            reserved_time="18:30",
            party_size=4,
            notes="창가 자리 요청",
        )
        assert res_id > 0

        reservations = pm.get_reservations()
        assert len(reservations) == 1
        assert reservations[0]["title"] == "주말 저녁 식사"
        assert reservations[0]["party_size"] == 4

        pm.update_reservation_status(res_id, "completed")
        completed = pm.get_reservations(status="completed", upcoming_only=False)
        assert len(completed) == 1

        pm.close()
        return True
    finally:
        os.unlink(db_path)


def test_visit_tracking():
    """방문 기록 테스트"""
    db_path = create_test_db()
    try:
        from jarvis import PlaceManager
        pm = PlaceManager(db_path=db_path)
        place_id = pm.save_place({
            "name": "단골 카페",
            "category": "cafe",
            "google_place_id": "ChIJcafe_regular",
        })

        pm.record_visit(place_id)
        pm.record_visit(place_id)
        bookmarks = pm.get_bookmarks()
        assert bookmarks[0]["visit_count"] == 2
        assert bookmarks[0]["last_visited_at"] is not None

        pm.close()
        return True
    finally:
        os.unlink(db_path)


def test_nlu_place_intents():
    """NLU 장소 관련 인텐트 테스트"""
    from jarvis import NLUParser
    parser = NLUParser()

    # 장소 검색 인텐트
    result = parser.parse("주말에 놀러갈 곳 추천해줘")
    assert result["intent"] == "search_place"

    result = parser.parse("강남 맛집 추천")
    assert result["intent"] == "search_place"

    # 예약 인텐트
    result = parser.parse("예약 추가해줘")
    assert result["intent"] == "add_reservation"

    result = parser.parse("예약 목록 보여줘")
    assert result["intent"] == "list_reservations"

    # 지역 추출
    result = parser.parse("제주도 카페 추천")
    assert result["entities"].get("region") is not None
    assert result["entities"].get("place_category") == "cafe"

    return True


def test_remove_bookmark():
    """즐겨찾기 해제 테스트"""
    db_path = create_test_db()
    try:
        from jarvis import PlaceManager
        pm = PlaceManager(db_path=db_path)
        place_id = pm.save_place({
            "name": "임시 장소",
            "category": "other",
            "google_place_id": "ChIJtemp",
        }, bookmark=True)

        assert len(pm.get_bookmarks()) == 1
        pm.remove_bookmark(place_id)
        assert len(pm.get_bookmarks()) == 0

        pm.close()
        return True
    finally:
        os.unlink(db_path)


if __name__ == "__main__":
    tests = [
        ("imports", test_imports),
        ("place_manager_save_get", test_place_manager_save_and_get),
        ("reservation", test_reservation),
        ("visit_tracking", test_visit_tracking),
        ("nlu_place_intents", test_nlu_place_intents),
        ("remove_bookmark", test_remove_bookmark),
    ]

    passed = 0
    for name, fn in tests:
        try:
            result = fn()
            status = "PASS" if result else "FAIL"
            if result:
                passed += 1
        except Exception as e:
            status = f"FAIL ({e})"
        print(f"{'✅' if status == 'PASS' else '❌'} {name:30s}: {status}")

    print(f"\nTotal: {passed}/{len(tests)} tests passed")
