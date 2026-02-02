#!/usr/bin/env python3
"""
GitHub API 클라이언트
"""

from __future__ import annotations

import subprocess
import json
from datetime import datetime
from typing import Optional

from .types import (
    PullRequest,
    Issue,
    User,
    Label,
    Review,
    PRState,
    ReviewState,
)


class GitHubClient:
    """GitHub API 클라이언트 (gh CLI 사용)"""

    def __init__(self, repo: Optional[str] = None) -> None:
        """
        Args:
            repo: 레포지토리 (owner/repo 형식, None이면 현재 디렉토리)
        """
        self.repo = repo

    def _run_gh(self, args: list[str]) -> dict | list | None:
        """gh CLI 실행"""
        cmd = ["gh"] + args
        if self.repo:
            cmd.extend(["--repo", self.repo])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout) if result.stdout.strip() else None
        except subprocess.CalledProcessError as e:
            raise GitHubError(f"gh command failed: {e.stderr}") from e
        except json.JSONDecodeError:
            return None

    def get_pull_requests(
        self,
        state: str = "open",
        limit: int = 30,
    ) -> list[PullRequest]:
        """PR 목록 조회"""
        data = self._run_gh([
            "pr", "list",
            "--state", state,
            "--limit", str(limit),
            "--json", "number,title,state,author,createdAt,updatedAt,url,body,labels,isDraft,additions,deletions,changedFiles",
        ])

        if not data or not isinstance(data, list):
            return []

        return [self._parse_pr(pr) for pr in data]

    def get_pull_request(self, number: int) -> PullRequest:
        """단일 PR 조회"""
        data = self._run_gh([
            "pr", "view", str(number),
            "--json", "number,title,state,author,createdAt,updatedAt,url,body,labels,isDraft,additions,deletions,changedFiles,reviews",
        ])

        if not data or not isinstance(data, dict):
            raise GitHubError(f"PR #{number} not found")

        return self._parse_pr(data)

    def get_issues(
        self,
        state: str = "open",
        limit: int = 30,
    ) -> list[Issue]:
        """Issue 목록 조회"""
        data = self._run_gh([
            "issue", "list",
            "--state", state,
            "--limit", str(limit),
            "--json", "number,title,state,author,createdAt,updatedAt,url,body,labels,assignees",
        ])

        if not data or not isinstance(data, list):
            return []

        return [self._parse_issue(issue) for issue in data]

    def get_my_assigned_issues(self) -> list[Issue]:
        """내게 할당된 Issue 조회"""
        data = self._run_gh([
            "issue", "list",
            "--assignee", "@me",
            "--state", "open",
            "--json", "number,title,state,author,createdAt,updatedAt,url,body,labels,assignees",
        ])

        if not data or not isinstance(data, list):
            return []

        return [self._parse_issue(issue) for issue in data]

    def get_review_requests(self) -> list[PullRequest]:
        """리뷰 요청된 PR 조회"""
        data = self._run_gh([
            "pr", "list",
            "--search", "review-requested:@me",
            "--json", "number,title,state,author,createdAt,updatedAt,url,body,labels,isDraft",
        ])

        if not data or not isinstance(data, list):
            return []

        return [self._parse_pr(pr) for pr in data]

    def _parse_pr(self, data: dict) -> PullRequest:
        """PR 데이터 파싱"""
        state_map = {"OPEN": PRState.OPEN, "CLOSED": PRState.CLOSED, "MERGED": PRState.MERGED}

        reviews = []
        for r in data.get("reviews", []):
            review_state_map = {
                "PENDING": ReviewState.PENDING,
                "APPROVED": ReviewState.APPROVED,
                "CHANGES_REQUESTED": ReviewState.CHANGES_REQUESTED,
                "COMMENTED": ReviewState.COMMENTED,
            }
            reviews.append(Review(
                id=r.get("id", 0),
                user=User(login=r.get("author", {}).get("login", "")),
                state=review_state_map.get(r.get("state", ""), ReviewState.PENDING),
                body=r.get("body", ""),
            ))

        return PullRequest(
            number=data["number"],
            title=data["title"],
            state=state_map.get(data.get("state", "OPEN"), PRState.OPEN),
            author=User(login=data.get("author", {}).get("login", "")),
            created_at=datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updatedAt"].replace("Z", "+00:00")),
            url=data["url"],
            body=data.get("body", ""),
            labels=[Label(name=lbl["name"], color=lbl.get("color", "")) for lbl in data.get("labels", [])],
            reviews=reviews,
            draft=data.get("isDraft", False),
            additions=data.get("additions", 0),
            deletions=data.get("deletions", 0),
            changed_files=data.get("changedFiles", 0),
        )

    def _parse_issue(self, data: dict) -> Issue:
        """Issue 데이터 파싱"""
        return Issue(
            number=data["number"],
            title=data["title"],
            state=data.get("state", "open").lower(),
            author=User(login=data.get("author", {}).get("login", "")),
            created_at=datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updatedAt"].replace("Z", "+00:00")),
            url=data["url"],
            body=data.get("body", ""),
            labels=[Label(name=lbl["name"], color=lbl.get("color", "")) for lbl in data.get("labels", [])],
            assignees=[User(login=usr.get("login", "")) for usr in data.get("assignees", [])],
        )


class GitHubError(Exception):
    """GitHub API 에러"""
    pass
