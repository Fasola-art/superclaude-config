#!/usr/bin/env python3
"""
Context 모델
"""

from __future__ import annotations

from typing import Optional

from ..db import get_db


class ContextManager:
    """컨텍스트 스냅샷 관리 (remember 기능)"""

    @staticmethod
    def save_context(
        project_path: str,
        last_file: str,
        last_action: str,
        summary: str,
    ) -> None:
        """컨텍스트 저장"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO context_snapshots
                    (project_path, last_file, last_action, conversation_summary)
                VALUES (?, ?, ?, ?)
                """,
                (project_path, last_file, last_action, summary),
            )

    @staticmethod
    def get_last_context(project_path: Optional[str] = None) -> Optional[dict]:
        """마지막 컨텍스트 조회"""
        with get_db() as conn:
            cursor = conn.cursor()

            if project_path:
                cursor.execute(
                    """
                    SELECT * FROM context_snapshots
                    WHERE project_path = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (project_path,),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM context_snapshots
                    ORDER BY created_at DESC
                    LIMIT 1
                    """
                )

            row = cursor.fetchone()
            return dict(row) if row else None
