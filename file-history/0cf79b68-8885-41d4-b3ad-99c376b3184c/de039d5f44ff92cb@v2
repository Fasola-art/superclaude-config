#!/usr/bin/env python3
"""
jarvis-morning-briefing.py
모닝 브리핑 생성 훅

트리거: UserPromptSubmit
타임아웃: 5000ms
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

BRIEFING_INTERVAL_HOURS = 8  # 8시간마다 브리핑


def should_show_briefing() -> bool:
    """브리핑을 보여줘야 하는지 확인"""
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
    """브리핑 시간 저장"""
    BRIEFING_FILE.parent.mkdir(parents=True, exist_ok=True)
    BRIEFING_FILE.write_text(json.dumps({
        'lastBriefing': datetime.now().isoformat()
    }))


def get_incomplete_todos() -> list:
    """미완료 태스크 조회"""
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
    return todos[:5]  # 최대 5개


def get_recent_sessions() -> list:
    """최근 세션 조회"""
    sessions = []
    try:
        if SESSIONS_DIR.exists():
            files = sorted(SESSIONS_DIR.glob('*.json'), key=os.path.getmtime, reverse=True)
            for file in files[:3]:  # 최근 3개
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
    """브리핑 생성"""
    now = datetime.now()
    greeting = "좋은 아침" if now.hour < 12 else ("좋은 오후" if now.hour < 18 else "좋은 저녁")

    incomplete_todos = get_incomplete_todos()
    recent_sessions = get_recent_sessions()

    briefing_parts = [f"🌅 {greeting}입니다!"]

    if incomplete_todos:
        briefing_parts.append(f"\n📋 미완료 태스크 {len(incomplete_todos)}개:")
        for todo in incomplete_todos:
            status_icon = "🔄" if todo.get('status') == 'in_progress' else "⏳"
            briefing_parts.append(f"  {status_icon} {todo.get('subject', 'Unknown')}")

    if recent_sessions:
        briefing_parts.append(f"\n📂 최근 세션:")
        for session in recent_sessions:
            briefing_parts.append(f"  - {session['name']}")

    briefing_parts.append("\n💡 '계속' 키워드로 이전 작업을 이어갈 수 있습니다.")

    return {
        'greeting': greeting,
        'incompleteTodos': len(incomplete_todos),
        'recentSessions': len(recent_sessions),
        'message': '\n'.join(briefing_parts)
    }


def main():
    try:
        # stdin은 무시 (브리핑은 입력과 무관)
        sys.stdin.read()

        if not should_show_briefing():
            print(json.dumps({
                'status': 'skipped',
                'message': '브리핑 생략 (최근 표시됨)'
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
