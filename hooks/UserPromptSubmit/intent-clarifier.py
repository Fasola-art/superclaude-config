#!/usr/bin/env python3
"""
모호한 프롬프트 감지 → 명확화 유도 Hook

Hook Type: UserPromptSubmit
Matcher: "" (모든 프롬프트)

모호성 점수 ≥ threshold → 명확화 질문 출력
모호성 점수 < threshold → 무출력 (정상 진행)
"""

import json
import os
import sys
from pathlib import Path

# jarvis 모듈 경로 추가
sys.path.insert(0, str(Path.home() / ".claude" / "jarvis"))

CONFIG_PATH = Path.home() / ".claude" / "superclaude-config.json"


def load_config() -> dict:
    """설정에서 intentDetection 섹션 로드"""
    default = {"enabled": True, "ambiguityThreshold": 0.60, "minKeywords": 2}
    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        return config.get("intentDetection", default)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def main() -> None:
    config = load_config()

    if not config.get("enabled", True):
        return

    prompt = os.environ.get("PROMPT", "").strip()
    if not prompt:
        return

    # 슬래시 커맨드나 짧은 인사말은 스킵
    if prompt.startswith("/") or len(prompt) < 3:
        return

    threshold = config.get("ambiguityThreshold", 0.60)
    min_kw = config.get("minKeywords", 2)

    try:
        from nlu.ambiguity import calculate_ambiguity

        result = calculate_ambiguity(prompt, min_keywords=min_kw)
    except ImportError:
        return
    except Exception:
        return

    if result.score < threshold:
        return

    # 모호성 감지됨 → 명확화 유도 출력
    parts = [f"❓ 의도 확인 (모호성: {result.score:.0%})"]

    if result.suggestions:
        parts.append(f"   → {result.suggestions[0]}")

    if result.top_intents and result.top_intents[0].intent.name != "UNKNOWN":
        intent_names = [r.intent.name for r in result.top_intents[:2]]
        parts.append(f"   후보: {', '.join(intent_names)}")

    # 1줄 최대 출력 (hook 효율 규칙)
    print(" | ".join(parts))


if __name__ == "__main__":
    main()
