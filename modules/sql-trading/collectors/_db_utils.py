#!/usr/bin/env python3
"""
공통 DB 유틸리티

로컬: psql 바이너리 사용
Docker: psycopg2 사용 (환경변수 DB_HOST 감지)
"""
from __future__ import annotations

import os
import subprocess

# Docker 환경 감지 (DB_HOST 환경변수가 있으면 psycopg2 사용)
_USE_PSYCOPG2 = bool(os.getenv("DB_HOST"))

PSQL = "/opt/homebrew/opt/postgresql@16/bin/psql"
DB = os.getenv("DB_NAME", "claude_mcp")
DB_USER = os.getenv("DB_USER", "reim")
DB_PASS = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))


def _get_conn():
    """psycopg2 커넥션 (Docker용)"""
    import psycopg2
    return psycopg2.connect(
        dbname=DB, user=DB_USER, password=DB_PASS,
        host=DB_HOST, port=DB_PORT,
    )


def run_sql(sql: str) -> bool:
    """SQL 실행 (INSERT/UPDATE/DELETE)"""
    if _USE_PSYCOPG2:
        try:
            conn = _get_conn()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception:
            return False
    result = subprocess.run(
        [PSQL, "-U", DB_USER, "-d", DB, "-c", sql],
        capture_output=True, text=True, timeout=30,
    )
    return result.returncode == 0


def count_table(table: str) -> int:
    """테이블 데이터 건수 확인"""
    if _USE_PSYCOPG2:
        try:
            conn = _get_conn()
            cur = conn.cursor()
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            val = cur.fetchone()[0]
            cur.close()
            conn.close()
            return int(val)
        except Exception:
            return 0
    result = subprocess.run(
        [PSQL, "-U", DB_USER, "-d", DB, "-t", "-c",
         f"SELECT COUNT(*) FROM {table};"],
        capture_output=True, text=True, timeout=10,
    )
    return int(result.stdout.strip()) if result.returncode == 0 else 0


def query_rows(sql: str) -> list[str]:
    """쿼리 실행, 파이프 구분 결과 행 리스트 반환"""
    if _USE_PSYCOPG2:
        try:
            conn = _get_conn()
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return ["|".join(str(c) if c is not None else "" for c in row) for row in rows]
        except Exception:
            return []
    result = subprocess.run(
        [PSQL, "-U", DB_USER, "-d", DB, "-t", "-A", "-c", sql],
        capture_output=True, text=True, timeout=10,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.strip().split("\n") if line]


def escape_sql(text: str) -> str:
    """SQL 문자열 이스케이프"""
    if not text:
        return ""
    return text.replace("'", "''").replace("\\", "\\\\")
