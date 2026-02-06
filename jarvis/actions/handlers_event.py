#!/usr/bin/env python3
"""
Event Handlers - 일정 관리 핸들러
"""

import re
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import sys

jarvis_root = Path(__file__).parent.parent
sys.path.insert(0, str(jarvis_root))

from memory.manager import CalendarManager


def handle_add_event(command: str) -> Dict[str, Any]:
    """일정 추가"""
    match = re.search(r'["\'](.*?)["\']', command)
    event_title = match.group(1) if match else "새 일정"

    time_match = re.search(r'(\d{1,2}):(\d{2})', command)
    event_time = datetime.now().strftime('%Y-%m-%d')

    if time_match:
        event_time += f" {time_match.group(1)}:{time_match.group(2)}:00"
    else:
        event_time += " 09:00:00"

    event_id = CalendarManager.add_event(event_title, event_time)

    return {'success': True, 'action': 'add_event', 'event': event_title, 'event_id': event_id}


def handle_list_events(command: str) -> Dict[str, Any]:
    """일정 목록 조회"""
    events = CalendarManager.get_today_events()
    return {'success': True, 'action': 'list_events', 'events': events, 'count': len(events)}
