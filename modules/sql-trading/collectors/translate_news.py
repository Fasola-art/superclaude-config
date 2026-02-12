#!/usr/bin/env python3
"""
뉴스 한글 번역기

영어 뉴스를 한글로 번역, 원문은 metadata에 보존
"""

import json
import re
import subprocess
import sys
import time

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))

from deep_translator import GoogleTranslator
from _db_utils import DB, PSQL, escape_sql, run_sql

_tr = GoogleTranslator(source="en", target="ko")
_KR = re.compile(r"[가-힣]")


def _translate(text: str) -> str:
    """영어 → 한국어 (한글 15%+ 포함 시 스킵)"""
    if not text or len(_KR.findall(text)) / max(len(text), 1) > 0.15:
        return text
    try:
        return _tr.translate(text[:4500]) or text
    except Exception:
        return text


def fetch_untranslated(limit: int = 30) -> list[dict]:
    """영어 뉴스 조회"""
    r = subprocess.run(
        [PSQL, "-U", "reim", "-d", DB, "-t", "-A", "-F", "|||", "-c",
         f"SELECT id, title, COALESCE(summary,''), "
         f"COALESCE(metadata::text,'{{}}') "
         f"FROM market_news WHERE title !~ '[가-힣]' "
         f"ORDER BY timestamp DESC LIMIT {limit};"],
        capture_output=True, text=True, timeout=10,
    )
    if r.returncode != 0:
        return []
    rows = []
    for line in r.stdout.strip().split("\n"):
        p = line.split("|||")
        if len(p) >= 4:
            rows.append({"id": int(p[0]), "title": p[1],
                         "summary": p[2], "meta": p[3]})
    return rows


def collect_and_save(verbose: bool = True) -> int:
    """미번역 영어 뉴스 번역"""
    rows = fetch_untranslated()
    if not rows:
        if verbose:
            print("  ℹ️ 번역 필요한 뉴스 없음")
        return 0
    if verbose:
        print(f"  🌐 {len(rows)}건 번역 시작...")

    total = 0
    for row in rows:
        title_kr = _translate(row["title"])
        summary_kr = _translate(row["summary"])

        # 원문 보존 + 번역 플래그
        try:
            meta = json.loads(row["meta"]) if row["meta"] != "{}" else {}
        except json.JSONDecodeError:
            meta = {}
        meta.update({"original_title": row["title"][:500],
                      "translated": True})
        if row["summary"]:
            meta["original_summary"] = row["summary"][:800]

        mj = escape_sql(json.dumps(meta, ensure_ascii=False))
        run_sql(
            f"UPDATE market_news SET title='{escape_sql(title_kr[:500])}', "
            f"summary='{escape_sql(summary_kr[:1000])}', "
            f"metadata='{mj}'::jsonb WHERE id={row['id']};"
        )
        total += 1
        if verbose:
            print(f"    ✅ {row['title'][:30]} → {title_kr[:30]}")
        time.sleep(0.3)

    if verbose:
        print(f"  ✅ {total}건 번역 완료")
    return total


if __name__ == "__main__":
    print("🌐 뉴스 한글 번역 시작...")
    collect_and_save()
