"""트레이딩 시그널 API 라우터"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from db import fetch_all, fetch_one
from routers.signals_daily import router as daily_router

router = APIRouter()
router.include_router(daily_router)


@router.get("/latest")
def get_latest_signals() -> list[dict[str, Any]]:
    """최근 시그널"""
    rows = fetch_all("""
        SELECT symbol, signal_type, confidence, price,
               target_price, stop_loss, strategy, reason, timestamp
        FROM trading_signals
        WHERE timestamp > NOW() - INTERVAL '24 hours'
        ORDER BY timestamp DESC
        LIMIT 20
    """)
    return rows


@router.get("/strategy")
def get_strategy_status() -> list[dict[str, Any]]:
    """전략별 성과"""
    rows = fetch_all("""
        SELECT strategy,
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE signal_type IN ('BUY', 'STRONG_BUY')) as buys,
            COUNT(*) FILTER (WHERE signal_type IN ('SELL', 'STRONG_SELL')) as sells,
            ROUND(AVG(confidence)::numeric, 4) as avg_confidence
        FROM trading_signals
        WHERE timestamp > NOW() - INTERVAL '7 days'
        GROUP BY strategy
        ORDER BY total DESC
    """)
    return rows


@router.get("/backtest")
def get_backtest_results() -> list[dict[str, Any]]:
    """백테스팅 결과"""
    rows = fetch_all("""
        SELECT strategy, start_date, end_date, total_trades,
               win_rate, sharpe_ratio, max_drawdown, total_return
        FROM trading_backtest_results
        ORDER BY created_at DESC
        LIMIT 10
    """)
    return rows


@router.get("/risk")
def get_risk_status() -> dict[str, Any]:
    """리스크 현황"""
    latest = fetch_one("""
        SELECT level, event_type, description,
               daily_pnl_pct, total_drawdown_pct, timestamp
        FROM trading_risk_events
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    events = fetch_all("""
        SELECT level, event_type, description, daily_pnl_pct, timestamp
        FROM trading_risk_events
        WHERE timestamp > NOW() - INTERVAL '7 days'
        ORDER BY timestamp DESC
        LIMIT 20
    """)
    return {"current": latest, "recent_events": events}


@router.get("/paper")
def get_paper_trades() -> list[dict[str, Any]]:
    """페이퍼 트레이딩"""
    rows = fetch_all("""
        SELECT symbol, side, quantity, entry_price, exit_price,
               pnl, pnl_pct, strategy, timestamp
        FROM trading_paper_trades
        ORDER BY timestamp DESC
        LIMIT 30
    """)
    return rows
