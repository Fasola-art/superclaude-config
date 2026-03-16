#!/usr/bin/env python3
"""
Auto Context Manager Hook
- 주제 변화 감지 시 /clear 권장
- 컨텍스트 70% 이상 시 /compact 권장
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import datetime

STATE_FILE = Path.home() / ".claude" / "cache" / "context-manager-state.json"
HISTORY_SIZE = 5  # 최근 N개 프롬프트 저장
SIMILARITY_THRESHOLD = 0.08  # 유사도 임계값 (낮으면 주제 변화)
CONTEXT_THRESHOLD_PERCENT = 70
SESSION_THRESHOLD_MINUTES = 30

# 새 기능 개발 키워드 (명시적 트리거)
NEW_FEATURE_PATTERNS = [
    r"새\s*(기능|feature)",
    r"new\s*feature",
    r"기능\s*개발",
    r"새로\s*만들",
    r"처음부터",
    r"from\s*scratch",
    r"새\s*프로젝트",
    r"new\s*project",
]

# 불용어 (의미 없는 단어)
STOPWORDS = {
    "해줘", "해주세요", "좀", "이", "그", "저", "를", "을", "에", "에서", "로", "으로",
    "하고", "해서", "있는", "없는", "하는", "되는", "the", "a", "an", "is", "are",
    "to", "for", "and", "or", "in", "on", "at", "with", "please", "can", "you",
    "어떻게", "뭐", "무엇", "어디", "왜", "언제", "이거", "저거", "그거",
    "만들어줘", "작성해줘", "추가해줘", "수정해줘", "삭제해줘", "확인해줘",
    "알려줘", "설명해줘", "도와줘", "보여줘", "찾아줘", "고쳐줘", "설정해줘",
}


def get_input_data() -> dict:
    """stdin에서 입력 데이터 읽기"""
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, KeyError):
        return {}


def extract_keywords(text: str) -> set[str]:
    """텍스트에서 키워드 추출"""
    # 한글, 영문, 숫자만 추출
    words = re.findall(r"[가-힣a-zA-Z0-9]+", text.lower())
    # 2글자 이상, 불용어 제외
    return {w for w in words if len(w) >= 2 and w not in STOPWORDS}


def jaccard_similarity(set1: set, set2: set) -> float:
    """Jaccard 유사도 계산"""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def load_state() -> dict:
    """상태 파일 로드"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "session_start": datetime.now().isoformat(),
        "last_compact_suggestion": None,
        "recent_keywords": [],  # 최근 프롬프트 키워드들
        "current_topic_keywords": set(),  # 현재 주제 키워드
    }


def save_state(state: dict) -> None:
    """상태 파일 저장"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    # set을 list로 변환
    state_copy = state.copy()
    if isinstance(state_copy.get("current_topic_keywords"), set):
        state_copy["current_topic_keywords"] = list(state_copy["current_topic_keywords"])
    with open(STATE_FILE, "w", encoding='utf-8') as f:
        json.dump(state_copy, f)


def estimate_context_usage() -> int:
    """컨텍스트 사용량 추정 (%)"""
    session_dir = Path.home() / ".claude" / "projects"
    if not session_dir.exists():
        return 0
    jsonl_files = list(session_dir.rglob("*.jsonl"))
    if not jsonl_files:
        return 0
    latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
    size_mb = latest.stat().st_size / (1024 * 1024)
    return min(int(size_mb * 50), 100)


def get_session_duration_minutes(state: dict) -> int:
    """세션 경과 시간 (분)"""
    try:
        start = datetime.fromisoformat(state.get("session_start", datetime.now().isoformat()))
        return int((datetime.now() - start).total_seconds() / 60)
    except (ValueError, TypeError):
        return 0


def detect_topic_change(current_keywords: set, state: dict) -> bool:
    """주제 변화 감지"""
    recent = state.get("recent_keywords", [])
    if len(recent) < 2:
        return False  # 히스토리 부족

    # 최근 키워드들을 합쳐서 현재 주제 추정
    topic_keywords = set()
    for kw_list in recent[-HISTORY_SIZE:]:
        topic_keywords.update(kw_list)

    # 현재 프롬프트와 유사도 비교
    similarity = jaccard_similarity(current_keywords, topic_keywords)

    # 유사도가 낮으면 주제 변화
    return similarity < SIMILARITY_THRESHOLD and len(current_keywords) >= 2


def is_new_feature_request(prompt: str) -> bool:
    """새 기능 개발 키워드 감지"""
    for pattern in NEW_FEATURE_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return True
    return False


def main():
    input_data = get_input_data()
    prompt = input_data.get("prompt", "")
    if not prompt:
        return

    state = load_state()
    messages = []
    should_reset = False

    # 현재 프롬프트 키워드 추출
    current_keywords = extract_keywords(prompt)

    # 1. 명시적 키워드 감지 (우선)
    if is_new_feature_request(prompt):
        messages.append("[TIP] New feature keyword -> /clear recommended")
        should_reset = True
    # 2. 주제 변화 감지 (키워드 없을 때)
    elif detect_topic_change(current_keywords, state):
        messages.append("[TOPIC] Topic change detected -> /clear recommended")
        should_reset = True

    if should_reset:
        state["session_start"] = datetime.now().isoformat()
        state["recent_keywords"] = []

    # 2. 컨텍스트 체크 (30분+ & 70%+)
    duration = get_session_duration_minutes(state)
    usage = estimate_context_usage()

    if duration >= SESSION_THRESHOLD_MINUTES and usage >= CONTEXT_THRESHOLD_PERCENT:
        last_suggestion = state.get("last_compact_suggestion")
        should_suggest = True
        if last_suggestion:
            try:
                last_time = datetime.fromisoformat(last_suggestion)
                if (datetime.now() - last_time).total_seconds() < 600:
                    should_suggest = False
            except (ValueError, TypeError):
                pass
        if should_suggest:
            messages.append(f"[CTX] CTX:{usage}% ({duration}min) -> /compact")
            state["last_compact_suggestion"] = datetime.now().isoformat()

    # 키워드 히스토리 업데이트
    recent = state.get("recent_keywords", [])
    recent.append(list(current_keywords))
    state["recent_keywords"] = recent[-HISTORY_SIZE:]

    save_state(state)

    if messages:
        print(" | ".join(messages))


if __name__ == "__main__":
    main()
