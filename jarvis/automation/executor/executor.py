#!/usr/bin/env python3
"""
TaskExecutor 메인 클래스
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# 상대 임포트 (패키지 구조 사용)
from .intent_analyzer import analyze_intent
from .patterns import AVAILABLE_COMMANDS
from .task_handler import handle_add_task, handle_list_tasks, handle_complete_task
from .event_handler import handle_add_event, handle_list_events
from .context_handler import handle_remember, handle_recall
from .booking_handler import handle_booking, handle_planning

# JARVIS 루트 경로 추가 (memory 패키지 임포트용)
_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from memory import TaskManager, CalendarManager, ContextManager  # noqa: E402


class TaskExecutor:
    """작업 실행 엔진"""

    def __init__(self) -> None:
        self.task_manager = TaskManager()
        self.calendar_manager = CalendarManager()
        self.context_manager = ContextManager()

    def analyze_intent(self, command: str) -> dict[str, Any]:
        """명령어 의도 분석"""
        result = analyze_intent(command)
        return {
            "intent": result.intent,
            "command": result.command,
            "confidence": result.confidence,
        }

    def execute(self, command: str) -> dict[str, Any]:
        """명령 실행"""
        intent_result = analyze_intent(command)
        intent = intent_result.intent

        handlers = {
            "add_task": lambda c: handle_add_task(c, self.task_manager),
            "list_tasks": lambda c: handle_list_tasks(c, self.task_manager),
            "complete_task": lambda c: handle_complete_task(c, self.task_manager),
            "add_event": lambda c: handle_add_event(c, self.calendar_manager),
            "list_events": lambda c: handle_list_events(c, self.calendar_manager),
            "remember": lambda c: handle_remember(c, self.context_manager),
            "recall": lambda c: handle_recall(c, self.context_manager),
            "booking": handle_booking,
            "planning": handle_planning,
        }

        handler = handlers.get(intent, self._handle_unknown)
        return handler(command)

    def _handle_unknown(self, command: str) -> dict[str, Any]:
        """알 수 없는 명령"""
        return {
            "success": False,
            "message": "명령을 이해하지 못했습니다.",
            "available_commands": AVAILABLE_COMMANDS,
        }


# 싱글톤 인스턴스
_executor: TaskExecutor | None = None


def get_executor() -> TaskExecutor:
    """TaskExecutor 싱글톤 반환"""
    global _executor
    if _executor is None:
        _executor = TaskExecutor()
    return _executor
