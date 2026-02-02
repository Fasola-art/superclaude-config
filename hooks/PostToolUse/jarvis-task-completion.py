#!/usr/bin/env python3
"""
jarvis-task-completion.py
Jarvis task completion handling hook

Trigger: PostToolUse
Matcher: TaskUpdate|TodoWrite
Timeout: 5000ms
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

CLAUDE_DIR = Path.home() / '.claude'
JARVIS_DIR = CLAUDE_DIR / 'jarvis'
COMPLETIONS_FILE = JARVIS_DIR / 'task-completions.json'
DAILY_REPORT_DIR = JARVIS_DIR / 'daily-reports'

def ensure_dirs():
    """Create directories"""
    JARVIS_DIR.mkdir(parents=True, exist_ok=True)
    DAILY_REPORT_DIR.mkdir(parents=True, exist_ok=True)

def load_completions() -> Dict:
    """Load completion records"""
    if COMPLETIONS_FILE.exists():
        try:
            return json.loads(COMPLETIONS_FILE.read_text())
        except Exception:
            pass

    return {
        'totalCompleted': 0,
        'todayCompleted': 0,
        'lastCompletedAt': None,
        'completionHistory': [],
        'streaks': {
            'current': 0,
            'best': 0,
            'lastDate': None
        }
    }

def save_completions(data: Dict):
    """Save completion records"""
    ensure_dirs()
    COMPLETIONS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

def update_streaks(completions: Dict) -> Dict:
    """Update consecutive completion records"""
    today = datetime.now().date().isoformat()
    streaks = completions['streaks']

    if streaks['lastDate'] == today:
        # Already updated today
        return streaks

    from datetime import timedelta
    yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()

    if streaks['lastDate'] == yesterday:
        # Streak continues
        streaks['current'] += 1
    elif streaks['lastDate'] != today:
        # Streak broken
        streaks['current'] = 1

    streaks['lastDate'] = today

    if streaks['current'] > streaks['best']:
        streaks['best'] = streaks['current']

    return streaks

def is_completion_event(data: Dict) -> bool:
    """Check if this is a completion event"""
    # TaskUpdate with completed status
    if data.get('tool') == 'TaskUpdate':
        return data.get('status') == 'completed'

    # Check completed items in TodoWrite
    if data.get('tool') == 'TodoWrite':
        todos = data.get('todos', [])
        return any(t.get('status') == 'completed' for t in todos)

    return False

def extract_task_info(data: Dict) -> Optional[Dict]:
    """Extract task information"""
    if data.get('tool') == 'TaskUpdate':
        return {
            'taskId': data.get('taskId'),
            'subject': data.get('subject', 'Unknown Task'),
            'type': 'task'
        }

    if data.get('tool') == 'TodoWrite':
        completed = [t for t in data.get('todos', []) if t.get('status') == 'completed']
        if completed:
            return {
                'taskId': completed[0].get('id'),
                'subject': completed[0].get('content', 'Unknown Todo'),
                'type': 'todo'
            }

    return None

def generate_completion_message(completions: Dict, task_info: Optional[Dict]) -> str:
    """Generate completion message"""
    today_count = completions['todayCompleted']
    streak = completions['streaks']['current']

    messages = []

    if task_info:
        messages.append(f"Task completed: {task_info['subject'][:50]}")

    messages.append(f"Today: {today_count} completed")

    if streak > 1:
        messages.append(f"{streak} day streak!")

    # Milestone celebration
    total = completions['totalCompleted']
    milestones = [10, 50, 100, 500, 1000]
    for m in milestones:
        if total == m:
            messages.append(f"{m} tasks completed milestone!")
            break

    return ' | '.join(messages)

def process_completion(data: Dict) -> Dict:
    """Process completion event"""
    completions = load_completions()

    if not is_completion_event(data):
        return {
            'status': 'skipped',
            'message': 'Not a completion event'
        }

    task_info = extract_task_info(data)
    now = datetime.now()
    today = now.date().isoformat()

    # Reset today's count check
    last_date = completions.get('lastCompletedAt', '')[:10]
    if last_date != today:
        completions['todayCompleted'] = 0

    # Update completion records
    completions['totalCompleted'] += 1
    completions['todayCompleted'] += 1
    completions['lastCompletedAt'] = now.isoformat()

    # Add to history
    if task_info:
        completions['completionHistory'].append({
            'timestamp': now.isoformat(),
            **task_info
        })
        # Keep only recent 100 entries
        completions['completionHistory'] = completions['completionHistory'][-100:]

    # Update streak records
    completions['streaks'] = update_streaks(completions)

    save_completions(completions)

    return {
        'status': 'completed',
        'totalCompleted': completions['totalCompleted'],
        'todayCompleted': completions['todayCompleted'],
        'streak': completions['streaks']['current'],
        'message': generate_completion_message(completions, task_info)
    }

def main():
    try:
        input_data = sys.stdin.read()
        data = json.loads(input_data) if input_data.strip() else {}

        result = process_completion(data)

        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()
