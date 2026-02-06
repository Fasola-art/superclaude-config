#!/usr/bin/env python3
"""GitHub API 쿼리 실행"""

from __future__ import annotations

from typing import Optional

from .api_runner import GitHubCLI
from .parsers import parse_pr, parse_issue
from .types import PullRequest, Issue


def fetch_prs(
    cli: GitHubCLI, state: str = "open", limit: int = 30
) -> list[PullRequest]:
    """PR 목록 조회"""
    data = cli.run(
        [
            "pr",
            "list",
            "--state",
            state,
            "--limit",
            str(limit),
            "--json",
            "number,title,state,author,createdAt,updatedAt,url,body,labels,isDraft,additions,deletions,changedFiles",
        ]
    )
    return [parse_pr(pr) for pr in data] if isinstance(data, list) else []


def fetch_pr(cli: GitHubCLI, number: int) -> Optional[PullRequest]:
    """단일 PR 조회"""
    data = cli.run(
        [
            "pr",
            "view",
            str(number),
            "--json",
            "number,title,state,author,createdAt,updatedAt,url,body,labels,isDraft,additions,deletions,changedFiles,reviews",
        ]
    )
    return parse_pr(data) if isinstance(data, dict) else None


def fetch_issues(cli: GitHubCLI, state: str = "open", limit: int = 30) -> list[Issue]:
    """Issue 목록 조회"""
    data = cli.run(
        [
            "issue",
            "list",
            "--state",
            state,
            "--limit",
            str(limit),
            "--json",
            "number,title,state,author,createdAt,updatedAt,url,body,labels,assignees",
        ]
    )
    return [parse_issue(issue) for issue in data] if isinstance(data, list) else []


def fetch_assigned_issues(cli: GitHubCLI) -> list[Issue]:
    """내 할당 Issue 조회"""
    data = cli.run(
        [
            "issue",
            "list",
            "--assignee",
            "@me",
            "--state",
            "open",
            "--json",
            "number,title,state,author,createdAt,updatedAt,url,body,labels,assignees",
        ]
    )
    return [parse_issue(issue) for issue in data] if isinstance(data, list) else []


def fetch_review_requests(cli: GitHubCLI) -> list[PullRequest]:
    """리뷰 요청 PR 조회"""
    data = cli.run(
        [
            "pr",
            "list",
            "--search",
            "review-requested:@me",
            "--json",
            "number,title,state,author,createdAt,updatedAt,url,body,labels,isDraft",
        ]
    )
    return [parse_pr(pr) for pr in data] if isinstance(data, list) else []


def fetch_my_prs(cli: GitHubCLI, state: str = "open") -> list[PullRequest]:
    """내 PR 조회"""
    data = cli.run(
        [
            "pr",
            "list",
            "--author",
            "@me",
            "--state",
            state,
            "--json",
            "number,title,state,author,createdAt,updatedAt,url,body,labels,isDraft",
        ]
    )
    return [parse_pr(pr) for pr in data] if isinstance(data, list) else []
