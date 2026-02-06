#!/usr/bin/env python3
"""
jarvis-morning-briefing.py - 모닝 브리핑 훅 (80줄)
Hook Type: UserPromptSubmit
"""
import os
import sys
import json
from datetime import date
from pathlib import Path

CLAUDE_DIR = Path.home() / '.claude'
JARVIS_DIR = CLAUDE_DIR / 'jarvis'
MARKER_FILE = JARVIS_DIR / '.last_execution'

sys.path.insert(0, str(CLAUDE_DIR))
from jarvis.core import get_logger
logger = get_logger(__name__)


def is_first_execution_today() -> bool:
    if not MARKER_FILE.exists():
        return True
    try:
        return MARKER_FILE.read_text().strip() != date.today().isoformat()
    except (PermissionError, OSError):
        return True


def update_marker() -> None:
    try:
        MARKER_FILE.parent.mkdir(parents=True, exist_ok=True)
        MARKER_FILE.write_text(date.today().isoformat())
    except OSError:
        pass


def get_token_stats() -> str:
    stats_file = CLAUDE_DIR / 'stats-cache.json'
    if not stats_file.exists():
        return "Today 0 tokens"
    try:
        data = json.loads(stats_file.read_text())
        for day in data.get('dailyModelTokens', []):
            if day.get('date') == date.today().isoformat():
                tokens = sum(day.get('tokensByModel', {}).values())
                return f"Today {tokens:,} tokens"
    except (json.JSONDecodeError, OSError):
        pass
    return "Today 0 tokens"


def get_morning_briefing() -> str:
    lines = ["=" * 50, "JARVIS Briefing", "=" * 50, f"\n{get_token_stats()}"]

    try:
        from jarvis.memory import init_database, WorkSessionManager, TaskManager, CalendarManager
        init_database()

        yesterday = WorkSessionManager.get_yesterday_summary()
        lines.append(f"\nYesterday: {yesterday.get('total_sessions', 0) if yesterday else 0} sessions")

        events = CalendarManager.get_today_events()
        lines.append(f"Today: {len(events) if events else 0} events")

        tasks = TaskManager.get_pending_tasks()
        lines.append(f"Pending: {len(tasks) if tasks else 0} tasks")

    except ImportError:
        lines.append("\nJARVIS modules not installed")
    except Exception as e:
        lines.append(f"\nError: {type(e).__name__}")

    try:
        from jarvis.memory.ml_predictor import get_predictor
        suggestion = get_predictor().suggest_next_action()
        if suggestion:
            lines.append(f"\nSuggestion: {suggestion}")
    except ImportError:
        pass
    except Exception:
        pass

    lines.append("\n" + "=" * 50)
    return "\n".join(lines)


def main() -> None:
    prompt = os.environ.get('CLAUDE_USER_PROMPT', '')
    force = '/j briefing' in prompt.lower() or '/j 브리핑' in prompt.lower()

    if force or is_first_execution_today():
        print(get_morning_briefing())
        if not force:
            update_marker()


if __name__ == '__main__':
    main()
