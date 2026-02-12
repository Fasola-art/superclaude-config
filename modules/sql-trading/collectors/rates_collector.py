#!/usr/bin/env python3
"""
금리 데이터 수집기

데이터 소스: FRED API
대상 테이블: interest_rates
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

from _db_utils import run_sql

# FRED 시리즈 정의: (series_id, rate_type, country)
FRED_SERIES = [
    ("FEDFUNDS", "기준금리", "US"),
    ("DFF", "연방기금실효금리", "US"),
    ("MORTGAGE30US", "30년주담대금리", "US"),
    ("DGS10", "10년국채수익률", "US"),
    ("DGS2", "2년국채수익률", "US"),
    ("IORB", "지급준비금이자율", "US"),
]


def load_fred_key() -> str:
    """FRED API 키 로드"""
    keys_file = Path.home() / ".claude/credentials/api-keys.json"
    with open(keys_file) as f:
        data = json.load(f)
    return data["fred"]["keys"][0]["key"]


def fetch_fred_series(api_key: str, series_id: str) -> dict[str, Any] | None:
    """FRED에서 시리즈 최신 값 조회"""
    url = (f"https://api.stlouisfed.org/fred/series/observations"
           f"?series_id={series_id}&api_key={api_key}"
           f"&file_type=json&sort_order=desc&limit=5")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    observations = resp.json().get("observations", [])

    # 유효한 값 찾기 ('.' 제외)
    for obs in observations:
        if obs["value"] != ".":
            return {"date": obs["date"], "value": float(obs["value"])}
    return None


def collect_and_save(verbose: bool = True) -> int:
    """금리 데이터 수집 및 저장"""
    api_key = load_fred_key()
    values = []

    for series_id, rate_type, country in FRED_SERIES:
        try:
            result = fetch_fred_series(api_key, series_id)
            if result:
                values.append(
                    f"('{result['date']}', '{rate_type}', {result['value']}, "
                    f"'{country}', 'fred')"
                )
                if verbose:
                    print(f"    {rate_type}: {result['value']}% ({result['date']})")
        except Exception as e:
            if verbose:
                print(f"    ⚠️ {series_id} 실패: {e}")

    if not values:
        return 0

    sql = ("INSERT INTO interest_rates (date, rate_type, rate_value, country, source) "
           "VALUES\n" + ",\n".join(values) + ";")
    run_sql(sql)

    if verbose:
        print(f"  ✅ interest_rates: {len(values)}건 저장")
    return len(values)


if __name__ == "__main__":
    try:
        print("🏛️ FRED 금리 데이터 수집 중...")
        collect_and_save()
    except Exception as e:
        print(f"❌ 금리 수집 실패: {e}")
        sys.exit(1)
