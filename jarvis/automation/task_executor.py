#!/usr/bin/env python3
"""
JARVIS Task Executor
자율 작업 실행 엔진
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, Any

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "memory"))
from manager import TaskManager, CalendarManager, ContextManager


class TaskExecutor:
    """작업 실행 엔진"""

    def __init__(self):
        self.task_manager = TaskManager()
        self.calendar_manager = CalendarManager()
        self.context_manager = ContextManager()

    def analyze_intent(self, command: str) -> Dict[str, Any]:
        """명령어 의도 분석"""
        command_lower = command.lower()

        # 패턴 매칭으로 의도 파악
        patterns = {
            'add_task': [
                r'할\s*일.*추가',
                r'작업.*추가',
                r'todo.*add',
                r'task.*create'
            ],
            'list_tasks': [
                r'할\s*일.*보여',
                r'작업.*목록',
                r'todo.*list',
                r'tasks?.*show'
            ],
            'complete_task': [
                r'완료.*표시',
                r'끝났',
                r'done',
                r'complete'
            ],
            'add_event': [
                r'일정.*추가',
                r'약속.*잡',
                r'미팅.*예약',
                r'event.*add'
            ],
            'list_events': [
                r'일정.*보여',
                r'오늘.*일정',
                r'스케줄',
                r'calendar'
            ],
            'remember': [
                r'기억해',
                r'저장해',
                r'컨텍스트.*저장',
                r'remember'
            ],
            'recall': [
                r'어디까지',
                r'마지막.*작업',
                r'이어서',
                r'recall',
                r'continue'
            ],
            'booking': [
                r'예약',
                r'book',
                r'reservation'
            ],
            'planning': [
                r'계획',
                r'plan',
                r'일정.*짜'
            ]
        }

        for intent, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, command_lower):
                    return {
                        'intent': intent,
                        'command': command,
                        'confidence': 0.8
                    }

        return {
            'intent': 'unknown',
            'command': command,
            'confidence': 0.0
        }

    def execute(self, command: str) -> Dict[str, Any]:
        """명령 실행"""
        intent_result = self.analyze_intent(command)
        intent = intent_result['intent']

        handlers = {
            'add_task': self._handle_add_task,
            'list_tasks': self._handle_list_tasks,
            'complete_task': self._handle_complete_task,
            'add_event': self._handle_add_event,
            'list_events': self._handle_list_events,
            'remember': self._handle_remember,
            'recall': self._handle_recall,
            'booking': self._handle_booking,
            'planning': self._handle_planning,
        }

        handler = handlers.get(intent, self._handle_unknown)
        return handler(command)

    def _handle_add_task(self, command: str) -> Dict[str, Any]:
        """작업 추가 처리"""
        # 간단한 파싱 (실제로는 더 정교한 NLP 필요)
        # 예: "내일까지 보고서 작성 할 일 추가해줘"

        # 제목 추출 시도
        title_match = re.search(r'["\'](.+?)["\']', command)
        if title_match:
            title = title_match.group(1)
        else:
            # 키워드 제거 후 제목으로 사용
            title = re.sub(r'(할\s*일|작업|추가|해줘|해주세요)', '', command).strip()

        if not title:
            return {
                'success': False,
                'message': '작업 제목을 인식하지 못했습니다.',
                'hint': '"작업 제목" 추가해줘 형식으로 입력해주세요.'
            }

        task_id = self.task_manager.add_task(title)

        return {
            'success': True,
            'message': f'작업이 추가되었습니다: "{title}"',
            'task_id': task_id
        }

    def _handle_list_tasks(self, command: str) -> Dict[str, Any]:
        """작업 목록 조회"""
        tasks = self.task_manager.get_pending_tasks()

        if not tasks:
            return {
                'success': True,
                'message': '진행 중인 작업이 없습니다.',
                'tasks': []
            }

        return {
            'success': True,
            'message': f'{len(tasks)}개의 작업이 있습니다.',
            'tasks': tasks
        }

    def _handle_complete_task(self, command: str) -> Dict[str, Any]:
        """작업 완료 처리"""
        # 숫자(ID) 추출 시도
        id_match = re.search(r'(\d+)', command)

        if not id_match:
            return {
                'success': False,
                'message': '완료할 작업 ID를 인식하지 못했습니다.',
                'hint': '작업 ID 번호를 포함해주세요.'
            }

        task_id = int(id_match.group(1))
        self.task_manager.complete_task(task_id)

        return {
            'success': True,
            'message': f'작업 #{task_id}가 완료되었습니다.'
        }

    def _handle_add_event(self, command: str) -> Dict[str, Any]:
        """일정 추가"""
        return {
            'success': False,
            'message': '일정 추가 기능은 추후 구현 예정입니다.',
            'hint': '날짜, 시간, 제목을 포함해주세요.'
        }

    def _handle_list_events(self, command: str) -> Dict[str, Any]:
        """일정 조회"""
        events = self.calendar_manager.get_today_events()

        if not events:
            return {
                'success': True,
                'message': '오늘 예정된 일정이 없습니다.',
                'events': []
            }

        return {
            'success': True,
            'message': f'오늘 {len(events)}개의 일정이 있습니다.',
            'events': events
        }

    def _handle_remember(self, command: str) -> Dict[str, Any]:
        """컨텍스트 저장"""
        # 현재 프로젝트 경로 감지 시도
        try:
            result = subprocess.run(['pwd'], capture_output=True, text=True)
            project_path = result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            project_path = str(Path.cwd())

        self.context_manager.save_context(
            project_path=project_path,
            last_file="",
            last_action="manual_save",
            summary=command
        )

        return {
            'success': True,
            'message': '현재 컨텍스트가 저장되었습니다.',
            'project_path': project_path
        }

    def _handle_recall(self, command: str) -> Dict[str, Any]:
        """컨텍스트 복원"""
        context = self.context_manager.get_last_context()

        if not context:
            return {
                'success': False,
                'message': '저장된 컨텍스트가 없습니다.'
            }

        return {
            'success': True,
            'message': '마지막 컨텍스트를 찾았습니다.',
            'context': context
        }

    def _handle_booking(self, command: str) -> Dict[str, Any]:
        """예약 처리"""
        return {
            'success': False,
            'message': '예약 기능은 추후 구현 예정입니다.',
            'hint': '/j book 레스토랑명 날짜 시간 형식으로 사용 예정'
        }

    def _handle_planning(self, command: str) -> Dict[str, Any]:
        """계획 수립"""
        return {
            'success': False,
            'message': '계획 수립 기능은 추후 구현 예정입니다.',
            'hint': '/j plan 이벤트명 형식으로 사용 예정'
        }

    def _handle_unknown(self, command: str) -> Dict[str, Any]:
        """알 수 없는 명령"""
        return {
            'success': False,
            'message': '명령을 이해하지 못했습니다.',
            'available_commands': [
                '/j briefing - 상세 브리핑',
                '/j remember - 작업 연속성 저장',
                '/j do <작업> - 자율 작업 수행',
                '/j book <예약> - 예약하기',
                '/j plan <이벤트> - 계획 수립'
            ]
        }


# 싱글톤 인스턴스
_executor = None

def get_executor() -> TaskExecutor:
    """TaskExecutor 싱글톤 반환"""
    global _executor
    if _executor is None:
        _executor = TaskExecutor()
    return _executor


if __name__ == "__main__":
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
