#!/usr/bin/env python3
"""
암호화폐 시세 + 김치프리미엄 수집기

데이터 소스: CoinGecko (USD) + Upbit (KRW)
대상 테이블: crypto_prices, kimchi_premium
"""

import sys

from _db_utils import run_sql
from crypto_api import fetch_coingecko, fetch_exchange_rate, fetch_upbit_prices


def insert_crypto_prices(usd_data: dict, krw_data: dict, exchange_rate: float) -> int:
    """crypto_prices 테이블에 INSERT"""
    values = []
    for symbol, d in usd_data.items():
        price_krw = krw_data.get(symbol, d["price_usd"] * exchange_rate)
        values.append(
            f"(NOW(), '{symbol}', {d['price_usd']}, {price_krw}, "
            f"{d['change_pct_24h']}, {d['volume_24h']}, {d['market_cap']}, 'coingecko')"
        )
    if values:
        sql = ("INSERT INTO crypto_prices "
               "(timestamp, symbol, price_usd, price_krw, "
               "change_pct_24h, volume_24h, market_cap, source) "
               "VALUES\n" + ",\n".join(values) + ";")
        run_sql(sql)
    return len(values)


def insert_kimchi_premium(usd_data: dict, krw_data: dict, exchange_rate: float) -> int:
    """kimchi_premium 테이블에 INSERT"""
    values = []
    for symbol, krw_price in krw_data.items():
        usd_info = usd_data.get(symbol)
        if not usd_info:
            continue
        expected_krw = usd_info["price_usd"] * exchange_rate
        premium = ((krw_price / expected_krw) - 1) * 100 if expected_krw > 0 else 0
        values.append(
            f"(NOW(), '{symbol}', {usd_info['price_usd']}, {krw_price}, "
            f"{exchange_rate}, {round(premium, 2)}, 'coingecko+upbit')"
        )
    if values:
        sql = ("INSERT INTO kimchi_premium "
               "(timestamp, symbol, global_price_usd, korea_price_krw, "
               "exchange_rate, premium_pct, source) "
               "VALUES\n" + ",\n".join(values) + ";")
        run_sql(sql)
    return len(values)


def collect_and_save(verbose: bool = True) -> int:
    """수집 및 DB 저장, INSERT 건수 반환"""
    usd_data = fetch_coingecko()
    krw_data = fetch_upbit_prices()
    exchange_rate = fetch_exchange_rate()

    if verbose:
        print(f"  📡 CoinGecko: {len(usd_data)}개, Upbit: {len(krw_data)}개, 환율: {exchange_rate:.0f}")

    crypto_count = insert_crypto_prices(usd_data, krw_data, exchange_rate)
    kimchi_count = insert_kimchi_premium(usd_data, krw_data, exchange_rate)

    if verbose:
        print(f"  ✅ crypto_prices: {crypto_count}건, kimchi_premium: {kimchi_count}건")
    return crypto_count + kimchi_count


if __name__ == "__main__":
    try:
        collect_and_save()
    except Exception as e:
        print(f"❌ 암호화폐 수집 실패: {e}")
        sys.exit(1)
