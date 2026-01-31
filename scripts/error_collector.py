#!/usr/bin/env python3
"""
Error KB 자동 수집 시스템
- MCP 로그에서 에러 추출
- Error KB (pending/resolved) 폴더에 JSON 저장
- PostgreSQL에 기록
"""

import json
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
import subprocess

# 경로 설정
HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
ERROR_KB_DIR = CLAUDE_DIR / "error-kb"
PENDING_DIR = ERROR_KB_DIR / "pending"
RESOLVED_DIR = ERROR_KB_DIR / "resolved"
LOG_FILE = CLAUDE_DIR / "logs" / "mcp-router" / "launchd.err"
PSQL_PATH = "/opt/homebrew/Cellar/postgresql@16/16.11_1/bin/psql"
DB_NAME = "claude_mcp"

# 폴더 생성
PENDING_DIR.mkdir(parents=True, exist_ok=True)
RESOLVED_DIR.mkdir(parents=True, exist_ok=True)

def generate_error_id(error_type: str, message: str) -> str:
    """에러 고유 ID 생성 (중복 방지)"""
    content = f"{error_type}:{message}"
    return hashlib.md5(content.encode()).hexdigest()[:12]

def parse_log_errors(log_file: Path) -> list:
    """로그 파일에서 에러 추출"""
    errors = []
    if not log_file.exists():
        return errors

    error_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[ERROR\] ([^:]+): (.+)'
    )

    with open(log_file, 'r') as f:
        for line in f:
            match = error_pattern.match(line.strip())
            if match:
                timestamp_str, component, message = match.groups()
                errors.append({
                    'timestamp': timestamp_str,
                    'component': component,
                    'message': message,
                    'raw': line.strip()
                })

    return errors

def save_to_error_kb(error: dict) -> str:
    """Error KB에 저장"""
    error_id = generate_error_id(error['component'], error['message'])

    # 이미 존재하는지 확인
    pending_file = PENDING_DIR / f"{error_id}.json"
    resolved_file = RESOLVED_DIR / f"{error_id}.json"

    if pending_file.exists() or resolved_file.exists():
        return error_id  # 이미 기록됨

    error_record = {
        'id': error_id,
        'type': error['component'],
        'message': error['message'],
        'timestamp': error['timestamp'],
        'raw_log': error['raw'],
        'created_at': datetime.now().isoformat(),
        'resolved': False,
        'resolution': None,
        'context': {}
    }

    with open(pending_file, 'w') as f:
        json.dump(error_record, f, indent=2, ensure_ascii=False)

    return error_id

def save_to_postgres(error: dict) -> bool:
    """PostgreSQL에 저장"""
    error_id = generate_error_id(error['component'], error['message'])

    sql = f"""
    INSERT INTO errors (error_type, error_message, context, created_at)
    SELECT '{error['component']}', '{error['message'].replace("'", "''")}',
           '{{"error_id": "{error_id}", "raw": "{error['raw'].replace("'", "''")}"}}',
           '{error['timestamp'].replace(",", ".")}'
    WHERE NOT EXISTS (
        SELECT 1 FROM errors
        WHERE error_message = '{error['message'].replace("'", "''")}'
        AND error_type = '{error['component']}'
    );
    """

    try:
        result = subprocess.run(
            [PSQL_PATH, '-d', DB_NAME, '-c', sql],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"PostgreSQL 저장 실패: {e}")
        return False

def resolve_error(error_id: str, resolution: str):
    """에러를 해결됨으로 표시"""
    pending_file = PENDING_DIR / f"{error_id}.json"
    resolved_file = RESOLVED_DIR / f"{error_id}.json"

    if not pending_file.exists():
        print(f"에러 {error_id}를 찾을 수 없습니다")
        return False

    with open(pending_file, 'r') as f:
        error_record = json.load(f)

    error_record['resolved'] = True
    error_record['resolution'] = resolution
    error_record['resolved_at'] = datetime.now().isoformat()

    with open(resolved_file, 'w') as f:
        json.dump(error_record, f, indent=2, ensure_ascii=False)

    pending_file.unlink()

    # PostgreSQL 업데이트
    sql = f"""
    UPDATE errors
    SET resolved = true,
        resolution = '{resolution.replace("'", "''")}',
        resolved_at = CURRENT_TIMESTAMP
    WHERE context->>'error_id' = '{error_id}';
    """

    try:
        subprocess.run([PSQL_PATH, '-d', DB_NAME, '-c', sql], capture_output=True)
    except:
        pass

    return True

def collect_errors():
    """메인 수집 함수"""
    print(f"[{datetime.now().isoformat()}] 에러 수집 시작...")

    errors = parse_log_errors(LOG_FILE)
    new_count = 0

    for error in errors:
        error_id = save_to_error_kb(error)
        if save_to_postgres(error):
            new_count += 1

    print(f"총 {len(errors)}개 에러 중 {new_count}개 새로 기록됨")

    # 현재 상태 출력
    pending = list(PENDING_DIR.glob("*.json"))
    resolved = list(RESOLVED_DIR.glob("*.json"))
    print(f"Error KB 상태: {len(pending)}개 미해결, {len(resolved)}개 해결됨")

def list_pending():
    """미해결 에러 목록"""
    pending = list(PENDING_DIR.glob("*.json"))
    if not pending:
        print("미해결 에러 없음")
        return

    print(f"\n=== 미해결 에러 ({len(pending)}개) ===")
    for f in pending:
        with open(f, 'r') as file:
            error = json.load(file)
            print(f"[{error['id']}] {error['type']}: {error['message'][:60]}...")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "collect":
            collect_errors()
        elif sys.argv[1] == "list":
            list_pending()
        elif sys.argv[1] == "resolve" and len(sys.argv) >= 4:
            resolve_error(sys.argv[2], sys.argv[3])
        else:
            print("사용법:")
            print("  python error_collector.py collect  - 에러 수집")
            print("  python error_collector.py list     - 미해결 목록")
            print("  python error_collector.py resolve <id> <resolution>")
    else:
        collect_errors()
