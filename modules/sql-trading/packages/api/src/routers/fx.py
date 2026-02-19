"""외환 API 라우터"""
import json
import time
from datetime import datetime, timezone
from urllib.request import urlopen

try:
    import requests
except ImportError as exc:  # pragma: no cover - runtime dependency
    requests = None

from fastapi import APIRouter, HTTPException

router = APIRouter()

_CACHE = {"ts": 0.0, "data": None}
_FUTURES_CACHE: dict[str, dict] = {}
_YAHOO = {"session": None, "crumb": "", "ts": 0.0}

FX_SYMBOLS = {
    "EURUSD": "6E=F",
    "USDJPY": "6J=F",
    "GBPUSD": "6B=F",
    "USDCNH": "USDCNH=X",
}

INTERVAL_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "60m",
    "6h": "60m",
    "1d": "1d",
    "1w": "1wk",
    "1mo": "1mo",
}

RANGE_MAP = {
    "1m": "5d",
    "5m": "60d",
    "15m": "60d",
    "30m": "60d",
    "1h": "6mo",
    "6h": "6mo",
    "1d": "5y",
    "1w": "10y",
    "1mo": "max",
}


def _fetch_rates() -> dict:
    url = "https://open.er-api.com/v6/latest/USD"
    if requests is None:
        raise HTTPException(status_code=500, detail="requests not available")

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    session.get("https://fc.yahoo.com", timeout=10)
    crumb_resp = session.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10)
    crumb = crumb_resp.text.strip()

    params = {"interval": interval, "range": range_, "crumb": crumb}
    resp = session.get(url, params=params, timeout=10)
    resp.raise_for_status()
    payload = resp.json()

    if payload.get("result") != "success":
        raise HTTPException(status_code=502, detail="FX API error")

    rates = payload.get("rates", {})
    usd = rates.get("USD")
    krw = rates.get("KRW")
    if not usd or not krw:
        raise HTTPException(status_code=502, detail="FX API missing USD/KRW")

    currencies = ["USD", "EUR", "JPY", "GBP", "CNY"]
    items = []
    for cur in currencies:
        rate = rates.get(cur)
        if not rate:
            continue
        rate_krw = krw if cur == "USD" else krw / rate
        items.append({
            "currency": cur,
            "rate_usd": round(rate / usd, 6),
            "rate_krw": round(rate_krw, 6),
        })

    as_of = payload.get("time_last_update_utc")
    if not as_of:
        as_of = datetime.now(timezone.utc).isoformat()

    return {
        "base": "USD",
        "as_of": as_of,
        "rates": items,
    }


@router.get("/rates")
def get_fx_rates():
    now = time.time()
    cached = _CACHE.get("data")
    if cached and (now - _CACHE.get("ts", 0)) < 60:
        return cached

    data = _fetch_rates()
    _CACHE["ts"] = now
    _CACHE["data"] = data
    return data


def _fetch_chart(symbol: str, interval: str, range_: str) -> list[dict]:
    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + symbol
    if requests is None:
        raise HTTPException(status_code=500, detail="requests not available")

    session = _YAHOO["session"]
    if session is None:
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0"})
        _YAHOO["session"] = session

    if not _YAHOO["crumb"] or (time.time() - _YAHOO["ts"]) > 21600:
        session.get("https://fc.yahoo.com", timeout=10)
        crumb_resp = session.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10)
        _YAHOO["crumb"] = crumb_resp.text.strip()
        _YAHOO["ts"] = time.time()

    params = {"interval": interval, "range": range_, "crumb": _YAHOO["crumb"]}
    resp = session.get(url, params=params, timeout=10)
    if resp.status_code == 429:
        session.get("https://fc.yahoo.com", timeout=10)
        crumb_resp = session.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10)
        _YAHOO["crumb"] = crumb_resp.text.strip()
        _YAHOO["ts"] = time.time()
        params["crumb"] = _YAHOO["crumb"]
        resp = session.get(url, params=params, timeout=10)
    resp.raise_for_status()
    payload = resp.json()

    result = payload.get("chart", {}).get("result")
    if not result:
        raise HTTPException(status_code=502, detail="FX chart API error")

    data = result[0]
    ts = data.get("timestamp") or []
    quote = data.get("indicators", {}).get("quote", [{}])[0]

    bars = []
    opens = quote.get("open") or []
    highs = quote.get("high") or []
    lows = quote.get("low") or []
    closes = quote.get("close") or []
    vols = quote.get("volume") or []

    for i, t in enumerate(ts):
        if i >= len(opens) or i >= len(highs) or i >= len(lows) or i >= len(closes):
            continue
        o = opens[i]
        h = highs[i]
        l = lows[i]
        c = closes[i]
        v = vols[i] if i < len(vols) else 0
        if None in (o, h, l, c):
            continue
        bars.append({
            "t": int(t),
            "o": float(o),
            "h": float(h),
            "l": float(l),
            "c": float(c),
            "v": int(v or 0),
        })
    return bars


def _aggregate_chunk(chunk: list[dict]) -> dict:
    return {
        "t": chunk[0]["t"],
        "o": chunk[0]["o"],
        "h": max(b["h"] for b in chunk),
        "l": min(b["l"] for b in chunk),
        "c": chunk[-1]["c"],
        "v": sum(b["v"] for b in chunk),
    }


def _downsample_6h(bars: list[dict]) -> list[dict]:
    if not bars:
        return []
    grouped = []
    chunk = []
    for bar in bars:
        chunk.append(bar)
        if len(chunk) == 6:
            grouped.append(_aggregate_chunk(chunk))
            chunk = []
    if chunk:
        grouped.append(_aggregate_chunk(chunk))
    return grouped


@router.get("/futures")
def get_fx_futures(symbol: str, interval: str = "1h"):
    key = f"{symbol}:{interval}"
    now = time.time()
    cached = _FUTURES_CACHE.get(key)
    if cached and (now - cached.get("ts", 0)) < 60:
        return cached["data"]

    src = FX_SYMBOLS.get(symbol)
    if not src:
        raise HTTPException(status_code=400, detail="Unsupported symbol")

    iv = INTERVAL_MAP.get(interval)
    if not iv:
        raise HTTPException(status_code=400, detail="Unsupported interval")

    range_ = RANGE_MAP.get(interval, "1mo")
    try:
        bars = _fetch_chart(src, iv, range_)
    except Exception as exc:
        print(f"FX chart error: {exc}")
        if cached:
            return cached["data"]
        raise HTTPException(status_code=503, detail="FX chart unavailable") from exc
    if interval == "6h":
        bars = _downsample_6h(bars)

    note = "spot" if symbol == "USDCNH" else "futures"
    data = {
        "symbol": symbol,
        "source_symbol": src,
        "interval": interval,
        "note": note,
        "bars": bars,
    }
    _FUTURES_CACHE[key] = {"ts": now, "data": data}
    return data
