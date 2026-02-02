#!/usr/bin/env python3
"""
작업(Task) 관련 핸들러
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

# JARVIS 루트를 sys.path에 추가 (중복 방지)
_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

if TYPE_CHECKING:
    from memory import TaskManager

from utils import parse_title, extract_id, build_response  # noqa: E402


# 제목 추출 시 제거할 키워드
TASK_KEYWORDS = [
    r"할\s*일",
    r"작업",
    r"추가",
    r"해줘",
    r"해주세요",
]


def handle_add_task(command: str, task_manager: TaskManager) -> dict[str, Any]:
    """
    작업 추가 처리

    Args:
        command: 명령어
        task_manager: TaskManager 인스턴스

    Returns:
        처리 결과
    """
    title = parse_title(command, TASK_KEYWORDS)

    if not title:
        return build_response(
            success=False,
            message="작업 제목을 인식하지 못했습니다.",
            hint='"작업 제목" 추가해줘 형식으로 입력해주세요.',
        )

    task_id = task_manager.add_task(title)

    return build_response(
        success=True,
        message=f'작업이 추가되었습니다: "{title}"',
        task_id=task_id,
    )


def handle_list_tasks(command: str, task_manager: TaskManager) -> dict[str, Any]:
    """
    작업 목록 조회

    Args:
        command: 명령어 (미사용, 시그니처 일관성)
        task_manager: TaskManager 인스턴스

    Returns:
        처리 결과
    """
    tasks = task_manager.get_pending_tasks()

    if not tasks:
        return build_response(
            success=True,
            message="진행 중인 작업이 없습니다.",
            tasks=[],
        )

    return build_response(
        success=True,
        message=f"{len(tasks)}개의 작업이 있습니다.",
        tasks=tasks,
    )


def handle_complete_task(command: str, task_manager: TaskManager) -> dict[str, Any]:
    """
    작업 완료 처리

    Args:
        command: 명령어
        task_manager: TaskManager 인스턴스

    Returns:
        처리 결과
    """
    task_id = extract_id(command)

    if task_id is None:
        return build_response(
            success=False,
            message="완료할 작업 ID를 인식하지 못했습니다.",
            hint="작업 ID 번호를 포함해주세요.",
        )

    task_manager.complete_task(task_id)

    return build_response(
        success=True,
        message=f"작업 #{task_id}가 완료되었습니다.",
    )
