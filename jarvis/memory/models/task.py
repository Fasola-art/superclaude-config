#!/usr/bin/env python3
"""
Task 모델
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from ..db import get_db


class TaskManager:
    """작업 관리"""

    @staticmethod
    def add_task(
        title: str,
        description: str = "",
        priority: int = 2,
        due_date: Optional[str] = None,
        project_path: Optional[str] = None,
    ) -> int:
        """작업 추가"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (title, description, priority, due_date, project_path)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, description, priority, due_date, project_path),
            )
            return cursor.lastrowid or 0

    @staticmethod
    def get_pending_tasks() -> list[dict]:
        """대기 중인 작업 조회"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM tasks
                WHERE status != 'completed'
                ORDER BY priority ASC, due_date ASC
                """
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def complete_task(task_id: int) -> None:
        """작업 완료"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tasks
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (task_id,),
            )

    @staticmethod
    def get_today_tasks() -> list[dict]:
        """오늘 작업 조회"""
        with get_db() as conn:
            cursor = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                """
                SELECT * FROM tasks
                WHERE (due_date = ? OR due_date IS NULL)
                AND status != 'completed'
                ORDER BY priority ASC
                """,
                (today,),
            )
            return [dict(row) for row in cursor.fetchall()]
