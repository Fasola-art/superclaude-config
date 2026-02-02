#!/usr/bin/env python3
"""
SQL 알림 모니터 훅 (PostToolUse)

트리거 조건:
- SQL 쿼리 실행 후
- 트레이딩 신호 테이블 변경 시

동작:
- 고신뢰도 신호 감지 시 알림
- 물류 지연 급증 시 알림
- 운임 급등/급락 시 알림

Version: 1.0.0
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


# 알림 임계값 설정
THRESHOLDS = {
    "signal_confidence": 0.8,      # 신호 신뢰도 임계값
    "delay_rate_increase": 5.0,    # 지연율 증가 임계값 (%)
    "freight_change": 10.0,        # 운임 변화 임계값 (%)
}


def check_high_confidence_signals(tool_output: str) -> list[dict]:
    """고신뢰도 트레이딩 신호 감지"""
    alerts = []

    # 신호 관련 키워드 및 패턴 확인
    keywords = ["BUY", "SELL", "confidence", "signal_type"]
    if not any(kw in tool_output for kw in keywords):
        return alerts

    # 신뢰도 임계값 초과 신호 감지 (간단한 패턴 매칭)
    # 실제로는 구조화된 출력 파싱 필요
    if "confidence" in tool_output and "0.8" in tool_output:
        alerts.append({
            "type": "HIGH_CONFIDENCE_SIGNAL",
            "message": "고신뢰도 트레이딩 신호 감지",
            "priority": "high",
            "timestamp": datetime.now().isoformat()
        })

    return alerts


def check_logistics_anomalies(tool_output: str) -> list[dict]:
    """물류 이상 감지"""
    alerts = []

    # 지연 관련 키워드 확인
    if "delay" in tool_output.lower() or "delayed" in tool_output.lower():
        # 지연율 급증 패턴 감지
        if "%" in tool_output:
            alerts.append({
                "type": "LOGISTICS_DELAY_ALERT",
                "message": "물류 지연 현황 확인 필요",
                "priority": "medium",
                "timestamp": datetime.now().isoformat()
            })

    return alerts


def check_freight_anomalies(tool_output: str) -> list[dict]:
    """운임 이상 감지"""
    alerts = []

    freight_keywords = ["BDI", "FBX", "freight", "운임"]
    if not any(kw in tool_output for kw in freight_keywords):
        return alerts

    # 운임 급변동 감지 (간단한 패턴)
    change_indicators = ["+10%", "-10%", "급등", "급락"]
    if any(ind in tool_output for ind in change_indicators):
        alerts.append({
            "type": "FREIGHT_CHANGE_ALERT",
            "message": "운임 지수 급변동 감지",
            "priority": "high",
            "timestamp": datetime.now().isoformat()
        })

    return alerts


def save_alerts(alerts: list[dict]) -> None:
    """알림 저장"""
    if not alerts:
        return

    alerts_file = Path.home() / ".claude" / "modules" / "sql-trading" / "alerts.jsonl"
    alerts_file.parent.mkdir(parents=True, exist_ok=True)

    with open(alerts_file, 'a', encoding='utf-8') as f:
        for alert in alerts:
            f.write(json.dumps(alert, ensure_ascii=False) + "\n")


def display_alerts(alerts: list[dict]) -> None:
    """알림 출력"""
    if not alerts:
        return

    print("\n" + "=" * 50)
    print("🚨 SQL Trading 알림")
    print("=" * 50)

    for alert in alerts:
        priority_emoji = "🔴" if alert["priority"] == "high" else "🟡"
        print(f"{priority_emoji} [{alert['type']}] {alert['message']}")

    print("=" * 50 + "\n")


def should_trigger(tool_name: str, tool_input: dict) -> bool:
    """훅 실행 조건 확인"""
    # Bash에서 psql 또는 SQL 관련 명령 실행 시
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        sql_keywords = ["psql", "SELECT", "INSERT", "sql-trading", "claude_mcp"]
        if any(kw in command for kw in sql_keywords):
            return True

    # Skill 도구에서 sql 관련 스킬 실행 시
    if tool_name == "Skill":
        skill = tool_input.get("skill", "")
        if skill in ["sql", "sql-trading"]:
            return True

    return False


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
    if not should_trigger(tool_name, tool_input):
        return 0

    # 알림 수집
    all_alerts = []
    all_alerts.extend(check_high_confidence_signals(tool_output))
    all_alerts.extend(check_logistics_anomalies(tool_output))
    all_alerts.extend(check_freight_anomalies(tool_output))

    # 알림 처리
    if all_alerts:
        save_alerts(all_alerts)
        display_alerts(all_alerts)

    return 0


if __name__ == "__main__":
    sys.exit(main())
