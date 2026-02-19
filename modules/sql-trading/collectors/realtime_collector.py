#!/usr/bin/env python3
"""
실시간 시장 데이터 수집기 (Realtime Market Collector)

데이터 소스:
- Alpha Vantage: 핵심 종목 (조정가 포함, 25회/일 제한)
- FRED: BDI(발틱운임지수), 경제지표 (무제한)
- Yahoo Finance: 나머지 종목 (백업)

Version: 2.0.0
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

try:
    import yfinance as yf
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf


# API 키 로드
def load_api_keys() -> Dict[str, str]:
    """API 키 로드"""
    keys_file = Path.home() / ".claude/credentials/api-keys.json"
    if keys_file.exists():
        with open(keys_file) as f:
            data = json.load(f)
            return {
                "alpha_vantage": data.get("alpha_vantage", {}).get("api_key", ""),
                "fred": data.get("fred", {}).get("keys", [{}])[0].get("key", ""),
            }
    return {}


API_KEYS = load_api_keys()


def _escape_sql(value: str) -> str:
    """단순 SQL 문자열 이스케이프"""
    return value.replace("'", "''")

# 추적 종목 정의
WATCHLIST = {
    # Dry Bulk 해운주 (BDI 연동) - 원자재 경기 민감
    "dry_bulk": {
        "SBLK": "Star Bulk Carriers",
        "DSX": "Diana Shipping",
        "EGLE": "Eagle Bulk Shipping",
        "NMM": "Navios Maritime Partners",
        "GNK": "Genco Shipping",
    },
    # 컨테이너 해운 - 소비재 경기
    "container": {
        "ZIM": "ZIM Integrated Shipping",
        "MATX": "Matson Inc",
        "DAC": "Danaos Corporation",
    },
    # 탱커 - 에너지 경기
    "tanker": {
        "FRO": "Frontline Ltd",
        "STNG": "Scorpio Tankers",
        "TNK": "Teekay Tankers",
    },
    # 원자재 ETF
    "commodity": {
        "DBC": "Invesco DB Commodity",
        "GSG": "iShares S&P GSCI",
        "DBA": "Invesco DB Agriculture",
        "DBB": "Invesco DB Base Metals",
    },
    # 경기 지표
    "index": {
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones",
        "^IXIC": "NASDAQ",
    },
    # 크립토 연계 주식
    "crypto_equity": {
        "BMNR": "BitMine",
        "DFDV": "DFDV",
    },
}

# Alpha Vantage: 신뢰성 중요한 ETF/지수만 (25회/일 제한)
# 6시간 간격으로만 호출해 일일 한도 초과를 방지
ALPHA_VANTAGE_SYMBOLS = ["DBC", "GSG", "DBA", "DBB"]  # 원자재 ETF만
ALPHA_VANTAGE_HOURS = {0, 6, 12, 18}


def fetch_alpha_vantage(symbol: str) -> Optional[Dict[str, Any]]:
    """Alpha Vantage에서 데이터 수집 (조정가 포함)"""
    api_key = API_KEYS.get("alpha_vantage")
    if not api_key:
        return None

    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        resp = requests.get(url, timeout=10)
        data = resp.json()

        if "Global Quote" not in data:
            return None

        quote = data["Global Quote"]
        price = float(quote.get("05. price", 0))
        prev_close = float(quote.get("08. previous close", 0))
        change_pct = float(quote.get("10. change percent", "0%").replace("%", ""))
        volume = int(quote.get("06. volume", 0))

        # 섹터 찾기
        sector = "unknown"
        name = symbol
        for sec, syms in WATCHLIST.items():
            if symbol in syms:
                sector = sec
                name = syms[symbol]
                break

        return {
            "symbol": symbol,
            "name": name,
            "price": round(price, 4),
            "change_pct": round(change_pct, 4),
            "volume": volume,
            "sector": sector,
            "source": "alpha_vantage",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        print(f"⚠️ Alpha Vantage {symbol} 실패: {e}")
        return None


def fetch_fred_bdi() -> Optional[Dict[str, Any]]:
    """FRED에서 BDI(발틱운임지수) 수집"""
    api_key = API_KEYS.get("fred")
    if not api_key:
        return None

    try:
        # DBDI: Baltic Dry Index
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id=DBDI&api_key={api_key}&file_type=json&sort_order=desc&limit=5"
        resp = requests.get(url, timeout=10)
        data = resp.json()

        observations = data.get("observations", [])
        if len(observations) < 2:
            return None

        # 유효한 값 찾기 (. 이 아닌 것)
        values = []
        for obs in observations:
            if obs["value"] != ".":
                values.append(float(obs["value"]))
                if len(values) >= 2:
                    break

        if len(values) < 2:
            return None

        current = values[0]
        prev = values[1]
        change_pct = ((current - prev) / prev) * 100

        return {
            "index_name": "BDI",
            "route": "Baltic Dry Index",
            "value": int(current),
            "change_pct": round(change_pct, 2),
            "date": observations[0]["date"],
            "source": "fred",
        }

    except Exception as e:
        print(f"⚠️ FRED BDI 수집 실패: {e}")
        return None


def fetch_fred_indicators() -> List[Dict[str, Any]]:
    """FRED에서 경제지표 수집"""
    api_key = API_KEYS.get("fred")
    if not api_key:
        return []

    indicators = [
        ("T10Y2Y", "10Y-2Y Spread", "금리"),  # 장단기 금리차
        ("BAMLH0A0HYM2", "HY Spread", "신용"),  # 하이일드 스프레드
        ("DCOILWTICO", "WTI Oil", "에너지"),  # WTI 유가
        ("DCOILBRENTEU", "Brent Oil", "에너지"),  # 브렌트유
    ]

    results = []
    for series_id, name, category in indicators:
        try:
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&sort_order=desc&limit=5"
            resp = requests.get(url, timeout=10)
            data = resp.json()

            observations = data.get("observations", [])
            values = [float(o["value"]) for o in observations if o["value"] != "."][:2]

            if len(values) >= 2:
                change_pct = ((values[0] - values[1]) / abs(values[1])) * 100 if values[1] != 0 else 0
                results.append({
                    "series_id": series_id,
                    "name": name,
                    "category": category,
                    "value": round(values[0], 4),
                    "change_pct": round(change_pct, 2),
                    "date": observations[0]["date"],
                    "source": "fred",
                })

        except Exception as e:
            print(f"⚠️ FRED {series_id} 실패: {e}")

    return results


def fetch_yfinance(symbols: List[str]) -> List[Dict[str, Any]]:
    """Yahoo Finance에서 시장 데이터 수집 (백업)"""
    results = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d", interval="1m")
            if hist.empty:
                hist = ticker.history(period="5d")

            if hist.empty:
                continue

            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
            change_pct = ((current - prev) / prev) * 100
            volume = int(hist['Volume'].iloc[-1]) if hist['Volume'].iloc[-1] else 0

            # 섹터 찾기
            sector = "unknown"
            name = symbol
            for sec, syms in WATCHLIST.items():
                if symbol in syms:
                    sector = sec
                    name = syms[symbol]
                    break

            results.append({
                "symbol": symbol,
                "name": name,
                "price": round(float(current), 4),
                "change_pct": round(float(change_pct), 4),
                "volume": volume,
                "sector": sector,
                "source": "yfinance",
                "timestamp": datetime.now().isoformat(),
            })

        except Exception as e:
            print(f"⚠️ yfinance {symbol} 실패: {e}")

    return results


def generate_market_sql(data: List[Dict[str, Any]]) -> str:
    """시장 데이터 INSERT SQL 생성"""
    if not data:
        return ""

    values = []
    for d in data:
        asset_type = "etf" if d["sector"] in ["commodity", "index"] else "stock"
        metadata = json.dumps({
            "sector": d["sector"],
            "name": d["name"],
            "source": d.get("source", "unknown")
        })

        values.append(
            f"(NOW(), '{_escape_sql(d['symbol'])}', {d['price']}, {d['change_pct']}, "
            f"{d['volume']}, '{_escape_sql(asset_type)}', "
            f"'{_escape_sql(d.get('source', 'unknown'))}', '{_escape_sql(metadata)}')"
        )

    return """INSERT INTO market_snapshots
