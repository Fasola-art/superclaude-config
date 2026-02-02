#!/usr/bin/env python3
"""
JARVIS Memory Manager
SQLite 기반 메모리 관리 시스템
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict

from .db import get_db, init_database


class WorkSessionManager:
    """작업 세션 관리"""

    @staticmethod
    def start_session(project_path: str, session_id: str) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO work_sessions (session_id, project_path) VALUES (?, ?)",
                (session_id, project_path)
            )
            return cursor.lastrowid or 0

    @staticmethod
    def end_session(session_id: str, files_edited: List[str], tools_used: List[str], summary: str) -> None:
        with get_db() as conn:
            conn.execute("""
                UPDATE work_sessions
                SET end_time = CURRENT_TIMESTAMP, files_edited = ?, tools_used = ?, summary = ?
                WHERE session_id = ?
            """, (json.dumps(files_edited), json.dumps(tools_used), summary, session_id))

    @staticmethod
    def get_recent_sessions(limit: int = 5) -> List[Dict]:
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM work_sessions ORDER BY start_time DESC LIMIT ?", (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_yesterday_summary() -> Optional[Dict]:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM work_sessions WHERE DATE(start_time) = ? ORDER BY start_time DESC",
                (yesterday,)
            )
            rows = cursor.fetchall()
        if not rows:
            return None
        return {'date': yesterday, 'sessions': [dict(row) for row in rows], 'total_sessions': len(rows)}


class TaskManager:
    """작업 관리"""

    @staticmethod
    def add_task(title: str, description: str = "", priority: int = 2,
                 due_date: str | None = None, project_path: str | None = None) -> int:
        with get_db() as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (title, description, priority, due_date, project_path) VALUES (?, ?, ?, ?, ?)",
                (title, description, priority, due_date, project_path)
            )
            return cursor.lastrowid or 0

    @staticmethod
    def get_pending_tasks() -> List[Dict]:
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE status != 'completed' ORDER BY priority ASC, due_date ASC"
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def complete_task(task_id: int) -> None:
        with get_db() as conn:
            conn.execute(
                "UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                (task_id,)
            )

    @staticmethod
    def get_today_tasks() -> List[Dict]:
        today = datetime.now().strftime('%Y-%m-%d')
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE (due_date = ? OR due_date IS NULL) AND status != 'completed' ORDER BY priority ASC",
                (today,)
            )
            return [dict(row) for row in cursor.fetchall()]


class CalendarManager:
    """일정 관리"""

    @staticmethod
    def add_event(title: str, event_time: str, location: str = "",
                  event_type: str = "reminder", notes: str = "") -> int:
        with get_db() as conn:
            cursor = conn.execute(
                "INSERT INTO calendar_events (title, event_time, location, event_type, notes) VALUES (?, ?, ?, ?, ?)",
                (title, event_time, location, event_type, notes)
            )
            return cursor.lastrowid or 0

    @staticmethod
    def get_today_events() -> List[Dict]:
        today = datetime.now().strftime('%Y-%m-%d')
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM calendar_events WHERE DATE(event_time) = ? ORDER BY event_time ASC",
                (today,)
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_upcoming_events(days: int = 7) -> List[Dict]:
        end_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM calendar_events WHERE DATE(event_time) <= ? AND DATE(event_time) >= DATE('now') ORDER BY event_time ASC",
                (end_date,)
            )
            return [dict(row) for row in cursor.fetchall()]


class ContextManager:
    """컨텍스트 스냅샷 관리 (remember 기능)"""

    @staticmethod
    def save_context(project_path: str, last_file: str, last_action: str, summary: str) -> None:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO context_snapshots (project_path, last_file, last_action, conversation_summary) VALUES (?, ?, ?, ?)",
                (project_path, last_file, last_action, summary)
            )

    @staticmethod
    def get_last_context(project_path: str | None = None) -> Optional[Dict]:
        with get_db() as conn:
            if project_path:
                cursor = conn.execute(
                    "SELECT * FROM context_snapshots WHERE project_path = ? ORDER BY created_at DESC LIMIT 1",
                    (project_path,)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM context_snapshots ORDER BY created_at DESC LIMIT 1"
                )
            row = cursor.fetchone()
        return dict(row) if row else None


class UsagePatternTracker:
    """사용 패턴 추적"""

    @staticmethod
    def record_usage(work_type: str) -> None:
        now = datetime.now()
        day_of_week = now.weekday()
        hour = now.hour

        with get_db() as conn:
            cursor = conn.execute(
                "SELECT id, frequency FROM usage_patterns WHERE day_of_week = ? AND hour = ? AND work_type = ?",
                (day_of_week, hour, work_type)
            )
            row = cursor.fetchone()

            if row:
                conn.execute(
                    "UPDATE usage_patterns SET frequency = frequency + 1, last_updated = CURRENT_TIMESTAMP WHERE id = ?",
                    (row['id'],)
                )
            else:
                conn.execute(
                    "INSERT INTO usage_patterns (day_of_week, hour, work_type) VALUES (?, ?, ?)",
                    (day_of_week, hour, work_type)
                )

    @staticmethod
    def get_patterns() -> List[Dict]:
        with get_db() as conn:
            cursor = conn.execute("SELECT * FROM usage_patterns ORDER BY frequency DESC")
            return [dict(row) for row in cursor.fetchall()]


if __name__ == "__main__":
    init_database()
    print("JARVIS database initialized successfully!")
