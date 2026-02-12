#!/usr/bin/env python3
"""
페이퍼 트레이드 + 무역 통계 시드 생성기

대상 테이블: trading_paper_trades, trade_statistics
"""

import random
import sys
from datetime import datetime, timedelta

from _db_utils import count_table, run_sql


def seed_paper_trades(verbose: bool = True) -> int:
    """페이퍼 트레이드 시드 (20건)"""
    if count_table("trading_paper_trades") > 0:
        if verbose:
            print("  ℹ️ paper_trades 이미 존재, 스킵")
        return 0

    random.seed(77)
    symbols = ["SBLK", "ZIM", "BTC", "ETH", "DBC", "GOGL", "FRO", "SOL", "XRP", "GSG"]
    strategies = ["Momentum", "Mean Reversion", "Breakout", "EMA Crossover"]

    values = []
    now = datetime.now()
    for _ in range(20):
        ts = now - timedelta(days=random.randint(1, 30))
        symbol = random.choice(symbols)
        side = random.choice(["BUY", "SELL"])
        qty = round(random.uniform(10, 500), 2)
        entry = round(random.uniform(5, 200), 2)
        pnl_pct = round(random.uniform(-5, 8), 2)
        exit_price = round(entry * (1 + pnl_pct / 100), 2)
        pnl = round((exit_price - entry) * qty, 2)
        if side == "SELL":
            pnl = round((entry - exit_price) * qty, 2)
        strategy = random.choice(strategies)
        values.append(
            f"('{ts.isoformat()}', '{symbol}', '{side}', {qty}, "
            f"{entry}, {exit_price}, {pnl}, {pnl_pct}, '{strategy}')"
        )

    sql = ("INSERT INTO trading_paper_trades "
           "(timestamp, symbol, side, quantity, entry_price, "
           "exit_price, pnl, pnl_pct, strategy) "
           "VALUES\n" + ",\n".join(values) + ";")
    run_sql(sql)
    if verbose:
        print(f"  ✅ paper_trades: {len(values)}건")
    return len(values)


def seed_trade_statistics(verbose: bool = True) -> int:
    """무역 통계 시드"""
    if count_table("trade_statistics") > 0:
        if verbose:
            print("  ℹ️ trade_statistics 이미 존재, 스킵")
        return 0

    random.seed(55)
    partners = [
        ("US", "미국"), ("CN", "중국"), ("JP", "일본"),
        ("DE", "독일"), ("VN", "베트남"),
    ]
    periods = ["202507", "202508", "202509", "202510", "202511", "202512", "202601"]

    values = []
    for partner_code, partner_name in partners:
        for period in random.sample(periods, 4):
            export_val = round(random.uniform(3000, 15000) * 1_000_000, 0)
            import_val = round(random.uniform(2500, 12000) * 1_000_000, 0)
            for flow, val in [("X", export_val), ("M", import_val)]:
                values.append(
                    f"('{period}', 'KR', '한국', '{partner_code}', "
                    f"'{partner_name}', '{flow}', 'TOTAL', '총계', "
                    f"{val}, NULL, NULL, NULL, 'seed')"
                )

    sql = ("INSERT INTO trade_statistics "
           "(period, reporter_code, reporter_name, partner_code, partner_name, "
           "flow_code, commodity_code, commodity_desc, trade_value, "
           "net_weight, qty, qty_unit, source) "
           "VALUES\n" + ",\n".join(values) + ";")
    run_sql(sql)
    if verbose:
        print(f"  ✅ trade_statistics: {len(values)}건")
    return len(values)


def collect_and_save(verbose: bool = True) -> int:
    """페이퍼 트레이드 + 무역 통계 시드 생성"""
    return seed_paper_trades(verbose) + seed_trade_statistics(verbose)


if __name__ == "__main__":
    try:
        print("🎯 트레이드/무역 시드 생성 중...")
        collect_and_save()
    except Exception as e:
        print(f"❌ 실패: {e}")
        sys.exit(1)
