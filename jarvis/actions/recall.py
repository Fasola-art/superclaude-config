#!/usr/bin/env python3
"""Recall 기능 - 저장된 컨텍스트 조회"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

from memory.db import get_db
from memory.context import ContextManager


def get_last_context(project_path: Optional[str] = None) -> Optional[dict]:
    """최근 컨텍스트 조회 (project_path=None이면 전체 최근)"""
    if project_path:
        project_path = str(Path(project_path).resolve())
    result = ContextManager.get_last_context(project_path)
    return dict(result) if result else None


def get_contexts_by_tag(tag: str) -> list[dict]:
    """태그로 컨텍스트 검색 (summary에서 태그 검색)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM context_snapshots WHERE conversation_summary LIKE ? "
            "ORDER BY created_at DESC",
            (f"%{tag}%",)
        )
        return [dict(row) for row in cursor.fetchall()]


def get_recent_contexts(limit: int = 10, project_path: Optional[str] = None) -> list[dict]:
    """최근 N개 컨텍스트 조회"""
    with get_db() as conn:
        cursor = conn.cursor()

        if project_path:
            project_path = str(Path(project_path).resolve())
            query = "SELECT * FROM context_snapshots WHERE project_path = ? ORDER BY created_at DESC LIMIT ?"
            params = (project_path, limit)
        else:
            query = "SELECT * FROM context_snapshots ORDER BY created_at DESC LIMIT ?"
            params = (limit,)

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def search_contexts(keyword: str) -> list[dict]:
    """키워드로 전체 검색 (summary, last_file, last_action)"""
    pattern = f"%{keyword}%"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM context_snapshots "
            "WHERE conversation_summary LIKE ? OR last_file LIKE ? OR last_action LIKE ? "
            "ORDER BY created_at DESC",
            (pattern, pattern, pattern)
        )
        return [dict(row) for row in cursor.fetchall()]
