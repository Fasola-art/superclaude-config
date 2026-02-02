#!/usr/bin/env python3
"""
JARVIS Morning Briefing Hook
Display yesterday's work summary, today's schedule, and incomplete tasks on first execution
Hook Type: UserPromptSubmit
"""

import os
import sys
import json
from datetime import datetime, date
from pathlib import Path

# Add JARVIS module path
JARVIS_DIR = Path.home() / ".claude" / "jarvis"
sys.path.insert(0, str(JARVIS_DIR / "memory"))

# Marker file (for checking first execution today)
MARKER_FILE = JARVIS_DIR / ".last_execution"


def is_first_execution_today() -> bool:
    """Check if this is the first execution today"""
    if not MARKER_FILE.exists():
        return True

    last_date = MARKER_FILE.read_text().strip()
    today = date.today().isoformat()

    return last_date != today


def update_marker():
    """Update marker file"""
    MARKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    MARKER_FILE.write_text(date.today().isoformat())


def get_token_stats() -> str:
    """Get today's token usage"""
    try:
        stats_file = Path.home() / ".claude" / "stats-cache.json"
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                data = json.load(f)
            today_str = date.today().isoformat()
            for day in data.get('dailyModelTokens', []):
                if day.get('date') == today_str:
                    tokens = sum(day.get('tokensByModel', {}).values())
                    return f"Today {tokens:,} tokens | Check details with /context"
        return "Today 0 tokens | Check details with /context"
    except:
        return "Check with /context"


def get_morning_briefing() -> str:
    """Generate morning briefing"""
    try:
        from manager import (
            init_database, WorkSessionManager, TaskManager,
            CalendarManager
        )
        from ml_predictor import get_predictor

        init_database()

        lines = []
        lines.append("=" * 50)
        lines.append("JARVIS Briefing")
        lines.append("=" * 50)

        # Token stats
        token_info = get_token_stats()
        lines.append(f"\n{token_info}")

        # Yesterday's work summary
        yesterday = WorkSessionManager.get_yesterday_summary()
        if yesterday:
            lines.append(f"\nYesterday's Work ({yesterday['date']})")
            lines.append(f"   Sessions: {yesterday['total_sessions']}")
            for session in yesterday['sessions'][:3]:
                if session.get('summary'):
                    lines.append(f"   - {session['summary'][:50]}...")
        else:
            lines.append("\nYesterday's Work: No records")

        # Today's schedule
        today_events = CalendarManager.get_today_events()
        lines.append(f"\nToday's Schedule ({len(today_events)} events)")
        if today_events:
            for event in today_events[:5]:
                time_str = event.get('event_time', '')[:16]
                lines.append(f"   - {time_str} - {event['title']}")
        else:
            lines.append("   No scheduled events.")

        # Incomplete tasks
        pending_tasks = TaskManager.get_pending_tasks()
        lines.append(f"\nIncomplete Tasks ({len(pending_tasks)})")
        if pending_tasks:
            for task in pending_tasks[:5]:
                priority_icon = "HIGH" if task['priority'] == 1 else "MED" if task['priority'] == 2 else "LOW"
                lines.append(f"   [{priority_icon}] {task['title']}")
        else:
            lines.append("   No incomplete tasks!")

        # ML prediction-based suggestions
        try:
            predictor = get_predictor()
            suggestion = predictor.suggest_next_action()
            if suggestion:
                lines.append(f"\nPrediction-Based Suggestion")
                lines.append(f"   {suggestion}")
        except:
            pass

        lines.append("\n" + "=" * 50)

        return "\n".join(lines)

    except Exception as e:
        return f"JARVIS briefing generation failed: {e}"


def main():
    # Get prompt from environment variable
    user_prompt = os.environ.get('CLAUDE_USER_PROMPT', '')

    # Force briefing display if /j briefing command
    force_briefing = '/j briefing' in user_prompt.lower() or '/j 브리핑' in user_prompt.lower()

    # Display only on first execution or forced briefing
    if force_briefing or is_first_execution_today():
        briefing = get_morning_briefing()
        print(briefing)

        if not force_briefing:
            update_marker()


if __name__ == "__main__":
    main()
