#!/usr/bin/env python3
"""
일정(Event) 관련 핸들러
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

if TYPE_CHECKING:
    from memory import CalendarManager

from utils import build_response  # noqa: E402


def handle_add_event(command: str, calendar_manager: CalendarManager) -> dict[str, Any]:
    """
    일정 추가 처리

    Args:
        command: 명령어
        calendar_manager: CalendarManager 인스턴스

    Returns:
        처리 결과

    Note:
        추후 NLU 모듈과 연동하여 날짜/시간/제목 파싱 구현 예정
    """
    return build_response(
        success=False,
        message="일정 추가 기능은 추후 구현 예정입니다.",
        hint="날짜, 시간, 제목을 포함해주세요.",
    )


def handle_list_events(command: str, calendar_manager: CalendarManager) -> dict[str, Any]:
    """
    일정 조회

    Args:
        command: 명령어 (미사용, 시그니처 일관성)
        calendar_manager: CalendarManager 인스턴스

    Returns:
        처리 결과
    """
    events = calendar_manager.get_today_events()

    if not events:
        return build_response(
            success=True,
            message="오늘 예정된 일정이 없습니다.",
            events=[],
        )

    return build_response(
        success=True,
        message=f"오늘 {len(events)}개의 일정이 있습니다.",
        events=events,
    )
