#!/usr/bin/env python3
"""GitHub 모니터링 모듈"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from .types import PullRequest, Issue, Notification
from .client import GitHubClient
from .monitor_utils import (
    create_pr_review_notification,
    create_issue_assigned_notification,
    filter_stale_prs,
    categorize_prs_by_review_state,
    collect_action_items,
)


class GitHubMonitor:
    """GitHub PR/Issue 모니터링"""

    def __init__(
        self,
        client: Optional[GitHubClient] = None,
        repos: Optional[list[str]] = None,
    ) -> None:
        """
        Args:
            client: GitHubClient 인스턴스
            repos: 모니터링할 레포지토리 목록
        """
        self.client = client or GitHubClient()
        self.repos = repos or []
        self._last_check: datetime = datetime.now()
        self._known_prs: set[str] = set()  # "repo:number" 형식
        self._known_issues: set[str] = set()

    def check_for_updates(self) -> list[Notification]:
        """업데이트 확인"""
        notifications: list[Notification] = []

        for repo in self.repos:
            client = GitHubClient(repo)

            # 리뷰 요청된 PR
            for pr in client.get_review_requests():
                key = f"{repo}:{pr.number}"
                if key not in self._known_prs:
                    notifications.append(
                        create_pr_review_notification(repo, pr)
                    )
                    self._known_prs.add(key)

            # 내게 할당된 Issue
            for issue in client.get_my_assigned_issues():
                key = f"{repo}:{issue.number}"
                if key not in self._known_issues:
                    notifications.append(
                        create_issue_assigned_notification(repo, issue)
                    )
                    self._known_issues.add(key)

        self._last_check = datetime.now()
        return notifications

    def get_pr_summary(self, repo: Optional[str] = None) -> dict:
        """PR 요약"""
        client = GitHubClient(repo) if repo else self.client
        prs = client.get_pull_requests(state="open")
        return categorize_prs_by_review_state(prs)

    def get_stale_prs(
        self, days: int = 7, repo: Optional[str] = None
    ) -> list[PullRequest]:
        """오래된 PR 조회"""
        client = GitHubClient(repo) if repo else self.client
        prs = client.get_pull_requests(state="open")
        return filter_stale_prs(prs, days)

    def get_my_action_items(self) -> dict[str, list[PullRequest | Issue]]:
        """내 액션 아이템"""
        return collect_action_items(self.repos)
