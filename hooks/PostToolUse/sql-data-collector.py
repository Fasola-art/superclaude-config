#!/usr/bin/env python3
"""
SQL 데이터 수집 훅 (PostToolUse)

트리거 조건:
- /sql 커맨드 실행 시
- 데이터 수집 관련 키워드 감지 시

동작:
- 자동으로 최신 물류/무역 데이터 수집
- DB에 데이터 적재

Version: 1.0.0
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

# Windows UTF-8 출력 강제
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path


def should_trigger(tool_name: str, tool_input: dict, tool_output: str) -> bool:
    """훅 실행 조건 확인"""
    # Skill 도구에서 /sql 커맨드 실행 시
    if tool_name == "Skill":
        skill = tool_input.get("skill", "")
        if skill in ["sql", "sql-trading"]:
            return True

    # Bash에서 psql 명령 실행 시
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if "psql" in command and "claude_mcp" in command:
            return True

    return False


def get_last_collection_time() -> datetime | None:
    """마지막 수집 시간 확인"""
    state_file = Path.home() / ".claude" / "modules" / "sql-trading" / ".collection_state.json"

    if state_file.exists():
        with open(state_file, encoding='utf-8') as f:
            state = json.load(f)
            last_time_str = state.get("last_collection")
            if last_time_str:
                return datetime.fromisoformat(last_time_str)

    return None


def update_collection_time() -> None:
    """수집 시간 업데이트"""
    state_file = Path.home() / ".claude" / "modules" / "sql-trading" / ".collection_state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)

    state = {"last_collection": datetime.now().isoformat()}

    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f)


def run_collection() -> dict:
    """데이터 수집 실행"""
    collector_path = Path.home() / ".claude" / "modules" / "sql-trading" / "collectors" / "logistics_collector.py"

    if not collector_path.exists():
        return {"success": False, "error": "수집기 파일 없음"}

    try:
        result = subprocess.run(
            [sys.executable, str(collector_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5분 타임아웃
        )

        if result.returncode == 0:
            update_collection_time()
            return {
                "success": True,
                "output": result.stdout,
                "collected_at": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": result.stderr
            }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "수집 타임아웃 (5분 초과)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """메인 훅 실행"""
    # 환경 변수에서 도구 정보 읽기
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    tool_input_str = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    tool_output = os.environ.get("CLAUDE_TOOL_OUTPUT", "")

    try:
        tool_input = json.loads(tool_input_str)
    except json.JSONDecodeError:
        tool_input = {}

    # 트리거 조건 확인
    if not should_trigger(tool_name, tool_input, tool_output):
        return 0

    # 마지막 수집 시간 확인 (1시간 이내면 스킵)
    last_time = get_last_collection_time()
    if last_time and datetime.now() - last_time < timedelta(hours=1):
        print(f"[INFO] 최근 수집 완료 ({last_time.strftime('%H:%M')}), 스킵")
        return 0

    # 데이터 수집 실행
    print("[COLLECT] SQL Trading 데이터 자동 수집 시작...")
    result = run_collection()

    if result["success"]:
        print(f"[OK] 데이터 수집 완료: {result['collected_at']}")
    else:
        print(f"[FAIL] 데이터 수집 실패: {result.get('error', 'Unknown error')}")

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
