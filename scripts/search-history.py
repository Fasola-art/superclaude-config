#!/usr/bin/env python3
"""
Claude Code 대화 이력 검색 스크립트
Usage: python3 search-history.py <keyword> [--last N] [--context K]
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

PROJECTS_DIR = Path("/mnt/c/Users/MSI/.claude/projects")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Claude Code 대화 이력 검색")
    parser.add_argument("keyword", nargs="?", default="", help="검색 키워드")
    parser.add_argument("--last", "-n", type=int, default=20, help="최근 N개 파일 검색 (기본: 20)")
    parser.add_argument("--context", "-c", type=int, default=200, help="매칭 텍스트 표시 길이 (기본: 200)")
    parser.add_argument("--role", "-r", choices=["user", "assistant", "all"], default="all", help="역할 필터")
    return parser.parse_args()


def format_timestamp(ts: str | float | None) -> str:
    if ts is None:
        return "unknown"
    try:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        return str(ts)[:16]
    except Exception:
        return str(ts)[:16]


def search(keyword: str, last_n: int = 20, context_len: int = 200, role: str = "all") -> None:
    if not PROJECTS_DIR.exists():
        print(f"[ERROR] 프로젝트 디렉토리 없음: {PROJECTS_DIR}")
        sys.exit(1)

    files = sorted(
        PROJECTS_DIR.rglob("*.jsonl"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )[:last_n]

    if not files:
        print("[INFO] JSONL 파일 없음")
        return

    results: list[dict] = []

    for f in files:
        try:
            lines = f.read_text(errors="ignore").splitlines()
        except Exception:
            continue

        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            # 역할 필터
            entry_role = entry.get("type", entry.get("role", ""))
            if role != "all" and entry_role != role:
                continue

            # 메시지 텍스트 추출
            msg = entry.get("message", entry.get("content", entry.get("text", "")))
            if isinstance(msg, dict):
                msg = msg.get("content", str(msg))
            elif isinstance(msg, list):
                msg = " ".join(
                    item.get("text", str(item)) if isinstance(item, dict) else str(item)
                    for item in msg
                )
            text = str(msg)

            if not keyword or keyword.lower() in text.lower():
                idx = text.lower().find(keyword.lower()) if keyword else 0
                snippet = text[max(0, idx - 50):idx + context_len].strip()
                results.append({
                    "file": f.name,
                    "line": line_num,
                    "role": entry_role or "unknown",
                    "timestamp": format_timestamp(entry.get("timestamp")),
                    "snippet": snippet,
                })

    if not results:
        print(f"[INFO] '{keyword}' 검색 결과 없음 (최근 {last_n}개 파일)")
        return

    print(f"\n=== 검색 결과: '{keyword}' ({len(results)}건) ===\n")
    for r in results:
        print(f"[{r['timestamp']}] {r['file']}:{r['line']} ({r['role']})")
        print(f"  {r['snippet'][:context_len]}")
        print()


if __name__ == "__main__":
    args = parse_args()
    search(
        keyword=args.keyword,
        last_n=args.last,
        context_len=args.context,
        role=args.role,
    )
