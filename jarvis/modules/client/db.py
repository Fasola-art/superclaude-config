"""
Client Tracker Database
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional


class ClientDB:
    """클라이언트 DB 관리"""

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = str(Path.home() / ".claude" / "jarvis" / "data" / "client.db")
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """DB 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    project TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    active INTEGER DEFAULT 1
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS work_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    hours REAL NOT NULL,
                    description TEXT NOT NULL,
                    hourly_rate REAL DEFAULT 0.0,
                    FOREIGN KEY (client_id) REFERENCES clients (id)
                )
                """
            )

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """쿼리 실행"""
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute(query, params)
