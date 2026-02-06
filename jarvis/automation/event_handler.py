#!/usr/bin/env python3
"""
Event Handler
일정 관련 핸들러
"""

from typing import Dict, Any


class EventHandler:
    """일정 관련 핸들러"""

    def __init__(self, calendar_manager):
        self.calendar_manager = calendar_manager

    def handle_add(self, command: str) -> Dict[str, Any]:
        """일정 추가"""
        return {
            'success': False,
            'message': '일정 추가 기능은 추후 구현 예정입니다.',
            'hint': '날짜, 시간, 제목을 포함해주세요.'
        }

    def handle_list(self, command: str) -> Dict[str, Any]:
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
