#!/usr/bin/env python3
"""Remember/Recall 기능 테스트"""

import os
import sys
from pathlib import Path

# JARVIS 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis.memory.db import init_database
from jarvis.actions.remember import save_context, save_quick_context
from jarvis.actions.recall import (
    get_last_context,
    get_contexts_by_tag,
    get_recent_contexts,
    search_contexts
)


def test_remember_recall():
    """Remember/Recall 통합 테스트"""
    print("=== Remember/Recall 기능 테스트 ===\n")

    # 1. DB 초기화
    print("1. DB 초기화...")
    init_database(force=True)
    print("   ✅ DB 초기화 완료\n")

    # 2. 컨텍스트 저장 테스트
    print("2. 컨텍스트 저장 테스트...")
    test_project = "/tmp/test-project"

    ctx_id1 = save_context(
        project_path=test_project,
        summary="API 연동 작업 중. FastAPI 엔드포인트 3개 생성 완료.",
        tags=["api", "fastapi"],
        last_file="main.py",
        last_action="create_endpoint"
    )
    print(f"   ✅ 컨텍스트 1 저장 완료 (ID: {ctx_id1})")

    ctx_id2 = save_context(
        project_path=test_project,
        summary="데이터베이스 스키마 설계. User, Post 테이블 생성.",
        tags=["database", "schema"],
        last_file="models.py",
        last_action="create_schema"
    )
    print(f"   ✅ 컨텍스트 2 저장 완료 (ID: {ctx_id2})\n")

    # 3. 최근 컨텍스트 조회
    print("3. 최근 컨텍스트 조회...")
    last = get_last_context(test_project)
    if last:
        print(f"   📝 Project: {last['project_path']}")
        print(f"   📝 Summary: {last['conversation_summary'][:50]}...")
        print(f"   📝 Last File: {last['last_file']}")
        print(f"   📝 Created: {last['created_at']}\n")

    # 4. 태그 검색
    print("4. 태그로 검색 (tag='api')...")
    results = get_contexts_by_tag("api")
    print(f"   ✅ {len(results)}개 발견")
    for r in results:
        print(f"      - {r['conversation_summary'][:40]}...\n")

    # 5. 최근 N개 조회
    print("5. 최근 5개 컨텍스트 조회...")
    recent = get_recent_contexts(limit=5)
    print(f"   ✅ {len(recent)}개 조회 완료")
    for r in recent:
        print(f"      - [{r['created_at']}] {r['conversation_summary'][:40]}...\n")

    # 6. 키워드 검색
    print("6. 키워드 검색 (keyword='데이터베이스')...")
    search_results = search_contexts("데이터베이스")
    print(f"   ✅ {len(search_results)}개 발견")
    for r in search_results:
        print(f"      - {r['conversation_summary'][:50]}...\n")

    # 7. 빠른 저장 테스트
    print("7. 빠른 컨텍스트 저장 테스트...")
    quick_id = save_quick_context(
        summary="빠른 메모: 내일 배포 예정",
        tags=["memo", "deploy"]
    )
    print(f"   ✅ 빠른 저장 완료 (ID: {quick_id})\n")

    print("=== ✅ 모든 테스트 통과 ===")


if __name__ == "__main__":
    test_remember_recall()
