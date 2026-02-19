#!/usr/bin/env python3
"""Book 기능 - 예약 관리"""

from __future__ import annotations

from typing import Optional
from jarvis.memory.db import get_db


def _init_bookings_table():
    """bookings 테이블 초기화"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                datetime TEXT NOT NULL,
                details TEXT NOT NULL,
                location TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def book_reservation(
    service: str,
    datetime_str: str,
    details: str,
    location: Optional[str] = None
) -> int:
    """
    예약 생성

    Args:
        service: 서비스 종류 (식당, 미용실, 병원 등)
        datetime_str: 예약 일시 (ISO format)
        details: 예약 상세
        location: 장소 (선택)

    Returns:
        생성된 booking ID
    """
    _init_bookings_table()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (service, datetime, details, location) VALUES (?, ?, ?, ?)",
            (service, datetime_str, details, location)
        )
        conn.commit()
        return cursor.lastrowid


def get_bookings(service: Optional[str] = None, status: str = "pending") -> list[dict]:
    """
    예약 목록 조회

    Args:
        service: 서비스 필터 (None이면 전체)
        status: 상태 필터

    Returns:
        예약 리스트
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM bookings WHERE status = ?"
        params = [status]

        if service:
            query += " AND service = ?"
            params.append(service)

        query += " ORDER BY datetime"
        cursor.execute(query, params)

        return [dict(zip([c[0] for c in cursor.description], row))
                for row in cursor.fetchall()]


def cancel_booking(booking_id: int) -> bool:
    """
    예약 취소

    Args:
        booking_id: 예약 ID

    Returns:
        성공 여부
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE bookings SET status = 'cancelled' WHERE id = ?",
            (booking_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
