#!/usr/bin/env python3
"""
jarvis-work-tracker.py
Jarvis work tracking hook

Trigger: PostToolUse
Matcher: Edit|Write|Bash|Task
Timeout: 5000ms
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
    """Create directories"""
    WORK_LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_today_log_path() -> Path:
    """Get today's log file path"""
    return WORK_LOG_DIR / f"work_{date.today().isoformat()}.json"

def load_today_log() -> Dict:
    """Load today's work log"""
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
    """Save today's work log"""
    ensure_dirs()
    log_path = get_today_log_path()
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False))

def categorize_operation(tool: str, data: Dict) -> str:
    """Categorize operation type"""
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
    """Extract file path"""
    return data.get('file_path') or data.get('path')

def is_error_result(data: Dict) -> bool:
    """Check if result is an error"""
    if data.get('exitCode', 0) != 0:
        return True
    if data.get('stderr', '').strip():
        return True
    return False

def track_work(data: Dict) -> Dict:
    """Track work"""
    log = load_today_log()
    tool = data.get('tool', 'unknown')

    # Create timeline entry
    entry = {
        'timestamp': datetime.now().isoformat(),
        'tool': tool,
        'category': categorize_operation(tool, data),
        'success': not is_error_result(data)
    }

    # Add file info
    file_path = extract_file_info(data)
    if file_path:
        entry['file'] = file_path
        if file_path not in log['filesChanged']:
            log['filesChanged'].append(file_path)
            log['summary']['filesModified'] += 1

    # Add command info
    if tool == 'Bash':
        command = data.get('command', '')
        entry['command'] = command[:100]  # Max 100 chars
        log['commandHistory'].append({
            'timestamp': entry['timestamp'],
            'command': command[:200],
            'exitCode': data.get('exitCode', 0)
        })
        log['summary']['commandsExecuted'] += 1

    # Track Task completion
    if tool == 'Task':
        log['summary']['tasksCompleted'] += 1

    # Track errors
    if is_error_result(data):
        log['summary']['errorsEncountered'] += 1
        entry['error'] = True

    # Add to timeline
    log['timeline'].append(entry)
    log['summary']['totalOperations'] += 1

    # Keep only recent 100 entries
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
            'message': f"Today's work: {summary['totalOperations']} operations, "
                      f"{summary['filesModified']} files, "
                      f"{summary['errorsEncountered']} errors"
        }

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))
        sys.exit(1)

if __name__ == '__main__':
    main()
