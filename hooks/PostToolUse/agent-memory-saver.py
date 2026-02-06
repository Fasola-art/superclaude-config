#!/usr/bin/env python3
"""
Task 실행 후 학습 내용 저장

Hook Type: PostToolUse
Matcher: Task

에이전트 결과에서 패턴/학습 추출 → UPSERT 저장
"""

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude" / "jarvis"))

CONFIG_PATH = Path.home() / ".claude" / "superclaude-config.json"

# 학습 추출 패턴
LEARNING_PATTERNS = [
    (r"(?:발견|found|discovered)[:：]\s*(.+)", "discovery"),
    (r"(?:해결|resolved|fixed)[:：]\s*(.+)", "resolution"),
    (r"(?:주의|warning|caution)[:：]\s*(.+)", "warning"),
    (r"(?:패턴|pattern)[:：]\s*(.+)", "pattern"),
    (r"(?:구조|structure|architecture)[:：]\s*(.+)", "architecture"),
]


def load_config() -> dict:
    """agentMemory 설정 로드"""
    default = {"enabled": True, "maxPerAgent": 50, "retentionDays": 30}
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f).get("agentMemory", default)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def extract_learnings(text: str) -> list[tuple[str, str]]:
    """에이전트 출력에서 학습 항목 추출"""
    learnings: list[tuple[str, str]] = []

    for pattern, category in LEARNING_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches[:2]:  # 패턴당 최대 2개
            cleaned = match.strip()[:200]  # 200자 제한
            if cleaned:
                learnings.append((category, cleaned))

    return learnings[:5]  # 최대 5개 학습


def main() -> None:
    config = load_config()
    if not config.get("enabled", True):
        return

    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        return

    if input_data.get("tool_name") != "Task":
        return

    tool_input = input_data.get("tool_input", {})
    tool_result = input_data.get("tool_result", {})

    agent_type = tool_input.get("subagent_type", "general-purpose")
    project_path = os.environ.get("PROJECT_PATH", os.getcwd())
    session_id = os.environ.get("SESSION_ID", "")
    result_text = str(tool_result.get("content", ""))

    if not result_text or len(result_text) < 20:
        return

    learnings = extract_learnings(result_text)
    if not learnings:
        return

    try:
        from memory.agent_memory import AgentMemory, MemoryEntry

        mem = AgentMemory(
            max_per_agent=config.get("maxPerAgent", 50),
            retention_days=config.get("retentionDays", 30),
        )

        for category, value in learnings:
            entry = MemoryEntry(
                agent_type=agent_type,
                context_key=f"{category}",
                context_value=value,
                project_path=project_path,
                session_id=session_id,
            )
            mem.save(entry)

        # 주기적 정리 (세이버 실행 시)
        mem.cleanup()
    except ImportError:
        return
    except Exception:
        return


if __name__ == "__main__":
    main()
