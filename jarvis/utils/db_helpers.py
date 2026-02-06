#!/usr/bin/env python3
"""
데이터베이스 공통 헬퍼 함수
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from memory.db import get_db


def execute_query(
    query: str,
    params: tuple = (),
    fetch_one: bool = False
) -> Optional[Dict[str, Any]]:
    """
    단일 쿼리 실행 및 결과 반환

    Args:
        query: SQL 쿼리
        params: 쿼리 파라미터
        fetch_one: True시 단일 결과만 반환

    Returns:
        Dict 또는 None
    """
    from memory.db import get_db

    with get_db() as conn:
        cursor = conn.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None if fetch_one else {}


def execute_query_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    쿼리 실행 및 모든 결과 반환

    Args:
        query: SQL 쿼리
        params: 쿼리 파라미터

    Returns:
        Dict 리스트
    """
    from memory.db import get_db

    with get_db() as conn:
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def execute_insert(query: str, params: tuple) -> int:
    """
    INSERT 쿼리 실행 및 lastrowid 반환

    Args:
        query: INSERT SQL
        params: 쿼리 파라미터

    Returns:
        삽입된 행의 ID
    """
    from memory.db import get_db

    with get_db() as conn:
        cursor = conn.execute(query, params)
        return cursor.lastrowid or 0
