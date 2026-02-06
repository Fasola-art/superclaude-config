#!/usr/bin/env python3
"""Remember/Recall 데모 CLI"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory.db import init_database
from actions import (
    save_context,
    save_quick_context,
    get_last_context,
    get_contexts_by_tag,
    get_recent_contexts,
    search_contexts
)


def print_context(ctx: dict, index: int = None):
    """컨텍스트 정보 출력"""
    prefix = f"[{index}] " if index is not None else ""
    print(f"\n{prefix}{'='*60}")
    print(f"ID: {ctx['id']}")
    print(f"Project: {ctx['project_path']}")
    print(f"Created: {ctx['created_at']}")
    print(f"Last File: {ctx['last_file']}")
    print(f"Last Action: {ctx['last_action']}")
    print(f"Summary:\n  {ctx['conversation_summary']}")
    print("="*60)


def main():
    """메인 데모"""
    init_database()

    if len(sys.argv) < 2:
        print("사용법:")
        print("  python demo_remember_recall.py save <project_path> <summary> [tags...]")
        print("  python demo_remember_recall.py quick <summary> [tags...]")
        print("  python demo_remember_recall.py last [project_path]")
        print("  python demo_remember_recall.py tag <tag>")
        print("  python demo_remember_recall.py recent [limit]")
        print("  python demo_remember_recall.py search <keyword>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "save":
        project = sys.argv[2]
        summary = sys.argv[3]
        tags = sys.argv[4:] if len(sys.argv) > 4 else None
        ctx_id = save_context(project, summary, tags)
        print(f"✅ 컨텍스트 저장 완료 (ID: {ctx_id})")

    elif cmd == "quick":
        summary = sys.argv[2]
        tags = sys.argv[3:] if len(sys.argv) > 3 else None
        ctx_id = save_quick_context(summary, tags)
        print(f"✅ 빠른 저장 완료 (ID: {ctx_id})")

    elif cmd == "last":
        project = sys.argv[2] if len(sys.argv) > 2 else None
        ctx = get_last_context(project)
        if ctx:
            print_context(ctx)
        else:
            print("❌ 저장된 컨텍스트가 없습니다.")

    elif cmd == "tag":
        tag = sys.argv[2]
        results = get_contexts_by_tag(tag)
        print(f"\n📌 태그 '{tag}' 검색 결과: {len(results)}개")
        for i, ctx in enumerate(results, 1):
            print_context(ctx, i)

    elif cmd == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        results = get_recent_contexts(limit)
        print(f"\n📝 최근 {limit}개 컨텍스트:")
        for i, ctx in enumerate(results, 1):
            print_context(ctx, i)

    elif cmd == "search":
        keyword = sys.argv[2]
        results = search_contexts(keyword)
        print(f"\n🔍 키워드 '{keyword}' 검색 결과: {len(results)}개")
        for i, ctx in enumerate(results, 1):
            print_context(ctx, i)

    else:
        print(f"❌ 알 수 없는 명령: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
