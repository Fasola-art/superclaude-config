#!/usr/bin/env python3
"""SQL 관련 Hook 공유 유틸리티"""

import json
import os
from datetime import datetime
from pathlib import Path

ALERTS_FILE = Path.home() / ".claude" / "modules" / "sql-trading" / "alerts.jsonl"
COLLECTION_STATE = Path.home() / ".claude" / "modules" / "sql-trading" / ".collection_state.json"

# SQL 트리거 키워드
SQL_TRIGGER_KEYWORDS = ["psql", "SELECT", "INSERT", "sql-trading", "claude_mcp"]


def should_trigger_sql(tool_name: str, tool_input: dict) -> bool:
    """SQL 관련 Hook 트리거 조건 확인"""
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        return any(kw in command for kw in SQL_TRIGGER_KEYWORDS)
    if tool_name == "Skill":
        return tool_input.get("skill", "") in ("sql", "sql-trading")
    return False


def get_tool_context() -> tuple[str, dict, str]:
    """환경변수에서 도구 정보 추출: (tool_name, tool_input, tool_output)"""
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    tool_output = os.environ.get("CLAUDE_TOOL_OUTPUT", "")
    try:
        tool_input = json.loads(os.environ.get("CLAUDE_TOOL_INPUT", "{}"))
    except json.JSONDecodeError:
        tool_input = {}
    return tool_name, tool_input, tool_output


def save_alerts(alerts: list[dict]) -> None:
    """알림을 JSONL 파일에 저장"""
    if not alerts:
        return
    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERTS_FILE, "a", encoding="utf-8") as f:
        for alert in alerts:
            f.write(json.dumps(alert, ensure_ascii=False) + "\n")


def make_alert(alert_type: str, message: str, priority: str = "medium") -> dict:
    """알림 딕셔너리 생성"""
    return {
        "type": alert_type,
        "message": message,
        "priority": priority,
        "timestamp": datetime.now().isoformat(),
    }
