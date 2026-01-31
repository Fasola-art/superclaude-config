#!/usr/bin/env python3
"""
한국어 응답 강제 Hook
- 한국어 응답 설정 확인
- 코드 주석도 한국어로
"""

import os
import json
from pathlib import Path

SETTINGS_FILE = Path.home() / ".claude" / "settings.json"

def check_language_setting():
    """언어 설정 확인 및 알림"""
    # 첫 프롬프트에서만 표시
    state_file = Path.home() / ".claude" / "cache" / "lang-reminded.json"

    if state_file.exists():
        return

    # 알림 표시
    print("🌏 응답 언어: 한국어 (코드 주석 포함)")

    # 상태 저장
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, 'w') as f:
        json.dump({"reminded": True}, f)

if __name__ == "__main__":
    check_language_setting()
