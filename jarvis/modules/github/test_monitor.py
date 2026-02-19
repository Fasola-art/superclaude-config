#!/usr/bin/env python3
"""GitHubMonitor 테스트"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from jarvis.modules.github import GitHubClient, GitHubMonitor


def test_client_basic():
    """GitHubClient 기본 동작 테스트"""
    print("=== GitHubClient 테스트 ===")

    client = GitHubClient()

    # PR 목록
    print("\n1. PR 목록 조회:")
    try:
        prs = client.get_pull_requests(limit=3)
        print(f"  ✓ {len(prs)}개 PR 조회 성공")
        if prs:
            print(f"  - 첫 번째 PR: #{prs[0].number} {prs[0].title}")
    except Exception as e:
        print(f"  ✗ 에러: {e}")

    # Issue 목록
    print("\n2. Issue 목록 조회:")
    try:
        issues = client.get_issues(limit=3)
        print(f"  ✓ {len(issues)}개 Issue 조회 성공")
        if issues:
            print(f"  - 첫 번째 Issue: #{issues[0].number} {issues[0].title}")
    except Exception as e:
        print(f"  ✗ 에러: {e}")

    # 내 할당 Issue
    print("\n3. 내 할당 Issue 조회:")
    try:
        my_issues = client.get_my_assigned_issues()
        print(f"  ✓ {len(my_issues)}개 할당 Issue 조회 성공")
    except Exception as e:
        print(f"  ✗ 에러: {e}")

    # 리뷰 요청
    print("\n4. 리뷰 요청 PR 조회:")
    try:
        review_prs = client.get_review_requests()
        print(f"  ✓ {len(review_prs)}개 리뷰 요청 PR 조회 성공")
    except Exception as e:
        print(f"  ✗ 에러: {e}")


def test_monitor():
    """GitHubMonitor 테스트"""
    print("\n=== GitHubMonitor 테스트 ===")

    # 레포지토리 목록 (실제 접근 가능한 레포로 변경 필요)
    repos = []

    monitor = GitHubMonitor(repos=repos)

    print("\n1. PR 요약:")
    try:
        summary = monitor.get_pr_summary()
        print(f"  ✓ PR 요약 생성 성공")
        for key, value in summary.items():
            if isinstance(value, (list, str)):
                print(f"  - {key}: {len(value)}개")
            else:
                print(f"  - {key}: {value}")
    except Exception as e:
        print(f"  ✗ 에러: {e}")

    print("\n2. 오래된 PR 조회:")
    try:
        stale = monitor.get_stale_prs(days=7)
        print(f"  ✓ {len(stale)}개 오래된 PR 발견")
    except Exception as e:
        print(f"  ✗ 에러: {e}")


def test_missing_features():
    """누락 기능 확인"""
    print("\n=== 누락 기능 확인 ===")

    client = GitHubClient()

    # get_notifications 필요
    print("\n1. get_notifications() 필요 여부:")
    if not hasattr(client, 'get_notifications'):
        print("  ✗ 누락: get_notifications() 추가 필요")
    else:
        print("  ✓ 존재")

    # get_my_prs 필요
    print("\n2. get_my_prs() 필요 여부:")
    if not hasattr(client, 'get_my_prs'):
        print("  ✗ 누락: get_my_prs() 추가 필요")
    else:
        print("  ✓ 존재")

    # get_mentions 필요
    print("\n3. get_mentions() 필요 여부:")
    if not hasattr(client, 'get_mentions'):
        print("  ✗ 누락: get_mentions() 추가 필요")
    else:
        print("  ✓ 존재")


if __name__ == "__main__":
    test_client_basic()
    test_monitor()
    test_missing_features()

    print("\n=== 테스트 완료 ===")
