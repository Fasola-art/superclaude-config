#!/usr/bin/env python3
"""
Extended Command Handlers
컨텍스트, 예약, 계획 핸들러
"""

import subprocess
from pathlib import Path
from typing import Dict, Any


class ContextHandler:
    """컨텍스트 관련 핸들러"""

    def __init__(self, context_manager):
        self.context_manager = context_manager

    def handle_remember(self, command: str) -> Dict[str, Any]:
        """컨텍스트 저장"""
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

    def handle_recall(self, command: str) -> Dict[str, Any]:
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


class BookingHandler:
    """예약 핸들러"""

    def handle(self, command: str) -> Dict[str, Any]:
        """예약 처리"""
        return {
            'success': False,
            'message': '예약 기능은 추후 구현 예정입니다.',
            'hint': '/j book 레스토랑명 날짜 시간 형식으로 사용 예정'
        }


class PlanningHandler:
    """계획 핸들러"""

    def handle(self, command: str) -> Dict[str, Any]:
        """계획 수립"""
        return {
            'success': False,
            'message': '계획 수립 기능은 추후 구현 예정입니다.',
            'hint': '/j plan 이벤트명 형식으로 사용 예정'
        }


class UnknownHandler:
    """알 수 없는 명령 핸들러"""

    def handle(self, command: str) -> Dict[str, Any]:
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
