#!/usr/bin/env python3
"""
컨텍스트(remember/recall) 관련 핸들러
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

if TYPE_CHECKING:
    from memory import ContextManager

from utils import build_response  # noqa: E402


def handle_remember(command: str, context_manager: ContextManager) -> dict[str, Any]:
    """
    컨텍스트 저장

    Args:
        command: 명령어
        context_manager: ContextManager 인스턴스

    Returns:
        처리 결과
    """
    # 현재 프로젝트 경로 감지
    try:
        result = subprocess.run(["pwd"], capture_output=True, text=True, check=True)
        project_path = result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        project_path = str(Path.cwd())

    context_manager.save_context(
        project_path=project_path,
        last_file="",
        last_action="manual_save",
        summary=command,
    )

    return build_response(
        success=True,
        message="현재 컨텍스트가 저장되었습니다.",
        project_path=project_path,
    )


def handle_recall(command: str, context_manager: ContextManager) -> dict[str, Any]:
    """
    컨텍스트 복원

    Args:
        command: 명령어 (미사용, 시그니처 일관성)
        context_manager: ContextManager 인스턴스

    Returns:
        처리 결과
    """
    context = context_manager.get_last_context()

    if not context:
        return build_response(
            success=False,
            message="저장된 컨텍스트가 없습니다.",
        )

    return build_response(
        success=True,
        message="마지막 컨텍스트를 찾았습니다.",
        context=context,
    )
