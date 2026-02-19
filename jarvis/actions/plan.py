#!/usr/bin/env python3
"""Plan 기능 - 여행/이벤트 계획 관리"""

from __future__ import annotations

from typing import Optional
from jarvis.memory.db import get_db


def _init_plan_tables():
    """plans, plan_items 테이블 초기화"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plan_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER NOT NULL,
                item TEXT NOT NULL,
                time TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plan_id) REFERENCES plans(id)
            )
        """)


def create_plan(event_name: str, date: str, description: Optional[str] = None) -> int:
    """새 계획 생성"""
    _init_plan_tables()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO plans (event_name, date, description) VALUES (?, ?, ?)",
            (event_name, date, description)
        )
        conn.commit()
        return cursor.lastrowid


def add_plan_item(plan_id: int, item: str, time: Optional[str] = None) -> int:
    """계획에 아이템 추가"""
    _init_plan_tables()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO plan_items (plan_id, item, time) VALUES (?, ?, ?)",
            (plan_id, item, time)
        )
        conn.commit()
        return cursor.lastrowid


def get_plan(plan_id: int) -> dict | None:
    """
    계획 상세 조회 (아이템 포함)

    Args:
        plan_id: 계획 ID

    Returns:
        계획 정보 + 아이템 리스트
    """
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM plans WHERE id = ?", (plan_id,))
        plan_row = cursor.fetchone()
        if not plan_row:
            return None

        plan = dict(zip([c[0] for c in cursor.description], plan_row))

        cursor.execute(
            "SELECT id, item, time FROM plan_items WHERE plan_id = ? ORDER BY time",
            (plan_id,)
        )
        plan["items"] = [dict(zip([c[0] for c in cursor.description], row))
                         for row in cursor.fetchall()]

        return plan
