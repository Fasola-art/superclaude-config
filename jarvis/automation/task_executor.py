#!/usr/bin/env python3
"""
JARVIS Task Executor
자율 작업 실행 엔진
"""

from pathlib import Path
from typing import Dict, Any
import sys

# memory 모듈 경로 추가
memory_path = Path(__file__).parent.parent / "memory"
if str(memory_path) not in sys.path:
    sys.path.insert(0, str(memory_path))

from jarvis.memory.manager import TaskManager, CalendarManager, ContextManager

from .intent_analyzer import IntentAnalyzer
from .handlers import (
    TaskHandler,
    EventHandler,
    ContextHandler,
    BookingHandler,
    PlanningHandler,
    UnknownHandler,
)


class TaskExecutor:
    """작업 실행 엔진"""

    def __init__(self):
        self.task_manager = TaskManager()
        self.calendar_manager = CalendarManager()
        self.context_manager = ContextManager()
        self.intent_analyzer = IntentAnalyzer()

        # 핸들러 매핑
        self.task_handler = TaskHandler(self.task_manager)
        self.event_handler = EventHandler(self.calendar_manager)
        self.context_handler = ContextHandler(self.context_manager)
        self.booking_handler = BookingHandler()
        self.planning_handler = PlanningHandler()
        self.unknown_handler = UnknownHandler()

    def execute(self, command: str) -> Dict[str, Any]:
        """명령 실행"""
        intent_result = self.intent_analyzer.analyze(command)
        intent = intent_result['intent']

        handlers = {
            'add_task': self.task_handler.handle_add,
            'list_tasks': self.task_handler.handle_list,
            'complete_task': self.task_handler.handle_complete,
            'add_event': self.event_handler.handle_add,
            'list_events': self.event_handler.handle_list,
            'remember': self.context_handler.handle_remember,
            'recall': self.context_handler.handle_recall,
            'booking': self.booking_handler.handle,
            'planning': self.planning_handler.handle,
        }

        handler = handlers.get(intent, self.unknown_handler.handle)
        return handler(command)


# 싱글톤 인스턴스
_executor = None


def get_executor() -> TaskExecutor:
    """TaskExecutor 싱글톤 반환"""
    global _executor
    if _executor is None:
        _executor = TaskExecutor()
    return _executor


if __name__ == "__main__":
    import json

    executor = get_executor()

    # 테스트
    tests = [
        "할 일 목록 보여줘",
        '"API 리팩토링" 작업 추가해줘',
        "어디까지 했더라",
        "기억해줘"
    ]

    print("=== JARVIS Task Executor Test ===\n")

    for test in tests:
        print(f"Input: {test}")
        result = executor.execute(test)
        print(f"Result: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print()
