#!/usr/bin/env python3
"""
JARVIS Memory Manager
SQLite 기반 메모리 관리 시스템
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path(__file__).parent / "jarvis.db"


def get_connection() -> sqlite3.Connection:
    """데이터베이스 연결 반환"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """데이터베이스 초기화 및 테이블 생성"""
    conn = get_connection()
    cursor = conn.cursor()

    # 작업 세션 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            project_path TEXT,
            files_edited TEXT,  -- JSON array
            tools_used TEXT,    -- JSON array
            summary TEXT
        )
    """)

    # 사용 패턴 테이블 (ML 학습용)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_of_week INTEGER,  -- 0=월, 6=일
            hour INTEGER,         -- 0-23
            work_type TEXT,       -- code_editing, testing, version_control 등
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
            status TEXT DEFAULT 'pending',  -- pending, in_progress, completed
            priority INTEGER DEFAULT 2,     -- 1=high, 2=medium, 3=low
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
            event_type TEXT,  -- meeting, reminder, deadline, personal
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 컨텍스트 저장 테이블 (remember 기능용)
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

    conn.commit()
    conn.close()


class WorkSessionManager:
    """작업 세션 관리"""

    @staticmethod
    def start_session(project_path: str, session_id: str) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO work_sessions (session_id, project_path) VALUES (?, ?)",
            (session_id, project_path)
        )
        conn.commit()
        session_db_id = cursor.lastrowid
        conn.close()
        return session_db_id

    @staticmethod
    def end_session(session_id: str, files_edited: List[str], tools_used: List[str], summary: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE work_sessions
            SET end_time = CURRENT_TIMESTAMP,
                files_edited = ?,
                tools_used = ?,
                summary = ?
            WHERE session_id = ?
        """, (json.dumps(files_edited), json.dumps(tools_used), summary, session_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_recent_sessions(limit: int = 5) -> List[Dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM work_sessions
            ORDER BY start_time DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_yesterday_summary() -> Optional[Dict]:
        conn = get_connection()
        cursor = conn.cursor()
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT * FROM work_sessions
            WHERE DATE(start_time) = ?
            ORDER BY start_time DESC
        """, (yesterday,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return None

        return {
            'date': yesterday,
            'sessions': [dict(row) for row in rows],
            'total_sessions': len(rows)
        }


class TaskManager:
    """작업 관리"""

    @staticmethod
    def add_task(title: str, description: str = "", priority: int = 2,
                 due_date: str = None, project_path: str = None) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, due_date, project_path)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, priority, due_date, project_path))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    @staticmethod
    def get_pending_tasks() -> List[Dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM tasks
            WHERE status != 'completed'
            ORDER BY priority ASC, due_date ASC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def complete_task(task_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (task_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_today_tasks() -> List[Dict]:
        conn = get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT * FROM tasks
            WHERE (due_date = ? OR due_date IS NULL)
            AND status != 'completed'
            ORDER BY priority ASC
        """, (today,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]


class CalendarManager:
    """일정 관리"""

    @staticmethod
    def add_event(title: str, event_time: str, location: str = "",
                  event_type: str = "reminder", notes: str = "") -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO calendar_events (title, event_time, location, event_type, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (title, event_time, location, event_type, notes))
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        return event_id

    @staticmethod
    def get_today_events() -> List[Dict]:
        conn = get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT * FROM calendar_events
            WHERE DATE(event_time) = ?
            ORDER BY event_time ASC
        """, (today,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_upcoming_events(days: int = 7) -> List[Dict]:
        conn = get_connection()
        cursor = conn.cursor()
        end_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT * FROM calendar_events
            WHERE DATE(event_time) <= ?
            AND DATE(event_time) >= DATE('now')
            ORDER BY event_time ASC
        """, (end_date,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]


class ContextManager:
    """컨텍스트 스냅샷 관리 (remember 기능)"""

    @staticmethod
    def save_context(project_path: str, last_file: str, last_action: str, summary: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO context_snapshots (project_path, last_file, last_action, conversation_summary)
            VALUES (?, ?, ?, ?)
        """, (project_path, last_file, last_action, summary))
        conn.commit()
        conn.close()

    @staticmethod
    def get_last_context(project_path: str = None) -> Optional[Dict]:
        conn = get_connection()
        cursor = conn.cursor()

        if project_path:
            cursor.execute("""
                SELECT * FROM context_snapshots
                WHERE project_path = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (project_path,))
        else:
            cursor.execute("""
                SELECT * FROM context_snapshots
                ORDER BY created_at DESC
                LIMIT 1
            """)

        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None


class UsagePatternTracker:
    """사용 패턴 추적"""

    @staticmethod
    def record_usage(work_type: str):
        now = datetime.now()
        day_of_week = now.weekday()
        hour = now.hour

        conn = get_connection()
        cursor = conn.cursor()

        # 기존 패턴 확인
        cursor.execute("""
            SELECT id, frequency FROM usage_patterns
            WHERE day_of_week = ? AND hour = ? AND work_type = ?
        """, (day_of_week, hour, work_type))

        row = cursor.fetchone()

        if row:
            cursor.execute("""
                UPDATE usage_patterns
                SET frequency = frequency + 1, last_updated = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (row['id'],))
        else:
            cursor.execute("""
                INSERT INTO usage_patterns (day_of_week, hour, work_type)
                VALUES (?, ?, ?)
            """, (day_of_week, hour, work_type))

        conn.commit()
        conn.close()

    @staticmethod
    def get_patterns() -> List[Dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM usage_patterns
            ORDER BY frequency DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]


# 초기화
if __name__ == "__main__":
    init_database()
    print("JARVIS database initialized successfully!")
