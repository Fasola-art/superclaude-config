#!/usr/bin/env python3
"""
암호화폐 API 수집 함수

CoinGecko, Upbit, 환율 API 호출
"""

import subprocess
import sys
from typing import Any

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

# 추적 코인 목록 (CoinGecko ID → 심볼)
COINS = {
    "bitcoin": "BTC", "ethereum": "ETH", "binancecoin": "BNB",
    "ripple": "XRP", "solana": "SOL", "cardano": "ADA",
    "dogecoin": "DOGE", "avalanche-2": "AVAX",
}

# Upbit 마켓 코드 매핑
UPBIT_MARKETS = {
    "BTC": "KRW-BTC", "ETH": "KRW-ETH", "XRP": "KRW-XRP",
    "SOL": "KRW-SOL", "ADA": "KRW-ADA", "DOGE": "KRW-DOGE",
    "AVAX": "KRW-AVAX",
}


def fetch_coingecko() -> dict[str, dict[str, Any]]:
    """CoinGecko에서 USD 시세 수집"""
    ids = ",".join(COINS.keys())
    url = (f"https://api.coingecko.com/api/v3/simple/price?ids={ids}"
           f"&vs_currencies=usd&include_market_cap=true"
           f"&include_24hr_vol=true&include_24hr_change=true")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    result = {}
    for cg_id, symbol in COINS.items():
        if cg_id in data:
            d = data[cg_id]
            result[symbol] = {
                "price_usd": d.get("usd", 0),
                "market_cap": d.get("usd_market_cap", 0),
                "volume_24h": d.get("usd_24h_vol", 0),
                "change_pct_24h": round(d.get("usd_24h_change", 0), 2),
            }
    return result


def fetch_upbit_prices() -> dict[str, float]:
    """Upbit에서 KRW 시세 수집"""
    markets = ",".join(UPBIT_MARKETS.values())
    url = f"https://api.upbit.com/v1/ticker?markets={markets}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    result = {}
    reverse_map = {v: k for k, v in UPBIT_MARKETS.items()}
    for ticker in resp.json():
        symbol = reverse_map.get(ticker["market"])
        if symbol:
            result[symbol] = float(ticker["trade_price"])
    return result


def fetch_exchange_rate() -> float:
    """USD/KRW 환율 조회"""
    url = "https://open.er-api.com/v6/latest/USD"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return float(resp.json()["rates"]["KRW"])
