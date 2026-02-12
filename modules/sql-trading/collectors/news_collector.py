#!/usr/bin/env python3
"""시장 뉴스 수집기 — Brave Search API, URL 기반 중복 방지"""

import json
import sys
import time
from pathlib import Path

import requests

from _db_utils import escape_sql, query_rows, run_sql

SEARCH_QUERIES = {
    "stocks": "stock market today Wall Street",
    "crypto": "bitcoin ethereum crypto market news",
    "realestate": "한국 부동산 시장 동향 아파트",
    "economy": "경제 지표 금리 인플레이션 GDP",
}


def load_brave_key() -> str:
    """Brave Search API 키 로드"""
    keys_file = Path.home() / ".claude/credentials/api-keys.json"
    with open(keys_file) as f:
        return json.load(f)["brave_search"]["keys"]["free"]


def fetch_brave_news(api_key: str, query: str, count: int = 5) -> list[dict]:
    """Brave Search에서 뉴스 검색"""
    resp = requests.get(
        "https://api.search.brave.com/res/v1/web/search",
        headers={"Accept": "application/json", "X-Subscription-Token": api_key},
        params={"q": query, "count": count, "freshness": "pd"},
        timeout=15,
    )
    resp.raise_for_status()
    return [
        {"title": r.get("title", ""), "summary": r.get("description", ""),
         "url": r.get("url", ""),
         "source": r.get("meta_url", {}).get("hostname", "unknown")}
        for r in resp.json().get("web", {}).get("results", [])[:count]
    ]


def _existing_urls() -> set[str]:
    """최근 7일간 저장된 뉴스 URL (중복 방지용)"""
    return set(query_rows(
        "SELECT url FROM market_news WHERE timestamp > NOW() - INTERVAL '7 days';"
    ))


def collect_and_save(verbose: bool = True) -> int:
    """뉴스 수집 및 저장 (URL 기반 중복 제거)"""
    api_key = load_brave_key()
    known = _existing_urls()
    values: list[str] = []

    for i, (category, query) in enumerate(SEARCH_QUERIES.items()):
        if i > 0:
            time.sleep(1.5)
        try:
            articles = fetch_brave_news(api_key, query, count=5)
            new_count = 0
            for a in articles:
                if a["url"] in known:
                    continue
                known.add(a["url"])
                t = escape_sql(a["title"][:500])
                s = escape_sql(a["summary"][:1000])
                u = escape_sql(a["url"][:500])
                src = escape_sql(a["source"][:100])
                values.append(
                    f"(NOW(), '{t}', '{s}', '{u}', '{src}', '{category}')")
                new_count += 1
            if verbose:
                skip = len(articles) - new_count
                msg = f"    {category}: {new_count}건 신규"
                if skip:
                    msg += f" ({skip}건 중복 스킵)"
                print(msg)
        except Exception as e:
            if verbose:
                print(f"    ⚠️ {category} 실패: {e}")

    if not values:
        if verbose:
            print("  ℹ️ 새 소식 없음 — 모든 뉴스가 이미 수집됨")
        return 0

    sql = ("INSERT INTO market_news "
           "(timestamp, title, summary, url, source, category) "
           "VALUES\n" + ",\n".join(values) + ";")
    run_sql(sql)
    if verbose:
        print(f"  ✅ market_news: {len(values)}건 신규 저장")
    return len(values)


if __name__ == "__main__":
    try:
        print("📰 시장 뉴스 수집 중...")
        collect_and_save()
    except Exception as e:
        print(f"❌ 뉴스 수집 실패: {e}")
        sys.exit(1)
