#!/usr/bin/env python3
"""
jarvis-work-tracker.py - 작업 추적 훅 (70줄)
Trigger: PostToolUse | Matcher: Edit|Write|Bash|Task | Timeout: 5000ms
"""
import sys
from pathlib import Path
from datetime import datetime, date
from typing import Any, Dict

sys.path.insert(0, str(Path.home() / '.claude'))
from jarvis.core import (
    safe_load_json, atomic_write_json, ensure_dir, run_hook,
    sanitize_file_path, mask_sensitive_data
)

WORK_LOG_DIR = Path.home() / '.claude/jarvis/work-logs'
TOOL_CATEGORIES = {
    'Edit': 'code_modification', 'Write': 'file_creation',
    'Bash': 'command_execution', 'Task': 'task_operation',
    'Read': 'file_read', 'Glob': 'file_search', 'Grep': 'content_search'
}


def get_default_log() -> Dict[str, Any]:
    return {
        'date': date.today().isoformat(),
        'summary': {'totalOperations': 0, 'filesModified': 0, 'commandsExecuted': 0,
                    'tasksCompleted': 0, 'errorsEncountered': 0},
        'timeline': [], 'filesChanged': [], 'commandHistory': []
    }


def is_error_result(data: Dict[str, Any]) -> bool:
    try:
        if int(data.get('exitCode', 0)) != 0:
            return True
    except (ValueError, TypeError):
        pass
    return bool(str(data.get('stderr', '')).strip())


def track_work(data: Dict[str, Any]) -> Dict[str, Any]:
    log_path = WORK_LOG_DIR / f"work_{date.today().isoformat()}.json"
    log = safe_load_json(log_path, get_default_log())
    tool = str(data.get('tool', 'unknown'))

    entry = {
        'timestamp': datetime.now().isoformat(), 'tool': tool,
        'category': TOOL_CATEGORIES.get(tool, 'other'),
        'success': not is_error_result(data)
    }

    file_path = sanitize_file_path(data.get('file_path') or data.get('path'))
    if file_path and file_path != '[REDACTED]':
        entry['file'] = file_path
        if file_path not in log['filesChanged']:
            log['filesChanged'].append(file_path)
            log['summary']['filesModified'] += 1

    if tool == 'Bash':
        cmd = mask_sensitive_data(str(data.get('command', '')))
        entry['command'] = cmd[:100]
        log['commandHistory'].append({'timestamp': entry['timestamp'], 'command': cmd[:200]})
        log['summary']['commandsExecuted'] += 1

    if tool == 'Task':
        log['summary']['tasksCompleted'] += 1
    if is_error_result(data):
        log['summary']['errorsEncountered'] += 1

    log['timeline'] = (log.get('timeline', []) + [entry])[-100:]
    log['commandHistory'] = log.get('commandHistory', [])[-50:]
    log['summary']['totalOperations'] += 1

    ensure_dir(WORK_LOG_DIR)
    atomic_write_json(log_path, log)
    return {'status': 'tracked', 'summary': log['summary']}


if __name__ == '__main__':
    run_hook(track_work)
