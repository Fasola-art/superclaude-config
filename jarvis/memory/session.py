#!/usr/bin/env python3
"""
작업 세션 관리
"""

from __future__ import annotations

import json
from typing import List, Dict, Optional

from utils.db_helpers import execute_insert, execute_query_all
from utils.datetime_helpers import get_yesterday_str
from .db import get_db


class WorkSessionManager:
    """작업 세션 관리"""

    @staticmethod
    def start_session(project_path: str, session_id: str) -> int:
        return execute_insert(
            "INSERT INTO work_sessions (session_id, project_path) VALUES (?, ?)",
            (session_id, project_path)
        )

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
        return execute_query_all(
            "SELECT * FROM work_sessions ORDER BY start_time DESC LIMIT ?",
            (limit,)
        )

    @staticmethod
    def get_yesterday_summary() -> Optional[Dict]:
        yesterday = get_yesterday_str()
        rows = execute_query_all(
            "SELECT * FROM work_sessions WHERE DATE(start_time) = ? ORDER BY start_time DESC",
            (yesterday,)
        )
        if not rows:
            return None
        return {'date': yesterday, 'sessions': rows, 'total_sessions': len(rows)}
