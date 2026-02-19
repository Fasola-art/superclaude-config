"""암호화폐 API 라우터"""
from fastapi import APIRouter
from db import fetch_all

router = APIRouter()


@router.get("/prices")
def get_crypto_prices():
    """주요 코인 시세"""
    rows = fetch_all("""
        SELECT DISTINCT ON (symbol)
            symbol, price_usd, price_krw, change_pct_24h,
            volume_24h, market_cap, timestamp
        FROM crypto_prices
        ORDER BY symbol, timestamp DESC
        LIMIT 20
    """)
    return rows


@router.get("/kimchi")
def get_kimchi_premium():
    """김치프리미엄"""
    rows = fetch_all("""
        SELECT DISTINCT ON (symbol)
            symbol, global_price_usd, korea_price_krw,
            exchange_rate, premium_pct, timestamp
        FROM kimchi_premium
        ORDER BY symbol, timestamp DESC
    """)
    return rows


@router.get("/dominance")
def get_dominance():
    """비트코인 도미넌스 (market_cap 비율 계산)"""
    rows = fetch_all("""
        SELECT DISTINCT ON (symbol)
            symbol, market_cap
        FROM crypto_prices
        WHERE market_cap IS NOT NULL
        ORDER BY symbol, timestamp DESC
    """)
    total = sum(float(r.get("market_cap") or 0) for r in rows)
    btc_cap = next((float(r["market_cap"]) for r in rows if r["symbol"] == "BTC"), 0)
    return {
        "btc_dominance": round(btc_cap / total * 100, 2) if total > 0 else 0,
        "total_market_cap": total,
    }
