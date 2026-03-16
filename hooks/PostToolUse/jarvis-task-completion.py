#!/usr/bin/env python3
"""
jarvis-task-completion.py - 태스크 완료 추적 훅 (60줄)
Trigger: PostToolUse | Matcher: TaskUpdate|TodoWrite | Timeout: 5000ms
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Dict

sys.path.insert(0, str(Path.home() / '.claude'))
from jarvis.core import safe_load_json, atomic_write_json, ensure_dir, run_hook

JARVIS_DIR = Path.home() / '.claude/jarvis'
COMPLETIONS_FILE = JARVIS_DIR / 'task-completions.json'
DEFAULT_DATA = {
    'totalCompleted': 0, 'todayCompleted': 0, 'lastCompletedAt': None,
    'completionHistory': [], 'streaks': {'current': 0, 'best': 0, 'lastDate': None}
}


def is_completion_event(data: Dict[str, Any]) -> bool:
    if data.get('tool') == 'TaskUpdate':
        return data.get('status') == 'completed'
    if data.get('tool') == 'TodoWrite':
        todos = data.get('todos', [])
        return any(isinstance(t, dict) and t.get('status') == 'completed' for t in todos)
    return False


def update_streaks(streaks: Dict[str, Any]) -> Dict[str, Any]:
    today = datetime.now().date().isoformat()
    if streaks.get('lastDate') == today:
        return streaks
    yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
    streaks['current'] = streaks['current'] + 1 if streaks.get('lastDate') == yesterday else 1
    streaks['lastDate'] = today
    streaks['best'] = max(streaks['current'], streaks.get('best', 0))
    return streaks


def process_completion(data: Dict[str, Any]) -> Dict[str, Any]:
    if not is_completion_event(data):
        return {'status': 'skipped', 'message': 'Not a completion event'}

    comp = safe_load_json(COMPLETIONS_FILE, DEFAULT_DATA.copy())
    now = datetime.now()
    today = now.date().isoformat()

    if (comp.get('lastCompletedAt') or '')[:10] != today:
        comp['todayCompleted'] = 0

    comp['totalCompleted'] += 1
    comp['todayCompleted'] += 1
    comp['lastCompletedAt'] = now.isoformat()
    comp['streaks'] = update_streaks(comp.get('streaks', DEFAULT_DATA['streaks'].copy()))
    comp['completionHistory'] = comp.get('completionHistory', [])[-99:]

    ensure_dir(JARVIS_DIR)
    atomic_write_json(COMPLETIONS_FILE, comp)

    return {
        'status': 'completed', 'totalCompleted': comp['totalCompleted'],
        'todayCompleted': comp['todayCompleted'], 'streak': comp['streaks']['current']
    }


if __name__ == '__main__':
    run_hook(process_completion)
