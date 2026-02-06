#!/usr/bin/env python3
"""GitHub 모니터링 유틸리티 함수"""

from datetime import datetime, timedelta

from .types import PullRequest, Issue, Notification, ReviewState
from .client import GitHubClient


def create_pr_review_notification(repo: str, pr: PullRequest) -> Notification:
    """리뷰 요청 알림 생성"""
    return Notification(
        type="pr_review_requested",
        title=f"[{repo}] 리뷰 요청: #{pr.number} {pr.title}",
        url=pr.url,
        repo=repo,
        timestamp=pr.updated_at,
        actor=pr.author,
        priority="high",
    )


def create_issue_assigned_notification(repo: str, issue: Issue) -> Notification:
    """이슈 할당 알림 생성"""
    return Notification(
        type="issue_assigned",
        title=f"[{repo}] 이슈 할당: #{issue.number} {issue.title}",
        url=issue.url,
        repo=repo,
        timestamp=issue.updated_at,
        priority="normal",
    )


def filter_stale_prs(prs: list[PullRequest], days: int) -> list[PullRequest]:
    """오래된 PR 필터링"""
    threshold = datetime.now() - timedelta(days=days)
    return [pr for pr in prs if pr.updated_at.replace(tzinfo=None) < threshold]


def categorize_prs_by_review_state(prs: list[PullRequest]) -> dict:
    """리뷰 상태별 PR 분류"""
    awaiting_review = [pr for pr in prs if not pr.draft and not pr.reviews]

    changes_requested = [
        pr
        for pr in prs
        if any(r.state == ReviewState.CHANGES_REQUESTED for r in pr.reviews)
    ]

    approved = [
        pr
        for pr in prs
        if any(r.state == ReviewState.APPROVED for r in pr.reviews)
        and all(r.state != ReviewState.CHANGES_REQUESTED for r in pr.reviews)
    ]

    return {
        "total_open": len(prs),
        "awaiting_review": awaiting_review,
        "changes_requested": changes_requested,
        "approved": approved,
        "draft": [pr for pr in prs if pr.draft],
        "prs": prs,
    }


def collect_action_items(repos: list[str]) -> dict[str, list[PullRequest | Issue]]:
    """액션 아이템 수집"""
    items: dict[str, list[PullRequest | Issue]] = {
        "review_requests": [],
        "assigned_issues": [],
        "my_open_prs": [],
    }

    for repo in repos:
        client = GitHubClient(repo)
        items["review_requests"].extend(client.get_review_requests())
        items["assigned_issues"].extend(client.get_my_assigned_issues())
        items["my_open_prs"].extend(client.get_my_prs())

    return items
