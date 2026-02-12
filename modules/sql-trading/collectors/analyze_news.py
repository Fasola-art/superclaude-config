#!/usr/bin/env python3
"""
뉴스 감정분석 배치 처리기

미분석 뉴스 조회 → FinBERT 분석 → DB UPDATE
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _db_utils import DB, PSQL, escape_sql, run_sql
from sentiment_analyzer import analyze_batch

# 카테고리별 관련 심볼
CATEGORY_SYMBOLS = {
    "stocks": ["SPY", "QQQ", "AAPL", "MSFT"],
    "crypto": ["BTC", "ETH", "BNB", "SOL"],
    "economy": ["TLT", "GLD", "DXY"],
    "realestate": ["VNQ", "IYR", "XLRE"],
}


def fetch_unanalyzed(limit: int = 50) -> list[dict]:
    """미분석 뉴스 조회 (sentiment IS NULL)"""
    result = subprocess.run(
        [PSQL, "-U", "reim", "-d", DB, "-t", "-A", "-F", "|||", "-c",
         f"SELECT id, title, COALESCE(summary,''), category "
         f"FROM market_news WHERE sentiment IS NULL "
         f"ORDER BY timestamp DESC LIMIT {limit};"],
        capture_output=True, text=True, timeout=10,
    )
    if result.returncode != 0:
        return []
    rows = []
    for line in result.stdout.strip().split("\n"):
        parts = line.split("|||")
        if len(parts) >= 4:
            rows.append({"id": int(parts[0]), "title": parts[1],
                         "summary": parts[2], "category": parts[3]})
    return rows


def update_sentiment(nid: int, analysis: dict, category: str) -> None:
    """분석 결과 DB UPDATE"""
    score = analysis["score"]
    rec = analysis["recommendation"]
    meta = json.dumps({
        "positive": analysis["positive"], "negative": analysis["negative"],
        "neutral": analysis["neutral"], "recommendation": rec["label"],
        "rec_key": rec["key"],
    }, ensure_ascii=False)

    symbols = CATEGORY_SYMBOLS.get(category, [])
    sym_sql = f"ARRAY[{','.join(repr(s) for s in symbols)}]" if symbols else "NULL"

    run_sql(
        f"UPDATE market_news SET sentiment={score}, symbols={sym_sql}, "
        f"metadata='{escape_sql(meta)}'::jsonb WHERE id={nid};"
    )


def collect_and_save(verbose: bool = True) -> int:
    """미분석 뉴스 전체 배치 분석"""
    rows = fetch_unanalyzed()
    if not rows:
        if verbose:
            print("  ℹ️ 미분석 뉴스 없음")
        return 0
    if verbose:
        print(f"  📊 {len(rows)}건 분석 시작...")

    texts = [f"{r['title']}. {r['summary']}" for r in rows]
    batch_size, total = 8, 0

    for i in range(0, len(texts), batch_size):
        results = analyze_batch(texts[i:i + batch_size])
        for row, analysis in zip(rows[i:i + batch_size], results):
            update_sentiment(row["id"], analysis, row["category"])
            total += 1
            if verbose:
                rec = analysis["recommendation"]
                print(f"    [{row['category']}] {rec['label']} "
                      f"({analysis['score']:+.2f}) - {row['title'][:40]}")

    if verbose:
        print(f"  ✅ {total}건 감정분석 완료")
    return total


if __name__ == "__main__":
    print("🧠 FinBERT 뉴스 감정분석 시작...")
    collect_and_save()
