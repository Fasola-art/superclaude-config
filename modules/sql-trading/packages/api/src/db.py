"""
DB 커넥션 풀 관리

psycopg2 ThreadedConnectionPool 기반
"""
import os
from contextlib import contextmanager
from typing import Any, Dict, Generator, List

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor


# 커넥션 풀 (최소 2, 최대 10)
_pool: pool.ThreadedConnectionPool | None = None


def get_pool() -> pool.ThreadedConnectionPool:
    """커넥션 풀 가져오기 (lazy init)"""
    global _pool
    if _pool is None:
        _pool = pool.ThreadedConnectionPool(
            minconn=2,
            maxconn=10,
            dbname=os.getenv("DB_NAME", "claude_mcp"),
            user=os.getenv("DB_USER", "reim"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
        )
    return _pool


@contextmanager
def get_conn() -> Generator:
    """커넥션 컨텍스트 매니저"""
    p = get_pool()
    conn = p.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        p.putconn(conn)


def fetch_all(sql: str, params: tuple | None = None) -> List[Dict[str, Any]]:
    """쿼리 실행 → dict 리스트 반환"""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]


def fetch_one(sql: str, params: tuple | None = None) -> Dict[str, Any] | None:
    """단일 행 조회"""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            return dict(row) if row else None


def execute(sql: str, params: tuple | None = None) -> int:
    """INSERT/UPDATE/DELETE 실행 → 영향 행 수 반환"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount


def close_pool() -> None:
    """풀 종료"""
    global _pool
    if _pool is not None:
        _pool.closeall()
        _pool = None
