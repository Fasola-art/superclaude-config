#!/usr/bin/env python3
"""
에이전트 메모리 관리 - Task 에이전트 간 컨텍스트 유지

- save: UPSERT (access_count 자동 증가)
- load: agent_type + project_path 기준 상위 K개 조회
- cleanup: retention_days 초과 메모리 삭제
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

from .db import get_db, init_database

_UPSERT_SQL = """
INSERT INTO agent_memories
    (agent_type, project_path, context_key, context_value, session_id)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(agent_type, project_path, context_key) DO UPDATE SET
    context_value = excluded.context_value,
    session_id = excluded.session_id,
    access_count = agent_memories.access_count + 1,
    last_accessed = CURRENT_TIMESTAMP
"""

_LOAD_WITH_PROJECT_SQL = """
SELECT * FROM agent_memories
WHERE agent_type = ? AND (project_path = ? OR project_path IS NULL)
ORDER BY access_count DESC, last_accessed DESC LIMIT ?
"""

_LOAD_ALL_SQL = """
SELECT * FROM agent_memories
WHERE agent_type = ?
ORDER BY access_count DESC, last_accessed DESC LIMIT ?
"""

_ENFORCE_LIMIT_SQL = """
DELETE FROM agent_memories WHERE id IN (
    SELECT id FROM agent_memories WHERE agent_type = ?
    ORDER BY access_count DESC, last_accessed DESC
    LIMIT -1 OFFSET ?
)
"""


@dataclass
class MemoryEntry:
    """단일 메모리 항목"""

    agent_type: str
    context_key: str
    context_value: str
    project_path: str | None = None
    session_id: str | None = None
    access_count: int = 1
    created_at: str = ""
    last_accessed: str = ""


class AgentMemory:
    """에이전트 메모리 저장소"""

    def __init__(self, max_per_agent: int = 50, retention_days: int = 30) -> None:
        self.max_per_agent = max_per_agent
        self.retention_days = retention_days
        init_database()

    def save(self, entry: MemoryEntry) -> None:
        """메모리 저장 (UPSERT - 중복 시 access_count 증가)"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(_UPSERT_SQL, (
                entry.agent_type, entry.project_path,
                entry.context_key, entry.context_value, entry.session_id,
            ))
            self._enforce_limit(cursor, entry.agent_type)

    def load(self, agent_type: str, project_path: str | None = None, top_k: int = 5) -> list[MemoryEntry]:
        """에이전트 메모리 로드 (access_count + 최신순 정렬)"""
        with get_db() as conn:
            cursor = conn.cursor()
            if project_path:
                cursor.execute(_LOAD_WITH_PROJECT_SQL, (agent_type, project_path, top_k))
            else:
                cursor.execute(_LOAD_ALL_SQL, (agent_type, top_k))

            rows = cursor.fetchall()
            ids = [row["id"] for row in rows]
            if ids:
                ph = ",".join("?" * len(ids))
                cursor.execute(f"UPDATE agent_memories SET last_accessed = CURRENT_TIMESTAMP WHERE id IN ({ph})", ids)
            return [self._row_to_entry(row) for row in rows]

    def cleanup(self) -> int:
        """retention_days 초과 메모리 삭제, 삭제 건수 반환"""
        cutoff = (datetime.now() - timedelta(days=self.retention_days)).isoformat()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM agent_memories WHERE last_accessed < ?", (cutoff,))
            return cursor.rowcount

    def format_for_prompt(self, entries: list[MemoryEntry]) -> str:
        """메모리 항목을 프롬프트 주입용 문자열로 포맷"""
        if not entries:
            return ""
        lines = ["[Agent Memory]"]
        for e in entries:
            lines.append(f"- {e.context_key}: {e.context_value}")
        return "\n".join(lines)

    def _enforce_limit(self, cursor: sqlite3.Cursor, agent_type: str) -> None:
        """에이전트별 메모리 수 제한 (초과분 삭제)"""
        cursor.execute(_ENFORCE_LIMIT_SQL, (agent_type, self.max_per_agent))

    @staticmethod
    def _row_to_entry(row: sqlite3.Row) -> MemoryEntry:
        """DB Row → MemoryEntry 변환"""
        return MemoryEntry(
            agent_type=row["agent_type"], context_key=row["context_key"],
            context_value=row["context_value"], project_path=row["project_path"],
            session_id=row["session_id"], access_count=row["access_count"],
            created_at=row["created_at"], last_accessed=row["last_accessed"],
        )
