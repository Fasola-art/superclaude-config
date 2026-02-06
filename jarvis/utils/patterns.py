#!/usr/bin/env python3
"""
정규식 패턴 공통 모듈
"""

from __future__ import annotations

import re
from typing import Optional


# 날짜 패턴
DATE_PATTERN = re.compile(r"(\d{1,2})월\s*(\d{1,2})일")
NEXT_WEEK_PATTERN = re.compile(r"다음\s*주\s*([월화수목금토일]요일)")

# 시간 패턴
TIME_PATTERN = re.compile(r"(오전|오후)?\s*(\d{1,2})\s*시")

# 숫자 패턴
NUMBER_PATTERN = re.compile(r"\d+")

# 인용문 패턴
QUOTED_TEXT_PATTERN = re.compile(r'["\']([^"\']+)["\']')


# 요일 매핑
WEEKDAY_MAP = {
    "월요일": 0,
    "화요일": 1,
    "수요일": 2,
    "목요일": 3,
    "금요일": 4,
    "토요일": 5,
    "일요일": 6,
}


def extract_date_match(text: str) -> Optional[re.Match]:
    """날짜 패턴 매칭"""
    return DATE_PATTERN.search(text)


def extract_time_match(text: str) -> Optional[re.Match]:
    """시간 패턴 매칭"""
    return TIME_PATTERN.search(text)
