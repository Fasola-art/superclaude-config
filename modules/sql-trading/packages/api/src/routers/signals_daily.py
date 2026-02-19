"""전일 추천 성과 API 라우터"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter
from db import fetch_all, fetch_one
from services.daily_performance import FetchAll, FetchOne, resolve_window

router = APIRouter()


def build_daily_performance(
    fetch_all_fn: FetchAll,
    fetch_one_fn: FetchOne,
    now_ny: datetime,
) -> dict[str, Any]:
    """전일 추천 성과 데이터를 생성한다."""
    kst = ZoneInfo("Asia/Seoul")
    start_open_ny, end_open_ny, signals = resolve_window(fetch_all_fn, fetch_one_fn, now_ny)
    results: list[dict[str, Any]] = []
    wins = losses = flats = 0

    for signal in signals:
        entry_price = signal.get("price") or 0
        if entry_price <= 0:
            continue

        end_snap = fetch_one_fn(
            """
            SELECT price, timestamp
            FROM market_snapshots
            WHERE symbol = %s AND timestamp >= %s
            ORDER BY timestamp ASC
            LIMIT 1
            """,
            (signal["symbol"], end_open_ny),
        )
        if not end_snap:
            end_snap = fetch_one_fn(
                """
                SELECT price, timestamp
                FROM market_snapshots
                WHERE symbol = %s AND timestamp < %s
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (signal["symbol"], end_open_ny),
            )
        if not end_snap or not end_snap.get("price"):
            continue

        exit_price = end_snap["price"]
        pct_change = (exit_price - entry_price) / entry_price * 100

        if abs(pct_change) < 1:
            outcome = "flat"
            flats += 1
        else:
            is_buy = signal["signal_type"] in ("BUY", "STRONG_BUY")
            success = pct_change >= 1 if is_buy else pct_change <= -1
            outcome = "win" if success else "loss"
            if success:
                wins += 1
            else:
                losses += 1

        results.append(
            {
                "symbol": signal["symbol"],
                "signal_type": signal["signal_type"],
                "entry_time": signal["timestamp"],
                "entry_price": entry_price,
                "exit_time": end_snap["timestamp"],
                "exit_price": exit_price,
                "pct_change": round(pct_change, 4),
                "outcome": outcome,
            }
        )

    denom = wins + losses
    win_rate = round((wins / denom) * 100, 2) if denom > 0 else 0

    return {
        "window": {
            "start_kst": start_open_ny.astimezone(kst).isoformat(),
            "end_kst": end_open_ny.astimezone(kst).isoformat(),
        },
        "summary": {
            "total": len(results),
            "wins": wins,
            "losses": losses,
            "flats": flats,
            "win_rate": win_rate,
        },
        "items": results,
    }


@router.get("/daily-performance")
def get_daily_performance() -> dict[str, Any]:
    """어제 미국장 시작 기준 추천 성과"""
    ny = ZoneInfo("America/New_York")
    now_ny = datetime.now(ny)
    return build_daily_performance(fetch_all, fetch_one, now_ny)
