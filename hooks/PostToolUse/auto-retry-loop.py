#!/usr/bin/env python3
"""
Check-Act Auto-Retry Loop Hook

Hook Type: PostToolUse
Matcher: Edit|Write

Edit/Write 후 syntax/type check 실행 → 실패 시 피드백 출력
Claude가 피드백을 읽고 수정 → 자연스러운 재시도 루프
"""

import json
import os
import sys
from pathlib import Path

# Windows UTF-8 출력 강제
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path.home() / ".claude" / "jarvis"))

CONFIG_PATH = Path.home() / ".claude" / "superclaude-config.json"
STATE_FILE = Path.home() / ".claude" / "cache" / "retry-state.json"


def load_config() -> dict:
    """autoRetry 설정 로드"""
    default = {"enabled": True, "maxRetries": 5, "passThreshold": 0.90,
               "skipPatterns": [".json", ".md", ".env", ".yaml"]}
    try:
        with open(CONFIG_PATH, encoding='utf-8') as f:
            return json.load(f).get("autoRetry", default)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def load_state() -> dict:
    """현재 재시도 상태 로드"""
    try:
        with open(STATE_FILE, encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state: dict) -> None:
    """재시도 상태 저장"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding='utf-8') as f:
        json.dump(state, f, indent=2)


def reset_state() -> None:
    """상태 리셋"""
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def main() -> None:
    config = load_config()
    if not config.get("enabled", True):
        return

    tool_name = os.environ.get("TOOL_NAME", "")
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return

    file_path = os.environ.get("FILE_PATH", "")
    if not file_path:
        return

    # 스킵 패턴 체크
    skip_patterns = config.get("skipPatterns", [])
    if any(file_path.endswith(pat) for pat in skip_patterns):
        return

    max_retries = config.get("maxRetries", 5)
    threshold = config.get("passThreshold", 0.90)

    # 현재 상태 로드
    state = load_state()
    current_file = state.get("file", "")
    attempt = state.get("attempt", 0)

    # 파일이 바뀌면 상태 리셋
    if current_file != file_path:
        attempt = 0

    attempt += 1

    # 최대 시도 초과 시 리셋
    if attempt > max_retries:
        reset_state()
        return

    try:
        from quality.gate_runner import run_gates
        from quality.feedback import generate_feedback

        result = run_gates(file_path)

        if result.score >= threshold:
            # 통과 → 상태 리셋
            reset_state()
            if attempt > 1:
                print(f"[OK] Auto-Retry 성공 ({attempt}회차, 점수: {result.score:.0%})")
            return

        # 실패 → 상태 저장 + 피드백 출력
        save_state({"file": file_path, "attempt": attempt})
        feedback = generate_feedback(result, attempt, max_retries)
        if feedback:
            print(feedback)

    except ImportError:
        return
    except Exception:
        return


if __name__ == "__main__":
    main()
