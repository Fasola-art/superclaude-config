#!/usr/bin/env python3
"""
Intent Analyzer
명령어 의도 분석
"""

import re
from typing import Dict, Any


class IntentAnalyzer:
    """명령어 의도 분석기"""

    def __init__(self):
        self.patterns = {
            'add_task': [
                r'추가[해줘]*',
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
            ],
            'github_check': [
                r'github.*확인',
                r'pr.*확인',
                r'pull.*request',
                r'깃허브.*체크'
            ],
            'file_operation': [
                r'파일.*생성',
                r'파일.*수정',
                r'파일.*삭제',
                r'file.*create',
                r'file.*edit'
            ]
        }

    def analyze(self, command: str) -> Dict[str, Any]:
        """명령어 의도 분석"""
        command_lower = command.lower()

        for intent, pattern_list in self.patterns.items():
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
