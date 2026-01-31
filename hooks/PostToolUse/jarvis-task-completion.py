#!/usr/bin/env python3
"""
jarvis-task-completion.py
Jarvis 태스크 완료 처리 훅

트리거: PostToolUse
매처: TaskUpdate|TodoWrite
타임아웃: 5000ms
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
    """디렉토리 생성"""
    JARVIS_DIR.mkdir(parents=True, exist_ok=True)
    DAILY_REPORT_DIR.mkdir(parents=True, exist_ok=True)

def load_completions() -> Dict:
    """완료 기록 로드"""
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
    """완료 기록 저장"""
    ensure_dirs()
    COMPLETIONS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

def update_streaks(completions: Dict) -> Dict:
    """연속 완료 기록 업데이트"""
    today = datetime.now().date().isoformat()
    streaks = completions['streaks']

    if streaks['lastDate'] == today:
        # 오늘 이미 업데이트됨
        return streaks

    from datetime import timedelta
    yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()

    if streaks['lastDate'] == yesterday:
        # 연속 유지
        streaks['current'] += 1
    elif streaks['lastDate'] != today:
        # 연속 끊김
        streaks['current'] = 1

    streaks['lastDate'] = today

    if streaks['current'] > streaks['best']:
        streaks['best'] = streaks['current']

    return streaks

def is_completion_event(data: Dict) -> bool:
    """완료 이벤트인지 확인"""
    # TaskUpdate로 completed 상태 변경
    if data.get('tool') == 'TaskUpdate':
        return data.get('status') == 'completed'

    # TodoWrite에서 완료 항목 확인
    if data.get('tool') == 'TodoWrite':
        todos = data.get('todos', [])
        return any(t.get('status') == 'completed' for t in todos)

    return False

def extract_task_info(data: Dict) -> Optional[Dict]:
    """태스크 정보 추출"""
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
    """완료 메시지 생성"""
    today_count = completions['todayCompleted']
    streak = completions['streaks']['current']

    messages = []

    if task_info:
        messages.append(f"✅ 태스크 완료: {task_info['subject'][:50]}")

    messages.append(f"오늘 {today_count}개 완료")

    if streak > 1:
        messages.append(f"🔥 {streak}일 연속 달성!")

    # 마일스톤 축하
    total = completions['totalCompleted']
    milestones = [10, 50, 100, 500, 1000]
    for m in milestones:
        if total == m:
            messages.append(f"🎉 {m}개 태스크 완료 달성!")
            break

    return ' | '.join(messages)

def process_completion(data: Dict) -> Dict:
    """완료 이벤트 처리"""
    completions = load_completions()

    if not is_completion_event(data):
        return {
            'status': 'skipped',
            'message': '완료 이벤트 아님'
        }

    task_info = extract_task_info(data)
    now = datetime.now()
    today = now.date().isoformat()

    # 오늘 카운트 리셋 체크
    last_date = completions.get('lastCompletedAt', '')[:10]
    if last_date != today:
        completions['todayCompleted'] = 0

    # 완료 기록 업데이트
    completions['totalCompleted'] += 1
    completions['todayCompleted'] += 1
    completions['lastCompletedAt'] = now.isoformat()

    # 히스토리 추가
    if task_info:
        completions['completionHistory'].append({
            'timestamp': now.isoformat(),
            **task_info
        })
        # 최근 100개만 유지
        completions['completionHistory'] = completions['completionHistory'][-100:]

    # 연속 기록 업데이트
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
