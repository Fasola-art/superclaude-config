#!/usr/bin/env python3
"""
SQL 알림 모니터 훅 (PostToolUse)
- 고신뢰도 신호 감지 시 알림
- 물류 지연 급증 시 알림
- 운임 급등/급락 시 알림
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude" / "hooks"))
from _shared.sql_utils import get_tool_context, should_trigger_sql, save_alerts, make_alert


def check_signals(output: str) -> list[dict]:
    """고신뢰도 트레이딩 신호 감지"""
    keywords = ["BUY", "SELL", "confidence", "signal_type"]
    if not any(kw in output for kw in keywords):
        return []
    if "confidence" in output and "0.8" in output:
        return [make_alert("HIGH_CONFIDENCE_SIGNAL", "고신뢰도 트레이딩 신호 감지", "high")]
    return []


def check_logistics(output: str) -> list[dict]:
    """물류 이상 감지"""
    lower = output.lower()
    if ("delay" in lower or "delayed" in lower) and "%" in output:
        return [make_alert("LOGISTICS_DELAY_ALERT", "물류 지연 현황 확인 필요")]
    return []


def check_freight(output: str) -> list[dict]:
    """운임 이상 감지"""
    if not any(kw in output for kw in ["BDI", "FBX", "freight", "운임"]):
        return []
    if any(ind in output for ind in ["+10%", "-10%", "급등", "급락"]):
        return [make_alert("FREIGHT_CHANGE_ALERT", "운임 지수 급변동 감지", "high")]
    return []


def display_alerts(alerts: list[dict]) -> None:
    """알림 출력"""
    if not alerts:
        return
    print("\n" + "=" * 40)
    for a in alerts:
        icon = "🔴" if a["priority"] == "high" else "🟡"
        print(f"{icon} [{a['type']}] {a['message']}")
    print("=" * 40)


def main() -> int:
    tool_name, tool_input, tool_output = get_tool_context()
    if not should_trigger_sql(tool_name, tool_input):
        return 0

    alerts = check_signals(tool_output) + check_logistics(tool_output) + check_freight(tool_output)
    if alerts:
        save_alerts(alerts)
        display_alerts(alerts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
