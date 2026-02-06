#!/usr/bin/env python3
"""
Task Handler
작업 관련 핸들러
"""

import re
from typing import Dict, Any


class TaskHandler:
    """작업 관련 핸들러"""

    def __init__(self, task_manager):
        self.task_manager = task_manager

    def handle_add(self, command: str) -> Dict[str, Any]:
        """작업 추가"""
        # 제목 추출
        title_match = re.search(r'["\'](.+?)["\']', command)
        if title_match:
            title = title_match.group(1)
        else:
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

    def handle_list(self, command: str) -> Dict[str, Any]:
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

    def handle_complete(self, command: str) -> Dict[str, Any]:
        """작업 완료"""
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
