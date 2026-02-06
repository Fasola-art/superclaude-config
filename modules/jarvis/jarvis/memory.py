"""
Memory management components
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class DatabaseManager:
    """Base database manager"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = str(Path.home() / ".claude/modules/jarvis/jarvis.db")
        self.db_path = db_path
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute(self, query: str, params: tuple = ()):
        self.connect()
        self.conn.execute("PRAGMA busy_timeout = 5000")
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor


class TaskManager(DatabaseManager):
    """Task management"""

    def add_task(self, title: str, priority: int = 5,
                 due_date: str = None, tags: List[str] = None) -> int:
        query = """
            INSERT INTO tasks (title, priority, due_date, tags, status)
            VALUES (?, ?, ?, ?, 'todo')
        """
        import json
        tags_json = json.dumps(tags) if tags else None
        cursor = self.execute(query, (title, priority, due_date, tags_json))
        return cursor.lastrowid

    def get_tasks(self, status: str = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM tasks"
        params = ()

        if status:
            query += " WHERE status = ?"
            params = (status,)

        query += " ORDER BY priority DESC, created_at DESC"
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def complete_task(self, task_id: int):
        query = "UPDATE tasks SET status = 'done' WHERE id = ?"
        self.execute(query, (task_id,))


class CalendarManager(DatabaseManager):
    """Calendar event management"""

    def add_event(self, title: str, start_time: str,
                  end_time: str = None, location: str = None) -> int:
        query = """
            INSERT INTO calendar_events (title, start_time, end_time, location)
            VALUES (?, ?, ?, ?)
        """
        cursor = self.execute(query, (title, start_time, end_time, location))
        return cursor.lastrowid

    def get_events(self, start_date: str = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM calendar_events"
        params = ()

        if start_date:
            query += " WHERE DATE(start_time) >= DATE(?)"
            params = (start_date,)

        query += " ORDER BY start_time"
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


class ContextManager(DatabaseManager):
    """Context tracking"""

    def add_context(self, context_type: str, data: str,
                    metadata: str = None) -> int:
        query = """
            INSERT INTO context_history (context_type, data, metadata)
            VALUES (?, ?, ?)
        """
        cursor = self.execute(query, (context_type, data, metadata))
        return cursor.lastrowid

    def get_recent_context(self, limit: int = 10) -> List[Dict[str, Any]]:
        query = """
            SELECT * FROM context_history
            ORDER BY timestamp DESC
            LIMIT ?
        """
        cursor = self.execute(query, (limit,))
        return [dict(row) for row in cursor.fetchall()]
