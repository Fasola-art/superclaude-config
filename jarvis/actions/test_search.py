#!/usr/bin/env python3
"""search.py 테스트"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from actions.search import search_local, search_memory, search_all


def test_search():
    """검색 시스템 테스트"""
    print("=== Search 테스트 시작 ===\n")

    # 1. 로컬 파일 검색
    print("✅ 로컬 파일 검색 (jarvis):")
    files = search_local("jarvis", str(Path.home() / ".claude"))
    for f in files[:5]:
        print(f"  - {f}")

    # 2. 메모리 검색
    print("\n✅ 메모리 검색 (trading):")
    memories = search_memory("trading")
    for m in memories[:3]:
        summary = m.get('conversation_summary', '')[:50]
        print(f"  - [{m['project_path']}] {summary}...")

    # 3. 통합 검색
    print("\n✅ 통합 검색 (jarvis):")
    results = search_all("jarvis", str(Path.home() / ".claude"))
    print(f"  메모리: {len(results['memory'])}건")
    print(f"  로컬: {len(results['local'])}건")

    print("\n=== Search 테스트 완료 ===")


if __name__ == "__main__":
    test_search()
