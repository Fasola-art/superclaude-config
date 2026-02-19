#!/usr/bin/env python3
"""
SQL 데이터 수집 훅 (PostToolUse)
- /sql 실행 시 자동으로 최신 물류/무역 데이터 수집
- 1시간 이내 수집 이력 있으면 스킵
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude" / "hooks"))
from _shared.sql_utils import get_tool_context, should_trigger_sql, COLLECTION_STATE

COLLECTOR = Path.home() / ".claude" / "modules" / "sql-trading" / "collectors" / "logistics_collector.py"


def get_last_collection() -> datetime | None:
    """마지막 수집 시간 확인"""
    if not COLLECTION_STATE.exists():
        return None
    try:
        ts = json.loads(COLLECTION_STATE.read_text()).get("last_collection")
        return datetime.fromisoformat(ts) if ts else None
    except Exception:
        return None


def run_collection() -> dict:
    """데이터 수집 실행"""
    if not COLLECTOR.exists():
        return {"success": False, "error": "수집기 파일 없음"}
    try:
        result = subprocess.run(
            [sys.executable, str(COLLECTOR)],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode == 0:
            COLLECTION_STATE.parent.mkdir(parents=True, exist_ok=True)
            COLLECTION_STATE.write_text(json.dumps({"last_collection": datetime.now().isoformat()}))
            return {"success": True, "collected_at": datetime.now().isoformat()}
        return {"success": False, "error": result.stderr}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "수집 타임아웃 (5분 초과)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main() -> int:
    tool_name, tool_input, tool_output = get_tool_context()
    if not should_trigger_sql(tool_name, tool_input):
        return 0

    last = get_last_collection()
    if last and datetime.now() - last < timedelta(hours=1):
        return 0

    result = run_collection()
    if result["success"]:
        print(f"✅ 데이터 수집 완료: {result['collected_at']}")
    else:
        print(f"❌ 수집 실패: {result.get('error', 'Unknown')}")
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
