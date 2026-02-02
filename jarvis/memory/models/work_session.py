#!/usr/bin/env python3
"""
WorkSession 모델
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Optional

from ..db import get_db


class WorkSessionManager:
    """작업 세션 관리"""

    @staticmethod
    def start_session(project_path: str, session_id: str) -> int:
        """세션 시작"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO work_sessions (session_id, project_path) VALUES (?, ?)",
                (session_id, project_path),
            )
            return cursor.lastrowid or 0

    @staticmethod
    def end_session(
        session_id: str,
        files_edited: list[str],
        tools_used: list[str],
        summary: str,
    ) -> None:
        """세션 종료"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE work_sessions
                SET end_time = CURRENT_TIMESTAMP,
                    files_edited = ?,
                    tools_used = ?,
                    summary = ?
                WHERE session_id = ?
                """,
                (json.dumps(files_edited), json.dumps(tools_used), summary, session_id),
            )

    @staticmethod
    def get_recent_sessions(limit: int = 5) -> list[dict]:
        """최근 세션 조회"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM work_sessions
                ORDER BY start_time DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_yesterday_summary() -> Optional[dict]:
        """어제 세션 요약"""
        with get_db() as conn:
            cursor = conn.cursor()
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            cursor.execute(
                """
                SELECT * FROM work_sessions
                WHERE DATE(start_time) = ?
                ORDER BY start_time DESC
                """,
                (yesterday,),
            )
            rows = cursor.fetchall()

            if not rows:
                return None

            return {
                "date": yesterday,
                "sessions": [dict(row) for row in rows],
                "total_sessions": len(rows),
            }
