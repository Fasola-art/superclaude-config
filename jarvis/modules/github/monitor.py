#!/usr/bin/env python3
"""
GitHub 모니터링 모듈
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from .types import PullRequest, Issue, Notification, ReviewState
from .client import GitHubClient


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

        # 각 레포 확인
        for repo in self.repos:
            client = GitHubClient(repo)

            # 리뷰 요청된 PR
            review_requests = client.get_review_requests()
            for pr in review_requests:
                key = f"{repo}:{pr.number}"
                if key not in self._known_prs:
                    notifications.append(Notification(
                        type="pr_review_requested",
                        title=f"[{repo}] 리뷰 요청: #{pr.number} {pr.title}",
                        url=pr.url,
                        repo=repo,
                        timestamp=pr.updated_at,
                        actor=pr.author,
                        priority="high",
                    ))
                    self._known_prs.add(key)

            # 내게 할당된 Issue
            my_issues = client.get_my_assigned_issues()
            for issue in my_issues:
                key = f"{repo}:{issue.number}"
                if key not in self._known_issues:
                    notifications.append(Notification(
                        type="issue_assigned",
                        title=f"[{repo}] 이슈 할당: #{issue.number} {issue.title}",
                        url=issue.url,
                        repo=repo,
                        timestamp=issue.updated_at,
                        priority="normal",
                    ))
                    self._known_issues.add(key)

        self._last_check = datetime.now()
        return notifications

    def get_pr_summary(self, repo: Optional[str] = None) -> dict:
        """PR 요약"""
        client = GitHubClient(repo) if repo else self.client
        prs = client.get_pull_requests(state="open")

        # 리뷰 대기 중인 PR
        awaiting_review = [pr for pr in prs if not pr.draft and not pr.reviews]

        # 변경 요청된 PR
        changes_requested = [
            pr for pr in prs
            if any(r.state == ReviewState.CHANGES_REQUESTED for r in pr.reviews)
        ]

        # 승인된 PR
        approved = [
            pr for pr in prs
            if any(r.state == ReviewState.APPROVED for r in pr.reviews)
            and all(r.state != ReviewState.CHANGES_REQUESTED for r in pr.reviews)
        ]

        return {
            "total_open": len(prs),
            "awaiting_review": len(awaiting_review),
            "changes_requested": len(changes_requested),
            "approved": len(approved),
            "draft": len([pr for pr in prs if pr.draft]),
            "prs": prs,
        }

    def get_stale_prs(
        self,
        days: int = 7,
        repo: Optional[str] = None,
    ) -> list[PullRequest]:
        """오래된 PR 조회"""
        client = GitHubClient(repo) if repo else self.client
        prs = client.get_pull_requests(state="open")

        threshold = datetime.now() - timedelta(days=days)
        return [
            pr for pr in prs
            if pr.updated_at.replace(tzinfo=None) < threshold
        ]

    def get_my_action_items(self) -> dict[str, list[PullRequest | Issue]]:
        """내 액션 아이템"""
        items: dict[str, list[PullRequest | Issue]] = {
            "review_requests": [],
            "assigned_issues": [],
            "my_open_prs": [],
        }

        for repo in self.repos:
            client = GitHubClient(repo)

            # 리뷰 요청
            items["review_requests"].extend(client.get_review_requests())

            # 할당된 이슈
            items["assigned_issues"].extend(client.get_my_assigned_issues())

        return items
