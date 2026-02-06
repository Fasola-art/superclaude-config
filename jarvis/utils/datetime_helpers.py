#!/usr/bin/env python3
"""
날짜/시간 공통 헬퍼 함수
"""

from __future__ import annotations

from datetime import datetime, timedelta


def get_today_str() -> str:
    """오늘 날짜 문자열 (YYYY-MM-DD)"""
    return datetime.now().strftime('%Y-%m-%d')


def get_yesterday_str() -> str:
    """어제 날짜 문자열 (YYYY-MM-DD)"""
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


def get_tomorrow_str() -> str:
    """내일 날짜 문자열 (YYYY-MM-DD)"""
    return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')


def get_date_n_days_later(days: int) -> str:
    """N일 후 날짜 문자열 (YYYY-MM-DD)"""
    return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')


def format_datetime(dt: datetime, fmt: str = '%Y-%m-%d') -> str:
    """datetime 객체를 지정 포맷으로 변환"""
    return dt.strftime(fmt)


def parse_datetime(date_str: str, fmt: str = '%Y-%m-%d') -> datetime:
    """문자열을 datetime 객체로 파싱"""
    return datetime.strptime(date_str, fmt)


def get_next_weekday(target_weekday: int) -> datetime:
    """
    다음 주 특정 요일 반환

    Args:
        target_weekday: 요일 (0=월요일, 6=일요일)

    Returns:
        다음 주 해당 요일의 datetime
    """
    now = datetime.now()
    days_ahead = target_weekday - now.weekday() + 7
    if days_ahead <= 0:
        days_ahead += 7
    return now + timedelta(days=days_ahead)
