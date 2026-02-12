#!/usr/bin/env python3
"""
공통 DB 유틸리티

모든 수집기에서 공유하는 psql 실행 함수
"""

import subprocess
from pathlib import Path

PSQL = "/opt/homebrew/opt/postgresql@16/bin/psql"
DB = "claude_mcp"


def run_sql(sql: str) -> bool:
    """psql로 SQL 실행"""
    result = subprocess.run(
        [PSQL, "-U", "reim", "-d", DB, "-c", sql],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0


def count_table(table: str) -> int:
    """테이블 데이터 건수 확인"""
    result = subprocess.run(
        [PSQL, "-U", "reim", "-d", DB, "-t", "-c",
         f"SELECT COUNT(*) FROM {table};"],
        capture_output=True, text=True, timeout=10
    )
    return int(result.stdout.strip()) if result.returncode == 0 else 0


def query_rows(sql: str) -> list[str]:
    """psql로 쿼리 실행, 결과 행 리스트 반환"""
    result = subprocess.run(
        [PSQL, "-U", "reim", "-d", DB, "-t", "-A", "-c", sql],
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
