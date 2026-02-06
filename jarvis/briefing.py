#!/usr/bin/env python3
"""JARVIS 브리핑 모듈"""

from datetime import date, datetime
from memory import init_database, WorkSessionManager, TaskManager, CalendarManager
from memory.ml_predictor import get_predictor


def get_detailed_briefing() -> str:
    """상세 브리핑 생성"""
    init_database()
    lines = []

    lines.append('═' * 60)
    lines.append(f'🤖 JARVIS Briefing - {date.today().strftime("%Y년 %m월 %d일 (%a)")}')
    lines.append('═' * 60)

    # 어제 작업 요약
    lines.append('\n📊 어제 작업 요약')
    lines.append('─' * 40)
    yesterday = WorkSessionManager.get_yesterday_summary()
    if yesterday:
        lines.append(f'   세션: {yesterday.get("total_sessions", 0)}개')
        duration = yesterday.get("total_duration", 0)
        if duration:
            lines.append(f'   작업 시간: {duration:.0f}분')
    else:
        lines.append('   데이터 없음')

    # 오늘 일정
    events = CalendarManager.get_today_events()
    lines.append(f'\n📅 오늘 일정 ({len(events)}개)')
    lines.append('─' * 40)
    if events:
        for e in events:
            time_str = e.get('time', '') or e.get('start_time', '') or ''
            location = e.get('location', '')
            loc_str = f' @ {location}' if location else ''
            lines.append(f'   • {time_str} {e.get("title", "")}{loc_str}')
    else:
        lines.append('   일정 없음')

    # 대기 작업 - 우선순위별
    tasks = TaskManager.get_pending_tasks()
    lines.append(f'\n📋 대기 작업 ({len(tasks)}개)')
    lines.append('─' * 40)

    high = [t for t in tasks if t.get('priority', 0) >= 2]
    normal = [t for t in tasks if t.get('priority', 0) < 2]

    if high:
        lines.append('   🔴 높은 우선순위:')
        for t in high[:5]:
            due = t.get('due_date', '')
            due_str = f' (마감: {due})' if due else ''
            lines.append(f'      [{t.get("id", "?")}] {t.get("title", "")}{due_str}')
            if t.get('description'):
                lines.append(f'          └─ {t.get("description")[:50]}')
        if len(high) > 5:
            lines.append(f'      ... 외 {len(high)-5}개')

    if normal:
        lines.append('   🟡 일반:')
        for t in normal[:3]:
            lines.append(f'      [{t.get("id", "?")}] {t.get("title", "")}')
        if len(normal) > 3:
            lines.append(f'      ... 외 {len(normal)-3}개')

    # ML 추천
    lines.append('\n🧠 AI 추천')
    lines.append('─' * 40)
    suggestion = get_predictor().suggest_next_action()
    lines.append(f'   {suggestion if suggestion else "패턴 데이터 수집 중"}')

    # 시스템 상태
    lines.append('\n⚙️ 시스템')
    lines.append('─' * 40)
    lines.append(f'   {datetime.now().strftime("%H:%M")} | DB ✅')

    lines.append('\n' + '═' * 60)

    return '\n'.join(lines)


def get_simple_briefing() -> str:
    """간단 브리핑 생성"""
    init_database()
    lines = []

    lines.append('═' * 50)
    lines.append(f'🤖 JARVIS - {date.today().strftime("%Y-%m-%d")}')
    lines.append('═' * 50)

    events = CalendarManager.get_today_events()
    tasks = TaskManager.get_pending_tasks()
    high_tasks = [t for t in tasks if t.get('priority', 0) >= 2]

    lines.append(f'📅 일정: {len(events)}개 | 📋 작업: {len(tasks)}개 (🔴 {len(high_tasks)})')
    lines.append('═' * 50)

    return '\n'.join(lines)


if __name__ == '__main__':
    import sys
    if '--simple' in sys.argv:
        print(get_simple_briefing())
    else:
        print(get_detailed_briefing())
