#!/usr/bin/env python3
"""
JARVIS Do - 자율실행 명령어 인터페이스
자연어 명령을 파싱하고 적절한 액션 실행
"""

from pathlib import Path
from typing import Dict, Any
import sys

# 상위 모듈 경로 추가
jarvis_root = Path(__file__).parent.parent
if str(jarvis_root) not in sys.path:
    sys.path.insert(0, str(jarvis_root))

from automation.intent_analyzer import IntentAnalyzer
from .do_handlers import (
    handle_add_task,
    handle_list_tasks,
    handle_complete_task,
    handle_add_event,
    handle_list_events,
    handle_remember,
    handle_recall,
    handle_github_check,
    handle_file_operation,
    handle_unknown
)


class DoExecutor:
    """Do 명령 실행기"""

    def __init__(self):
        self.intent_analyzer = IntentAnalyzer()
        self.handler_map = {
            'add_task': handle_add_task,
            'list_tasks': handle_list_tasks,
            'complete_task': handle_complete_task,
            'add_event': handle_add_event,
            'list_events': handle_list_events,
            'remember': handle_remember,
            'recall': handle_recall,
            'github_check': handle_github_check,
            'file_operation': handle_file_operation,
        }

    def execute(self, command: str) -> Dict[str, Any]:
        """자연어 명령 실행"""
        # 의도 파악
        intent_result = self.intent_analyzer.analyze(command)
        intent = intent_result['intent']

        # 적절한 핸들러 선택
        handler = self.handler_map.get(intent, handle_unknown)

        # 핸들러 실행
        return handler(command)


# 싱글톤 인스턴스
_executor = None


def execute_command(command: str) -> Dict[str, Any]:
    """
    자연어 명령 실행 (진입점)

    Args:
        command: 자연어 명령어 (예: "내일까지 보고서 작성 추가해줘")

    Returns:
        실행 결과 딕셔너리
    """
    global _executor
    if _executor is None:
        _executor = DoExecutor()

    return _executor.execute(command)


if __name__ == "__main__":
    import json

    # 테스트 케이스
    test_cases = [
        "내일까지 보고서 작성 추가해줘",
        "할 일 목록 보여줘",
        "GitHub PR 확인해줘",
        "오늘 일정 보여줘",
        "지금까지 작업 내용 기억해줘",
        "어디까지 했더라",
    ]

    print("=== JARVIS Do Executor Test ===\n")

    for test in test_cases:
        print(f"Command: {test}")
        result = execute_command(test)
        print(f"Result: {json.dumps(result, ensure_ascii=False, indent=2)}\n")
