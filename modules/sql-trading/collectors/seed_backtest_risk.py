#!/usr/bin/env python3
"""
백테스트 결과 + 리스크 이벤트 시드 생성기

대상 테이블: trading_backtest_results, trading_risk_events
"""

import random
import sys
from datetime import datetime, timedelta

from _db_utils import count_table, escape_sql, run_sql


def seed_backtest(verbose: bool = True) -> int:
    """백테스트 결과 시드 (5건)"""
    if count_table("trading_backtest_results") > 0:
        if verbose:
            print("  ℹ️ backtest_results 이미 존재, 스킵")
        return 0

    strategies = [
        ("Momentum", 156, 58.3, 1.85, 12.4, 24.7),
        ("Mean Reversion", 203, 52.1, 1.42, 15.8, 18.3),
        ("Breakout", 89, 45.2, 0.95, 18.2, 12.1),
        ("EMA Crossover", 134, 61.8, 2.05, 8.6, 31.5),
        ("MACD Divergence", 112, 54.7, 1.28, 14.1, 19.8),
    ]

    values = []
    for name, trades, wr, sharpe, mdd, ret in strategies:
        values.append(
            f"('{name}', '2025-01-01', '2026-01-31', {trades}, "
            f"{wr}, {sharpe}, {mdd}, {ret})"
        )

    sql = ("INSERT INTO trading_backtest_results "
           "(strategy, start_date, end_date, total_trades, "
           "win_rate, sharpe_ratio, max_drawdown, total_return) "
           "VALUES\n" + ",\n".join(values) + ";")
    run_sql(sql)
    if verbose:
        print(f"  ✅ backtest_results: {len(values)}건")
    return len(values)


def seed_risk_events(verbose: bool = True) -> int:
    """리스크 이벤트 시드 (15건)"""
    if count_table("trading_risk_events") > 0:
        if verbose:
            print("  ℹ️ risk_events 이미 존재, 스킵")
        return 0

    random.seed(99)
    events = [
        ("NORMAL", "daily_pnl", "일일 PnL 정상 범위", 1.2, 2.1, "모니터링 유지"),
        ("NORMAL", "daily_pnl", "일일 PnL 정상 범위", 0.8, 1.8, "모니터링 유지"),
        ("NORMAL", "daily_pnl", "소폭 손실 발생", -0.5, 2.5, "모니터링 유지"),
        ("WARNING", "drawdown", "드로다운 5% 초과", -2.1, 5.3, "포지션 축소 검토"),
        ("NORMAL", "daily_pnl", "수익 실현", 2.8, 1.2, "모니터링 유지"),
        ("NORMAL", "volatility", "변동성 정상", 0.3, 1.9, "모니터링 유지"),
        ("WARNING", "daily_pnl", "급격한 손실", -3.2, 7.1, "손절매 실행"),
        ("NORMAL", "daily_pnl", "소폭 수익", 0.6, 3.8, "모니터링 유지"),
        ("CRITICAL", "drawdown", "최대 드로다운 경고", -3.5, 10.2, "전 포지션 청산"),
        ("NORMAL", "daily_pnl", "반등 수익", 1.8, 8.5, "모니터링 유지"),
        ("NORMAL", "daily_pnl", "정상 거래", 0.4, 7.2, "모니터링 유지"),
        ("WARNING", "concentration", "포지션 집중도 경고", -1.5, 6.8, "분산 투자 조정"),
        ("NORMAL", "daily_pnl", "소폭 수익", 1.1, 5.9, "모니터링 유지"),
        ("NORMAL", "daily_pnl", "정상 범위", 0.2, 5.5, "모니터링 유지"),
        ("NORMAL", "daily_pnl", "안정적 수익", 0.9, 4.8, "모니터링 유지"),
    ]

    values = []
    now = datetime.now()
    for i, (level, etype, desc, pnl, dd, action) in enumerate(events):
        ts = now - timedelta(days=30 - i * 2)
        values.append(
            f"('{ts.isoformat()}', '{level}', '{etype}', "
            f"'{escape_sql(desc)}', {pnl}, {dd}, '{escape_sql(action)}')"
        )

    sql = ("INSERT INTO trading_risk_events "
           "(timestamp, level, event_type, description, "
           "daily_pnl_pct, total_drawdown_pct, action_taken) "
           "VALUES\n" + ",\n".join(values) + ";")
    run_sql(sql)
    if verbose:
        print(f"  ✅ risk_events: {len(values)}건")
    return len(values)


def collect_and_save(verbose: bool = True) -> int:
    """백테스트 + 리스크 시드 생성"""
    return seed_backtest(verbose) + seed_risk_events(verbose)


if __name__ == "__main__":
    try:
        print("🎯 백테스트/리스크 시드 생성 중...")
        collect_and_save()
    except Exception as e:
        print(f"❌ 실패: {e}")
        sys.exit(1)
