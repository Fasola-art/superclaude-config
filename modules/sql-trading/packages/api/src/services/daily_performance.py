"""전일 추천 성과 계산 유틸리티"""
from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Any, Callable
from zoneinfo import ZoneInfo

FetchAll = Callable[[str, tuple[object, ...] | None], list[dict[str, Any]]]
FetchOne = Callable[[str, tuple[object, ...] | None], dict[str, Any] | None]


def window_for_date(session_date: date, tz: ZoneInfo) -> tuple[datetime, datetime]:
    """미국장 시작(09:30 NY) 기준 하루 윈도우를 생성한다."""
    start_open = datetime.combine(session_date, time(9, 30), tz)
    return start_open, start_open + timedelta(days=1)


def load_signals(fetch_all_fn: FetchAll, start_open: datetime, end_open: datetime) -> list[dict[str, Any]]:
    """주어진 기간의 시그널을 조회한다."""
    return fetch_all_fn(
        """
        SELECT id, symbol, signal_type, price, timestamp
        FROM trading_signals
        WHERE timestamp >= %s AND timestamp < %s
          AND signal_type IN ('BUY', 'SELL', 'STRONG_BUY', 'STRONG_SELL')
        ORDER BY timestamp ASC
        """,
        (start_open, end_open),
    )


def resolve_window(
    fetch_all_fn: FetchAll,
    fetch_one_fn: FetchOne,
    now_ny: datetime,
) -> tuple[datetime, datetime, list[dict[str, Any]]]:
    """기본 윈도우가 비어있으면 최신 시그널 기준 윈도우로 대체한다."""
    ny = now_ny.tzinfo or ZoneInfo("America/New_York")
    start_open, end_open = window_for_date((now_ny - timedelta(days=1)).date(), ny)
    signals = load_signals(fetch_all_fn, start_open, end_open)
    if signals:
        return start_open, end_open, signals

    latest = fetch_one_fn("SELECT MAX(timestamp) as ts FROM trading_signals", None)
    if not latest or not latest.get("ts"):
        return start_open, end_open, []

    latest_ts = latest["ts"]
    if isinstance(latest_ts, datetime) and latest_ts.tzinfo is None:
        latest_ts = latest_ts.replace(tzinfo=ny)
    if isinstance(latest_ts, datetime):
        start_open, end_open = window_for_date(latest_ts.astimezone(ny).date(), ny)
        signals = load_signals(fetch_all_fn, start_open, end_open)
    return start_open, end_open, signals
