#!/usr/bin/env python3
"""모든 Hook에서 공유하는 유틸리티"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

CLAUDE_DIR = Path.home() / ".claude"
CACHE_DIR = CLAUDE_DIR / "cache"

# 불용어 (한/영)
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


def load_state(name: str) -> dict:
    """캐시 디렉토리에서 상태 파일 로드"""
    state_file = CACHE_DIR / f"{name}.json"
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_state(name: str, data: dict) -> None:
    """캐시 디렉토리에 상태 파일 저장 (set→list 자동 변환)"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    state_file = CACHE_DIR / f"{name}.json"

    def serialize(obj: object) -> object:
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj

    with open(state_file, "w") as f:
        json.dump(data, f, default=serialize)


def extract_keywords(text: str) -> set[str]:
    """텍스트에서 키워드 추출 (한글+영문, 불용어 제외)"""
    words = re.findall(r"[가-힣a-zA-Z0-9]+", text.lower())
    return {w for w in words if len(w) >= 2 and w not in STOPWORDS}


def jaccard_similarity(set1: set, set2: set) -> float:
    """Jaccard 유사도 계산"""
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)
