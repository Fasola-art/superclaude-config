#!/usr/bin/env python3
"""
Task Handlers - 할 일 관리 핸들러
"""

import re
from typing import Dict, Any
from pathlib import Path
from datetime import datetime, timedelta
import sys

jarvis_root = Path(__file__).parent.parent
sys.path.insert(0, str(jarvis_root))

from jarvis.memory.manager import TaskManager


def handle_add_task(command: str) -> Dict[str, Any]:
    """할 일 추가"""
    patterns = [r'["\'](.*?)["\']', r'추가[해줘]*\s*(.+?)(?:\s|$)']
    task_content = None

    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            task_content = match.group(1).strip()
            break

    if not task_content:
        task_content = re.sub(r'(추가|해줘|할\s*일|작업)', '', command).strip()

    due_date = None
    if '내일' in command:
        due_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    elif '오늘' in command:
        due_date = datetime.now().strftime('%Y-%m-%d')

    task_id = TaskManager.add_task(task_content, due_date=due_date)

    return {
        'success': True,
        'action': 'add_task',
        'task': task_content,
        'task_id': task_id,
        'due_date': due_date,
        'message': f"할 일 추가됨: {task_content}" + (f" (마감: {due_date})" if due_date else "")
    }


def handle_list_tasks(command: str) -> Dict[str, Any]:
    """할 일 목록 조회"""
    tasks = TaskManager.get_pending_tasks()
    return {
        'success': True,
        'action': 'list_tasks',
        'tasks': tasks,
        'count': len(tasks),
        'message': f"진행 중인 할 일 {len(tasks)}개"
    }


def handle_complete_task(command: str) -> Dict[str, Any]:
    """할 일 완료 처리"""
    match = re.search(r'(\d+)', command)
    task_id = int(match.group(1)) if match else None

    if task_id:
        TaskManager.complete_task(task_id)
        return {'success': True, 'action': 'complete_task', 'task_id': task_id}

    return {'success': False, 'error': '작업 ID를 찾을 수 없습니다'}
