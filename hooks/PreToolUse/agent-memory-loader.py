#!/usr/bin/env python3
"""
Task 실행 전 에이전트 메모리 로드 → 프롬프트에 주입

Hook Type: PreToolUse
Matcher: Task

agent_type + project_path로 상위 K개 메모리 조회 후 출력
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude" / "jarvis"))

CONFIG_PATH = Path.home() / ".claude" / "superclaude-config.json"


def load_config() -> dict:
    """agentMemory 설정 로드"""
    default = {"enabled": True, "maxPerAgent": 50, "retentionDays": 30, "topK": 5}
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f).get("agentMemory", default)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


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
    agent_type = tool_input.get("subagent_type", "general-purpose")
    project_path = os.environ.get("PROJECT_PATH", os.getcwd())

    try:
        from memory.agent_memory import AgentMemory

        mem = AgentMemory(
            max_per_agent=config.get("maxPerAgent", 50),
            retention_days=config.get("retentionDays", 30),
        )
        entries = mem.load(
            agent_type=agent_type,
            project_path=project_path,
            top_k=config.get("topK", 5),
        )
        output = mem.format_for_prompt(entries)
        if output:
            print(output)
    except ImportError:
        return
    except Exception:
        return


if __name__ == "__main__":
    main()
