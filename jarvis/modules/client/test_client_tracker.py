#!/usr/bin/env python3
"""
Client Tracker Tests
"""

import tempfile
from pathlib import Path

from .tracker import ClientTracker


def test_add_client():
    """클라이언트 추가 테스트"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = str(Path(tmpdir) / "test.db")
        tracker = ClientTracker(db_path)

        client_id = tracker.add_client("Acme Corp", "Website Redesign")
        assert client_id > 0
        print("✅ 클라이언트 추가 성공")


def test_log_work():
    """작업 로그 테스트"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = str(Path(tmpdir) / "test.db")
        tracker = ClientTracker(db_path)

        client_id = tracker.add_client("Acme Corp", "Website")
        log_id = tracker.log_work(client_id, 5.5, "Frontend development", 100.0)
        assert log_id > 0
        print("✅ 작업 로그 성공")


def test_get_summary():
    """작업 요약 테스트"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = str(Path(tmpdir) / "test.db")
        tracker = ClientTracker(db_path)

        client_id = tracker.add_client("Acme Corp", "Website")
        tracker.log_work(client_id, 5.0, "Design", 100.0)
        tracker.log_work(client_id, 3.0, "Development", 120.0)

        summary = tracker.get_summary(client_id)
        assert summary["total_hours"] == 8.0
        assert summary["total_amount"] == 860.0
        print("✅ 작업 요약 성공")


def test_get_invoice_data():
    """인보이스 데이터 테스트"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = str(Path(tmpdir) / "test.db")
        tracker = ClientTracker(db_path)

        client_id = tracker.add_client("Acme Corp", "Website")
        tracker.log_work(client_id, 5.0, "Design", 100.0)

        logs = tracker.get_invoice_data(client_id, "2026-02")
        assert len(logs) == 1
        assert logs[0].hours == 5.0
        print("✅ 인보이스 데이터 조회 성공")


if __name__ == "__main__":
    test_add_client()
    test_log_work()
    test_get_summary()
    test_get_invoice_data()
    print("\n🎉 모든 테스트 통과")
