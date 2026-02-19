#!/usr/bin/env python3
"""Search 기능 - 통합 검색"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Optional

from jarvis.memory.db import get_db


def search_web(query: str) -> str:
    """
    웹 검색 (기본 브라우저로 Google 검색)

    Args:
        query: 검색어

    Returns:
        실행 결과 메시지
    """
    import urllib.parse
    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded}"
    subprocess.run(["open", url], check=True)
    return f"웹 검색 실행: {query}"


def search_local(query: str, path: Optional[str] = None) -> list[str]:
    """
    로컬 파일 검색 (Spotlight 활용)

    Args:
        query: 검색어
        path: 검색 경로 (None이면 홈 디렉토리)

    Returns:
        검색 결과 파일 경로 리스트
    """
    search_path = path or str(Path.home())

    result = subprocess.run(
        ["mdfind", "-onlyin", search_path, query],
        capture_output=True,
        text=True,
        check=True
    )

    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return files[:20]  # 최대 20개


def search_memory(query: str, limit: int = 10) -> list[dict]:
    """
    JARVIS 메모리 검색 (context_snapshots)

    Args:
        query: 검색어
        limit: 결과 개수 제한

    Returns:
        매칭된 컨텍스트 리스트
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, project_path, conversation_summary, created_at
            FROM context_snapshots
            WHERE conversation_summary LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (f"%{query}%", limit))

        return [dict(zip([c[0] for c in cursor.description], row))
                for row in cursor.fetchall()]


def search_all(query: str, local_path: Optional[str] = None) -> dict:
    """
    통합 검색 (메모리 + 로컬 파일)

    Args:
        query: 검색어
        local_path: 로컬 검색 경로 (선택)

    Returns:
        {
            "memory": [...],
            "local": [...]
        }
    """
    return {
        "memory": search_memory(query),
        "local": search_local(query, local_path)
    }
