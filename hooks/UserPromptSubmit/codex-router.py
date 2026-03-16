#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codex Router Hook
- 코덱스/에이전트 위임에 적합한 작업 감지
- 이미 /codex 명시된 경우 건너뜀
- 클로드 전담 패턴은 제외
- 1줄 안내 출력
"""

import sys
import os
import io
import json
import re
from pathlib import Path

# Windows UTF-8 처리
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# 코덱스 위임 적합 키워드
CODEX_PATTERNS = {
    "optimization": [
        r"최적화", r"optimize", r"refactor", r"리팩토링", r"성능\s*개선",
        r"performance\s*improve", r"속도.*느림", r"메모리.*최적"
    ],
    "bug_fix": [
        r"버그\s*수정", r"bug\s*fix", r"오류\s*수정", r"에러\s*고쳐",
        r"fix\s*error", r"수정해줘.*오류", r"고쳐줘"
    ],
    "algorithm": [
        r"알고리즘", r"algorithm", r"정렬", r"sort", r"탐색", r"search.*구현",
        r"자료구조", r"data\s*structure"
    ],
    "security": [
        r"보안\s*취약", r"security\s*vuln", r"xss", r"sql\s*injection",
        r"csrf", r"취약점\s*수정"
    ],
    "duplicate_code": [
        r"중복\s*코드", r"duplicate\s*code", r"반복.*제거", r"DRY",
        r"코드.*정리", r"cleanup\s*code"
    ],
    "bulk_implementation": [
        r"전부\s*구현", r"모두\s*만들어", r"파일\s*\d+개", r"여러\s*파일",
        r"테스트.*전체", r"crud.*구현", r"api.*전부"
    ],
    "migration": [
        r"마이그레이션", r"migration", r"이전", r"포팅", r"porting",
        r"업그레이드.*코드", r"레거시.*변환"
    ]
}

# 클로드 전담 패턴 (제외)
CLAUDE_EXCLUSIVE = [
    r"어떻게\s*설계", r"아키텍처", r"architecture", r"설계.*해줘",
    r"어떤\s*방식", r"전략.*세워", r"계획.*짜줘", r"방향.*잡아",
    r"요구사항", r"기획", r"PRD", r"기능\s*정의"
]

# 이미 위임 명시된 패턴
ALREADY_DELEGATED = [
    r"/codex", r"코덱스\s*위임", r"codex\s*delegate",
    r"코덱스로\s*넘겨", r"코덱스한테\s*맡겨"
]

STATE_FILE = Path(__file__).parent.parent.parent / "cache" / "codex-router-state.json"


def detect_codex_task(prompt: str) -> tuple[bool, str]:
    """코덱스 적합 작업 감지. (감지됨, 카테고리)"""
    prompt_lower = prompt.lower()

    # 이미 /codex 명시된 경우 건너뜀
    for pattern in ALREADY_DELEGATED:
        if re.search(pattern, prompt, re.IGNORECASE):
            return False, ""

    # 클로드 전담 패턴 제외
    for pattern in CLAUDE_EXCLUSIVE:
        if re.search(pattern, prompt, re.IGNORECASE):
            return False, ""

    # 코덱스 적합 패턴 감지
    for category, patterns in CODEX_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return True, category

    return False, ""


def get_category_label(category: str) -> str:
    """카테고리 한국어 레이블"""
    labels = {
        "optimization": "최적화/리팩토링",
        "bug_fix": "버그 수정",
        "algorithm": "알고리즘/자료구조",
        "security": "보안 취약점",
        "duplicate_code": "중복 코드 제거",
        "bulk_implementation": "대량 구현",
        "migration": "코드 마이그레이션"
    }
    return labels.get(category, category)


def save_state(category: str) -> None:
    """감지 상태 저장"""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        state = {"last_detected": category, "count": 0}
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
                state["count"] = existing.get("count", 0) + 1
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)
    except Exception:
        pass


def main() -> None:
    # 환경 변수 또는 stdin에서 프롬프트 읽기
    prompt = os.environ.get("PROMPT", "")
    if not prompt and not sys.stdin.isatty():
        try:
            raw = sys.stdin.read()
            data = json.loads(raw)
            prompt = data.get("prompt", raw)
        except (json.JSONDecodeError, Exception):
            prompt = raw if "raw" in dir() else ""

    if not prompt:
        return

    detected, category = detect_codex_task(prompt)

    if detected:
        label = get_category_label(category)
        save_state(category)
        # 1줄 출력 (Efficiency Rules)
        print(f"[CODEX] {label} 감지 → /codex 로 위임하거나 계속 진행")


if __name__ == "__main__":
    main()
