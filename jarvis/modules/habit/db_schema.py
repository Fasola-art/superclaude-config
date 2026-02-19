#!/usr/bin/env python3
"""
Habit 데이터베이스 스키마
"""

from __future__ import annotations

import sys
from pathlib import Path

_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from jarvis.memory.db import get_db  # noqa: E402


def init_habit_tables() -> None:
    """습관 테이블 초기화"""
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                frequency TEXT DEFAULT 'DAILY',
                target_days TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active INTEGER DEFAULT 1
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT DEFAULT '',
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            )
        """)
