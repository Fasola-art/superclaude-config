#!/usr/bin/env python3
"""Remember 기능 - 작업 컨텍스트 저장"""

from __future__ import annotations

import os
from typing import Optional
from pathlib import Path

from memory.db import get_db
from memory.context import ContextManager


def save_context(
    project_path: str,
    summary: str,
    tags: Optional[list[str]] = None,
    last_file: Optional[str] = None,
    last_action: Optional[str] = None,
) -> int:
    """
    작업 컨텍스트 저장

    Args:
        project_path: 프로젝트 경로
        summary: 작업 요약 (Claude 대화 요약)
        tags: 태그 리스트 (검색용, summary에 추가)
        last_file: 마지막 작업 파일
        last_action: 마지막 수행 액션

    Returns:
        생성된 context ID
    """
    project_path = str(Path(project_path).resolve())

    # 태그를 summary에 추가
    full_summary = summary
    if tags:
        full_summary += f"\nTags: {', '.join(tags)}"

    # ContextManager 활용하여 저장
    ContextManager.save_context(
        project_path=project_path,
        last_file=last_file or "",
        last_action=last_action or "",
        summary=full_summary
    )

    # 방금 생성한 ID 반환
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM context_snapshots WHERE project_path = ? "
            "ORDER BY created_at DESC LIMIT 1",
            (project_path,)
        )
        result = cursor.fetchone()
        return result[0] if result else -1


def save_quick_context(summary: str, tags: Optional[list[str]] = None) -> int:
    """
    빠른 컨텍스트 저장 (현재 디렉토리 기준)

    Args:
        summary: 작업 요약
        tags: 태그 리스트

    Returns:
        생성된 context ID
    """
    return save_context(
        project_path=os.getcwd(),
        summary=summary,
        tags=tags,
        last_action="quick_save"
    )
