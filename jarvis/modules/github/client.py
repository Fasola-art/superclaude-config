#!/usr/bin/env python3
"""GitHub API 클라이언트"""

from __future__ import annotations

from typing import Optional

from .types import PullRequest, Issue
from .api_runner import GitHubCLI, GitHubError
from .queries import (
    fetch_prs,
    fetch_pr,
    fetch_issues,
    fetch_assigned_issues,
    fetch_review_requests,
    fetch_my_prs,
)


class GitHubClient:
    """GitHub API 클라이언트 (gh CLI 사용)"""

    def __init__(self, repo: Optional[str] = None) -> None:
        """
        Args:
            repo: 레포지토리 (owner/repo 형식, None이면 현재 디렉토리)
        """
        self.cli = GitHubCLI(repo)

    def get_pull_requests(
        self, state: str = "open", limit: int = 30
    ) -> list[PullRequest]:
        """PR 목록 조회"""
        return fetch_prs(self.cli, state, limit)

    def get_pull_request(self, number: int) -> PullRequest:
        """단일 PR 조회"""
        result = fetch_pr(self.cli, number)
        if not result:
            raise GitHubError(f"PR #{number} not found")
        return result

    def get_issues(self, state: str = "open", limit: int = 30) -> list[Issue]:
        """Issue 목록 조회"""
        return fetch_issues(self.cli, state, limit)

    def get_my_assigned_issues(self) -> list[Issue]:
        """내게 할당된 Issue 조회"""
        return fetch_assigned_issues(self.cli)

    def get_review_requests(self) -> list[PullRequest]:
        """리뷰 요청된 PR 조회"""
        return fetch_review_requests(self.cli)

    def get_my_prs(self, state: str = "open") -> list[PullRequest]:
        """내가 생성한 PR 조회"""
        return fetch_my_prs(self.cli, state)

    def get_notifications(self, all_notifications: bool = False) -> list[dict]:
        """알림 조회 (gh API 사용)"""
        args = ["api", "notifications"]
        if all_notifications:
            args.append("--paginate")

        data = self.cli.run(args)
        return data if isinstance(data, list) else []

    def get_mentions(self) -> list[dict]:
        """나를 멘션한 이슈/PR 조회"""
        notifications = self.get_notifications()
        return [n for n in notifications if n.get("reason") == "mention"]
