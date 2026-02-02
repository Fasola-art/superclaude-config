#!/usr/bin/env python3
"""
jarvis-morning-briefing.py
Morning briefing generation hook

Trigger: UserPromptSubmit
Timeout: 5000ms
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

CLAUDE_DIR = Path.home() / '.claude'
BRIEFING_FILE = CLAUDE_DIR / 'cache' / 'last-briefing.json'
TODOS_DIR = CLAUDE_DIR / 'todos'
SESSIONS_DIR = CLAUDE_DIR / 'sessions'

BRIEFING_INTERVAL_HOURS = 8  # Briefing every 8 hours


def should_show_briefing() -> bool:
    """Check if briefing should be shown"""
    try:
        if BRIEFING_FILE.exists():
            data = json.loads(BRIEFING_FILE.read_text())
            last_briefing = datetime.fromisoformat(data.get('lastBriefing', ''))
            hours_since = (datetime.now() - last_briefing).total_seconds() / 3600
            return hours_since >= BRIEFING_INTERVAL_HOURS
    except Exception:
        pass
    return True


def save_briefing_time():
    """Save briefing time"""
    BRIEFING_FILE.parent.mkdir(parents=True, exist_ok=True)
    BRIEFING_FILE.write_text(json.dumps({
        'lastBriefing': datetime.now().isoformat()
    }))


def get_incomplete_todos() -> list:
    """Get incomplete tasks"""
    todos = []
    try:
        if TODOS_DIR.exists():
            for file in TODOS_DIR.glob('*.json'):
                try:
                    data = json.loads(file.read_text())
                    if isinstance(data, list):
                        for todo in data:
                            if todo.get('status') not in ['completed', 'cancelled']:
                                todos.append(todo)
                    elif isinstance(data, dict) and data.get('status') not in ['completed', 'cancelled']:
                        todos.append(data)
                except Exception:
                    continue
    except Exception:
        pass
    return todos[:5]  # Max 5


def get_recent_sessions() -> list:
    """Get recent sessions"""
    sessions = []
    try:
        if SESSIONS_DIR.exists():
            files = sorted(SESSIONS_DIR.glob('*.json'), key=os.path.getmtime, reverse=True)
            for file in files[:3]:  # Recent 3
                try:
                    data = json.loads(file.read_text())
                    sessions.append({
                        'name': file.stem,
                        'lastModified': datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                    })
                except Exception:
                    continue
    except Exception:
        pass
    return sessions


def generate_briefing() -> dict:
    """Generate briefing"""
    now = datetime.now()
    greeting = "Good morning" if now.hour < 12 else ("Good afternoon" if now.hour < 18 else "Good evening")

    incomplete_todos = get_incomplete_todos()
    recent_sessions = get_recent_sessions()

    briefing_parts = [f"{greeting}!"]

    if incomplete_todos:
        briefing_parts.append(f"\nIncomplete tasks: {len(incomplete_todos)}")
        for todo in incomplete_todos:
            status_icon = "[in progress]" if todo.get('status') == 'in_progress' else "[pending]"
            briefing_parts.append(f"  {status_icon} {todo.get('subject', 'Unknown')}")

    if recent_sessions:
        briefing_parts.append(f"\nRecent sessions:")
        for session in recent_sessions:
            briefing_parts.append(f"  - {session['name']}")

    briefing_parts.append("\nUse 'continue' keyword to resume previous work.")

    return {
        'greeting': greeting,
        'incompleteTodos': len(incomplete_todos),
        'recentSessions': len(recent_sessions),
        'message': '\n'.join(briefing_parts)
    }


def main():
    try:
        # Ignore stdin (briefing is unrelated to input)
        sys.stdin.read()

        if not should_show_briefing():
            print(json.dumps({
                'status': 'skipped',
                'message': 'Briefing skipped (recently shown)'
            }, ensure_ascii=False))
            sys.exit(0)

        briefing = generate_briefing()
        save_briefing_time()

        output = {
            'status': 'briefing',
            **briefing
        }

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
