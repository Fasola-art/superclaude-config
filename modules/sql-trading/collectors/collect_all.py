#!/usr/bin/env python3
"""
통합 데이터 수집 오케스트레이터

모든 수집기를 순서대로 실행하고 결과를 보고한다.
사용법:
  python3 collect_all.py           # 전체 실행
  python3 collect_all.py --seed    # 시드 데이터만
  python3 collect_all.py --api     # API 수집만
"""

import argparse
import sys
import time

from _db_utils import DB, PSQL, count_table

# 수집기 정의: (모듈명, 설명, 타입)
COLLECTORS = [
    ("crypto_collector", "암호화폐 시세 + 김프", "api"),
    ("rates_collector", "금리 데이터", "api"),
    ("news_collector", "시장 뉴스", "api"),
    ("translate_news", "뉴스 한글 번역", "api"),
    ("realestate_collector", "부동산 지수 시드", "seed"),
    ("seed_backtest_risk", "백테스트/리스크 시드", "seed"),
    ("seed_paper_trade", "트레이드/무역 시드", "seed"),
    ("analyze_news", "FinBERT 감정분석", "api"),
    ("telegram_briefing", "텔레그램 브리핑", "api"),
]

# 검증 대상 테이블
TABLES = [
    "crypto_prices", "kimchi_premium", "interest_rates",
    "realestate_indices", "market_news", "trading_backtest_results",
    "trading_risk_events", "trading_paper_trades", "trade_statistics",
]


def run_collector(module_name: str, desc: str) -> tuple[bool, int]:
    """개별 수집기 실행"""
    try:
        mod = __import__(module_name)
        count = mod.collect_and_save(verbose=True)
        return True, count
    except Exception as e:
        print(f"  ❌ {desc} 실패: {e}")
        return False, 0


def main() -> int:
    """메인 실행"""
    parser = argparse.ArgumentParser(description="통합 데이터 수집기")
    parser.add_argument("--seed", action="store_true", help="시드 데이터만 실행")
    parser.add_argument("--api", action="store_true", help="API 수집만 실행")
    args = parser.parse_args()

    run_api = not args.seed
    run_seed = not args.api

    print("=" * 50)
    print("📊 마켓브리핑 데이터 수집 시작")
    print("=" * 50)

    start = time.time()
    total_success = 0
    total_count = 0

    for module_name, desc, ctype in COLLECTORS:
        if ctype == "api" and not run_api:
            continue
        if ctype == "seed" and not run_seed:
            continue

        print(f"\n{'─' * 40}")
        print(f"▶ {desc} ({module_name})")
        success, count = run_collector(module_name, desc)
        if success:
            total_success += 1
            total_count += count

    elapsed = time.time() - start

    # 검증
    print(f"\n{'=' * 50}")
    print("📋 테이블별 데이터 현황")
    print(f"{'=' * 50}")
    for table in TABLES:
        cnt = count_table(table)
        status = "✅" if cnt > 0 else "❌"
        print(f"  {status} {table:30} {cnt:>6}건")

    print(f"\n⏱️ 소요시간: {elapsed:.1f}초")
    print(f"📊 실행: {total_success}/{len(COLLECTORS)}개 수집기, {total_count}건 추가")
    return 0


if __name__ == "__main__":
    sys.exit(main())
