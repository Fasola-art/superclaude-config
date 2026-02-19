"""전일 추천 성과 계산 테스트"""
from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Any, Callable
from zoneinfo import ZoneInfo

from routers.signals_daily import build_daily_performance

FetchAll = Callable[[str, tuple[object, ...] | None], list[dict[str, Any]]]
FetchOne = Callable[[str, tuple[object, ...] | None], dict[str, Any] | None]


def build_fetchers(
    all_returns: list[list[dict[str, Any]]],
    one_returns: list[dict[str, Any] | None],
) -> tuple[FetchAll, FetchOne]:
    """fetch_all/fetch_one 스텁을 생성한다."""
    all_queue = list(all_returns)
    one_queue = list(one_returns)

    def fetch_all(_: str, __: tuple[object, ...] | None = None) -> list[dict[str, Any]]:
        """큐에 적재된 fetch_all 결과를 반환한다."""
        return all_queue.pop(0)

    def fetch_one(_: str, __: tuple[object, ...] | None = None) -> dict[str, Any] | None:
        """큐에 적재된 fetch_one 결과를 반환한다."""
        return one_queue.pop(0)

    return fetch_all, fetch_one


def test_daily_performance_fallback_to_latest_signal() -> None:
    """전일 시그널이 없을 때 최신 시그널 날짜로 윈도우를 보정한다."""
    ny = ZoneInfo("America/New_York")
    kst = ZoneInfo("Asia/Seoul")
    now_ny = datetime(2026, 2, 17, 10, 0, tzinfo=ny)
    latest_ts = datetime(2026, 2, 14, 12, 0, tzinfo=ny)
    start_open = datetime.combine(latest_ts.date(), time(9, 30), ny)
    end_open = start_open + timedelta(days=1)

    signals = [{"symbol": "AAPL", "signal_type": "BUY", "price": 100, "timestamp": latest_ts}]
    fetch_all, fetch_one = build_fetchers(
        all_returns=[[], signals],
        one_returns=[{"ts": latest_ts}, {"price": 110, "timestamp": end_open + timedelta(minutes=1)}],
    )

    result = build_daily_performance(fetch_all, fetch_one, now_ny)

    assert result["summary"]["wins"] == 1
    assert result["summary"]["losses"] == 0
    assert result["summary"]["flats"] == 0
    assert result["summary"]["win_rate"] == 100.0
    assert result["window"]["start_kst"] == start_open.astimezone(kst).isoformat()


def test_daily_performance_flat_outcome() -> None:
    """1% 이내 변동은 횡보로 계산한다."""
    ny = ZoneInfo("America/New_York")
    now_ny = datetime(2026, 2, 17, 10, 0, tzinfo=ny)
    signal_ts = datetime(2026, 2, 16, 10, 0, tzinfo=ny)

    signals = [{"symbol": "MSFT", "signal_type": "SELL", "price": 100, "timestamp": signal_ts}]
    fetch_all, fetch_one = build_fetchers(
        all_returns=[signals],
        one_returns=[{"price": 100.5, "timestamp": signal_ts + timedelta(hours=1)}],
    )

    result = build_daily_performance(fetch_all, fetch_one, now_ny)

    assert result["summary"]["flats"] == 1
    assert result["summary"]["win_rate"] == 0
    assert result["items"][0]["outcome"] == "flat"
