#!/usr/bin/env python3
"""
컨텍스트 스냅샷 관리 (remember 기능)
"""

from __future__ import annotations

from typing import Optional, Dict

from jarvis.utils.db_helpers import execute_query
from .db import get_db


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
        if project_path:
            return execute_query(
                "SELECT * FROM context_snapshots WHERE project_path = ? ORDER BY created_at DESC LIMIT 1",
                (project_path,),
                fetch_one=True
            )
        else:
            return execute_query(
                "SELECT * FROM context_snapshots ORDER BY created_at DESC LIMIT 1",
                fetch_one=True
            )
