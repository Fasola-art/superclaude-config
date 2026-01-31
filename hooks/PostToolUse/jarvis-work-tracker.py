#!/usr/bin/env python3
"""
jarvis-work-tracker.py
Jarvis 작업 추적 훅

트리거: PostToolUse
매처: Edit|Write|Bash|Task
타임아웃: 5000ms
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional

CLAUDE_DIR = Path.home() / '.claude'
JARVIS_DIR = CLAUDE_DIR / 'jarvis'
WORK_LOG_DIR = JARVIS_DIR / 'work-logs'

def ensure_dirs():
    """디렉토리 생성"""
    WORK_LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_today_log_path() -> Path:
    """오늘 날짜의 로그 파일 경로"""
    return WORK_LOG_DIR / f"work_{date.today().isoformat()}.json"

def load_today_log() -> Dict:
    """오늘 작업 로그 로드"""
    log_path = get_today_log_path()
    if log_path.exists():
        try:
            return json.loads(log_path.read_text())
        except Exception:
            pass

    return {
        'date': date.today().isoformat(),
        'summary': {
            'totalOperations': 0,
            'filesModified': 0,
            'commandsExecuted': 0,
            'tasksCompleted': 0,
            'errorsEncountered': 0
        },
        'timeline': [],
        'filesChanged': [],
        'commandHistory': []
    }

def save_today_log(log: Dict):
    """오늘 작업 로그 저장"""
    ensure_dirs()
    log_path = get_today_log_path()
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False))

def categorize_operation(tool: str, data: Dict) -> str:
    """작업 유형 분류"""
    categories = {
        'Edit': 'code_modification',
        'Write': 'file_creation',
        'Bash': 'command_execution',
        'Task': 'task_operation',
        'Read': 'file_read',
        'Glob': 'file_search',
        'Grep': 'content_search'
    }
    return categories.get(tool, 'other')

def extract_file_info(data: Dict) -> Optional[str]:
    """파일 경로 추출"""
    return data.get('file_path') or data.get('path')

def is_error_result(data: Dict) -> bool:
    """에러 결과 여부 확인"""
    if data.get('exitCode', 0) != 0:
        return True
    if data.get('stderr', '').strip():
        return True
    return False

def track_work(data: Dict) -> Dict:
    """작업 추적"""
    log = load_today_log()
    tool = data.get('tool', 'unknown')

    # 타임라인 항목 생성
    entry = {
        'timestamp': datetime.now().isoformat(),
        'tool': tool,
        'category': categorize_operation(tool, data),
        'success': not is_error_result(data)
    }

    # 파일 정보 추가
    file_path = extract_file_info(data)
    if file_path:
        entry['file'] = file_path
        if file_path not in log['filesChanged']:
            log['filesChanged'].append(file_path)
            log['summary']['filesModified'] += 1

    # 명령어 정보 추가
    if tool == 'Bash':
        command = data.get('command', '')
        entry['command'] = command[:100]  # 최대 100자
        log['commandHistory'].append({
            'timestamp': entry['timestamp'],
            'command': command[:200],
            'exitCode': data.get('exitCode', 0)
        })
        log['summary']['commandsExecuted'] += 1

    # Task 완료 추적
    if tool == 'Task':
        log['summary']['tasksCompleted'] += 1

    # 에러 추적
    if is_error_result(data):
        log['summary']['errorsEncountered'] += 1
        entry['error'] = True

    # 타임라인에 추가
    log['timeline'].append(entry)
    log['summary']['totalOperations'] += 1

    # 최근 100개 항목만 유지
    log['timeline'] = log['timeline'][-100:]
    log['commandHistory'] = log['commandHistory'][-50:]

    save_today_log(log)

    return log['summary']

def main():
    try:
        input_data = sys.stdin.read()
        data = json.loads(input_data) if input_data.strip() else {}

        summary = track_work(data)

        output = {
            'status': 'tracked',
            'summary': summary,
            'message': f"📊 오늘 작업: {summary['totalOperations']}개 작업, "
                      f"{summary['filesModified']}개 파일, "
                      f"{summary['errorsEncountered']}개 에러"
        }

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()