(timestamp, symbol, price, change_pct, volume, asset_type, source, metadata)
VALUES
""" + ",\n".join(values) + ";"


def generate_freight_sql(bdi: Optional[Dict[str, Any]]) -> str:
    """운임지수 INSERT SQL 생성"""
    if not bdi:
        return ""

    return f"""INSERT INTO freight_indices
(date, index_name, route, value, change_pct, source)
VALUES
('{_escape_sql(bdi['date'])}', '{_escape_sql(bdi['index_name'])}', '{_escape_sql(bdi['route'])}', {bdi['value']}, {bdi['change_pct']}, 'fred')
ON CONFLICT (date, index_name, route) DO UPDATE SET
value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;"""


def generate_indicators_sql(indicators: List[Dict[str, Any]]) -> str:
    """경제지표 INSERT SQL 생성"""
    if not indicators:
        return ""

    values = []
    for ind in indicators:
        values.append(
            f"('{_escape_sql(ind['series_id'])}', '{_escape_sql(ind['date'])}', {ind['value']}, "
            f"{ind['change_pct']}, '{_escape_sql(ind['category'])}', 'medium')"
        )

    return """INSERT INTO economic_indicators
(series_id, date, value, change_pct, category, importance)
VALUES
""" + ",\n".join(values) + """
ON CONFLICT (series_id, date) DO UPDATE SET
value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;"""


def save_to_db(sql: str) -> bool:
    """psql로 DB에 저장"""
    if not sql:
        return False

    psql_paths = [
        "/opt/homebrew/opt/postgresql@16/bin/psql",
        "/opt/homebrew/bin/psql",
        "/usr/local/bin/psql",
        "psql",
    ]

    psql_cmd = None
    for path in psql_paths:
        if Path(path).exists() or path == "psql":
            psql_cmd = path
            break

    if not psql_cmd:
        print("❌ psql을 찾을 수 없습니다")
        return False

    try:
        result = subprocess.run(
            [psql_cmd, "-U", "reim", "-d", "claude_mcp", "-c", sql],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ DB 저장 실패: {e}")
        return False


def collect_all(save_db: bool = True, verbose: bool = True) -> Dict[str, Any]:
    """전체 데이터 수집 및 저장"""
    all_data = []
    sources_used = []

    # 1. Alpha Vantage로 핵심 종목 수집 (일일 한도 보호)
    now_hour = datetime.now().hour
    if API_KEYS.get("alpha_vantage") and now_hour in ALPHA_VANTAGE_HOURS:
        if verbose:
            print("📡 Alpha Vantage 데이터 수집 중...")
        for symbol in ALPHA_VANTAGE_SYMBOLS:
            data = fetch_alpha_vantage(symbol)
            if data:
                all_data.append(data)
        if all_data:
            sources_used.append("alpha_vantage")

    # 2. yfinance로 나머지 종목 수집
    all_symbols = []
    for sector_symbols in WATCHLIST.values():
        all_symbols.extend(sector_symbols.keys())

    # Alpha Vantage로 수집한 종목 제외
    collected_symbols = {d["symbol"] for d in all_data}
    remaining_symbols = [s for s in all_symbols if s not in collected_symbols]

    if remaining_symbols:
        if verbose:
            print(f"📊 yfinance {len(remaining_symbols)}개 종목 수집 중...")
        yf_data = fetch_yfinance(remaining_symbols)
        all_data.extend(yf_data)
        if yf_data:
            sources_used.append("yfinance")

    # 3. FRED에서 BDI 수집
    bdi = None
    indicators = []
    if API_KEYS.get("fred"):
        if verbose:
            print("🏛️ FRED 경제지표 수집 중...")
        bdi = fetch_fred_bdi()
        indicators = fetch_fred_indicators()
        if bdi or indicators:
            sources_used.append("fred")

    if verbose:
        print(f"\n🚢 {len(all_data)}개 종목 데이터 수집 완료")
        print("=" * 60)

    # 출력
    if verbose:
        for d in sorted(all_data, key=lambda x: x["sector"]):
            emoji = "📈" if d["change_pct"] > 0 else "📉" if d["change_pct"] < 0 else "➡️"
            src = "🔷" if d.get("source") == "alpha_vantage" else "🔶"
            print(f"{emoji} {d['symbol']:5} | ${d['price']:10.2f} | {d['change_pct']:+7.2f}% | {d['name']} {src}")

        if bdi:
            print(f"\n📊 BDI: {bdi['value']} ({bdi['change_pct']:+.2f}%)")

        if indicators:
            print("\n📈 경제지표:")
            for ind in indicators:
                print(f"   • {ind['name']}: {ind['value']:.2f} ({ind['change_pct']:+.2f}%)")

        print("=" * 60)

    # DB 저장
    if save_db:
        # 시장 데이터
        market_sql = generate_market_sql(all_data)
        if market_sql:
            if save_to_db(market_sql):
                if verbose:
                    print(f"✅ {len(all_data)}개 시장 레코드 저장")
            else:
                if verbose:
                    print("❌ 시장 데이터 저장 실패")

        # BDI
        freight_sql = generate_freight_sql(bdi)
        if freight_sql:
            if save_to_db(freight_sql):
                if verbose:
                    print("✅ BDI 데이터 저장")

        # 경제지표
        indicators_sql = generate_indicators_sql(indicators)
        if indicators_sql:
            if save_to_db(indicators_sql):
                if verbose:
                    print(f"✅ {len(indicators)}개 경제지표 저장")

    # 섹터별 요약
    summary = {}
    for d in all_data:
        sector = d["sector"]
        if sector not in summary:
            summary[sector] = {"count": 0, "avg_change": 0, "symbols": []}
        summary[sector]["count"] += 1
        summary[sector]["avg_change"] += d["change_pct"]
        summary[sector]["symbols"].append(d["symbol"])

    for sector in summary:
        summary[sector]["avg_change"] /= summary[sector]["count"]
        summary[sector]["avg_change"] = round(summary[sector]["avg_change"], 2)

    return {
        "collected_at": datetime.now().isoformat(),
        "sources": sources_used,
        "total_records": len(all_data),
        "data": all_data,
        "bdi": bdi,
        "indicators": indicators,
        "summary": summary,
    }


def main():
    """메인 실행"""
    import argparse

    parser = argparse.ArgumentParser(description="실시간 시장 데이터 수집기 v2.0")
    parser.add_argument("--no-db", action="store_true", help="DB 저장 안함")
    parser.add_argument("--json", action="store_true", help="JSON 출력")
    parser.add_argument("--quiet", action="store_true", help="출력 최소화")
    args = parser.parse_args()

    result = collect_all(
        save_db=not args.no_db,
        verbose=not args.quiet
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    # 섹터 요약 출력
    if not args.quiet:
        print("\n📊 섹터별 요약:")
        for sector, info in result["summary"].items():
            emoji = "📈" if info["avg_change"] > 0 else "📉"
            print(f"  {emoji} {sector:12} | 평균 {info['avg_change']:+6.2f}% | {info['count']}종목")

        print(f"\n🔷 Alpha Vantage  🔶 yfinance")
        print(f"📡 소스: {', '.join(result['sources'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
