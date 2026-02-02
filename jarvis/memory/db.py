#!/usr/bin/env python3
"""
데이터베이스 연결 및 초기화
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Generator
from contextlib import contextmanager

DB_PATH = Path(__file__).parent / "jarvis.db"


def get_connection() -> sqlite3.Connection:
    """데이터베이스 연결 반환"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """컨텍스트 매니저로 DB 연결 관리"""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database() -> None:
    """데이터베이스 초기화 및 테이블 생성"""
    with get_db() as conn:
        cursor = conn.cursor()

        # 작업 세션 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS work_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                project_path TEXT,
                files_edited TEXT,
                tools_used TEXT,
                summary TEXT
            )
        """)

        # 사용 패턴 테이블 (ML 학습용)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week INTEGER,
                hour INTEGER,
                work_type TEXT,
                frequency INTEGER DEFAULT 1,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 작업 목록 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority INTEGER DEFAULT 2,
                due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                project_path TEXT
            )
        """)

        # 일정 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calendar_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                event_time TIMESTAMP,
                location TEXT,
                event_type TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 컨텍스트 저장 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS context_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_path TEXT,
                last_file TEXT,
                last_action TEXT,
                conversation_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
