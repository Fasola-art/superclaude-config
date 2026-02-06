"""
로그 집계 시스템

시스템 전체 로그를 SQLite에 수집하고 분석
"""
import json
import sqlite3
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional


class LogLevel(Enum):
    """로그 레벨"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogAggregator:
    """로그 집계기"""

    def __init__(self, db_path: str = "~/.claude/jarvis/data/logs.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """DB 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY,
                    level TEXT NOT NULL,
                    source TEXT NOT NULL,
                    message TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    timestamp TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_level ON logs(level)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_source ON logs(source)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_time ON logs(timestamp)")

    def log(
        self,
        level: LogLevel,
        source: str,
        message: str,
        metadata: Optional[dict] = None
    ) -> int:
        """로그 기록"""
        now = datetime.now().isoformat()
        meta = json.dumps(metadata or {})

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO logs (level, source, message, metadata, timestamp) VALUES (?, ?, ?, ?, ?)",
                (level.value, source, message, meta, now)
            )
            return cursor.lastrowid

    def query(
        self,
        level: Optional[LogLevel] = None,
        source: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> list[dict]:
        """로그 조회"""
        conditions = []
        params = []

        if level:
            conditions.append("level = ?")
            params.append(level.value)
        if source:
            conditions.append("source = ?")
            params.append(source)
        if since:
            conditions.append("timestamp >= ?")
            params.append(since.isoformat())

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT * FROM logs {where} ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql, params).fetchall()

        return [
            {
                "id": r["id"],
                "level": r["level"],
                "source": r["source"],
                "message": r["message"],
                "metadata": json.loads(r["metadata"]),
                "timestamp": r["timestamp"]
            }
            for r in rows
        ]

    def get_summary(self, hours: int = 24) -> dict:
        """로그 요약 통계"""
        since = datetime.now() - timedelta(hours=hours)

        with sqlite3.connect(self.db_path) as conn:
            # 전체 수
            total = conn.execute(
                "SELECT COUNT(*) FROM logs WHERE timestamp >= ?",
                (since.isoformat(),)
            ).fetchone()[0]

            # 레벨별 수
            by_level = {}
            for row in conn.execute(
                "SELECT level, COUNT(*) FROM logs WHERE timestamp >= ? GROUP BY level",
                (since.isoformat(),)
            ):
                by_level[row[0]] = row[1]

            # 소스별 수
            by_source = {}
            for row in conn.execute(
                "SELECT source, COUNT(*) FROM logs WHERE timestamp >= ? GROUP BY source",
                (since.isoformat(),)
            ):
                by_source[row[0]] = row[1]

        return {
            "total": total,
            "by_level": by_level,
            "by_source": by_source,
            "period_hours": hours
        }

    def cleanup(self, days: int = 30) -> int:
        """오래된 로그 삭제"""
        cutoff = datetime.now() - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM logs WHERE timestamp < ?",
                (cutoff.isoformat(),)
            )
            return cursor.rowcount
