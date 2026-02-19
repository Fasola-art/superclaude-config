#!/usr/bin/env python3
"""
작업(Task) 관리
"""

from __future__ import annotations

from typing import List, Dict

from jarvis.utils.db_helpers import execute_insert, execute_query_all
from jarvis.utils.datetime_helpers import get_today_str
from .db import get_db


class TaskManager:
    """작업 관리"""

    @staticmethod
    def add_task(title: str, description: str = "", priority: int = 2,
                 due_date: str | None = None, project_path: str | None = None) -> int:
        return execute_insert(
            "INSERT INTO tasks (title, description, priority, due_date, project_path) VALUES (?, ?, ?, ?, ?)",
            (title, description, priority, due_date, project_path)
        )

    @staticmethod
    def get_pending_tasks() -> List[Dict]:
        return execute_query_all(
            "SELECT * FROM tasks WHERE status != 'completed' ORDER BY priority ASC, due_date ASC"
        )

    @staticmethod
    def complete_task(task_id: int) -> None:
        with get_db() as conn:
            conn.execute(
                "UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                (task_id,)
            )

    @staticmethod
    def get_today_tasks() -> List[Dict]:
        return execute_query_all(
            "SELECT * FROM tasks WHERE (due_date = ? OR due_date IS NULL) AND status != 'completed' ORDER BY priority ASC",
            (get_today_str(),)
        )
