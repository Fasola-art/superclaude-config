"""학습 시스템 데이터베이스 레이어"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import Pattern


class LearningDB:
    """학습 데이터 저장소"""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """DB 스키마 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY,
                    category TEXT NOT NULL,
                    input_text TEXT NOT NULL,
                    output_action TEXT NOT NULL,
                    context TEXT DEFAULT '{}',
                    confidence REAL DEFAULT 1.0,
                    created_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY,
                    pattern_id INTEGER NOT NULL,
                    positive INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (pattern_id) REFERENCES patterns(id)
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_cat ON patterns(category)"
            )

    def insert_pattern(
        self, category: str, input_text: str,
        output_action: str, context: dict
    ) -> int:
        """패턴 삽입"""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO patterns
                   (category, input_text, output_action, context, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (category, input_text, output_action, json.dumps(context), now)
            )
            return cursor.lastrowid

    def get_pattern(self, pattern_id: int) -> Optional[Pattern]:
        """패턴 조회"""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM patterns WHERE id = ?", (pattern_id,)
            ).fetchone()
        return self._row_to_pattern(row) if row else None

    def get_all_patterns(self) -> list[tuple]:
        """전체 패턴 조회"""
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT * FROM patterns").fetchall()

    def get_top_patterns(self, limit: int) -> list[Pattern]:
        """상위 패턴 조회"""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """SELECT * FROM patterns WHERE confidence >= 1.0
                   ORDER BY confidence DESC LIMIT ?""", (limit,)
            ).fetchall()
        return [self._row_to_pattern(r) for r in rows]

    def update_confidence(self, pattern_id: int, delta: float) -> None:
        """신뢰도 업데이트"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """UPDATE patterns SET confidence = MAX(0.1, confidence + ?)
                   WHERE id = ?""", (delta, pattern_id)
            )

    def insert_feedback(self, pattern_id: int, positive: bool) -> None:
        """피드백 삽입"""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO feedback (pattern_id, positive, timestamp)
                   VALUES (?, ?, ?)""", (pattern_id, int(positive), now)
            )

    def _row_to_pattern(self, row: tuple) -> Pattern:
        """DB row → Pattern 변환"""
        return Pattern(
            id=row[0], category=row[1], input_text=row[2],
            output_action=row[3], context=json.loads(row[4]),
            confidence=row[5], created_at=row[6]
        )
