#!/usr/bin/env python3
"""
Client Work Tracker
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from .db import ClientDB
from .types import WorkLog


class ClientTracker:
    """클라이언트 작업 추적기"""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db = ClientDB(db_path)

    def add_client(self, name: str, project: str) -> int:
        """클라이언트 추가"""
        cursor = self.db.execute(
            "INSERT INTO clients (name, project, created_at) VALUES (?, ?, ?)",
            (name, project, datetime.now().isoformat()),
        )
        return cursor.lastrowid

    def log_work(
        self, client_id: int, hours: float, description: str, hourly_rate: float = 0.0
    ) -> int:
        """작업 기록"""
        cursor = self.db.execute(
            "INSERT INTO work_logs (client_id, date, hours, description, hourly_rate) VALUES (?, ?, ?, ?, ?)",
            (client_id, datetime.now().isoformat(), hours, description, hourly_rate),
        )
        return cursor.lastrowid

    def get_summary(self, client_id: int) -> dict[str, float]:
        """클라이언트 작업 요약"""
        cursor = self.db.execute(
            "SELECT SUM(hours), SUM(hours * hourly_rate) FROM work_logs WHERE client_id = ?",
            (client_id,),
        )
        row = cursor.fetchone()
        return {"total_hours": row[0] or 0.0, "total_amount": row[1] or 0.0}

    def get_invoice_data(self, client_id: int, month: str) -> list[WorkLog]:
        """월별 인보이스 데이터"""
        cursor = self.db.execute(
            "SELECT id, client_id, date, hours, description, hourly_rate FROM work_logs WHERE client_id = ? AND date LIKE ?",
            (client_id, f"{month}%"),
        )
        return [
            WorkLog(
                id=row[0],
                client_id=row[1],
                date=datetime.fromisoformat(row[2]),
                hours=row[3],
                description=row[4],
                hourly_rate=row[5],
            )
            for row in cursor.fetchall()
        ]
