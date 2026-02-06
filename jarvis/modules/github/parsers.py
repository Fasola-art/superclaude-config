#!/usr/bin/env python3
"""GitHub API 응답 파서"""

from __future__ import annotations

from datetime import datetime

from .types import (
    PullRequest,
    Issue,
    User,
    Label,
    Review,
    PRState,
    ReviewState,
)


def parse_pr(data: dict) -> PullRequest:
    """PR 데이터 파싱"""
    state_map = {
        "OPEN": PRState.OPEN,
        "CLOSED": PRState.CLOSED,
        "MERGED": PRState.MERGED,
    }

    reviews = []
    for r in data.get("reviews", []):
        review_state_map = {
            "PENDING": ReviewState.PENDING,
            "APPROVED": ReviewState.APPROVED,
            "CHANGES_REQUESTED": ReviewState.CHANGES_REQUESTED,
            "COMMENTED": ReviewState.COMMENTED,
        }
        reviews.append(
            Review(
                id=r.get("id", 0),
                user=User(login=r.get("author", {}).get("login", "")),
                state=review_state_map.get(r.get("state", ""), ReviewState.PENDING),
                body=r.get("body", ""),
            )
        )

    return PullRequest(
        number=data["number"],
        title=data["title"],
        state=state_map.get(data.get("state", "OPEN"), PRState.OPEN),
        author=User(login=data.get("author", {}).get("login", "")),
        created_at=datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00")),
        updated_at=datetime.fromisoformat(data["updatedAt"].replace("Z", "+00:00")),
        url=data["url"],
        body=data.get("body", ""),
        labels=[
            Label(name=lbl["name"], color=lbl.get("color", ""))
            for lbl in data.get("labels", [])
        ],
        reviews=reviews,
        draft=data.get("isDraft", False),
        additions=data.get("additions", 0),
        deletions=data.get("deletions", 0),
        changed_files=data.get("changedFiles", 0),
    )


def parse_issue(data: dict) -> Issue:
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
        labels=[
            Label(name=lbl["name"], color=lbl.get("color", ""))
            for lbl in data.get("labels", [])
        ],
        assignees=[
            User(login=usr.get("login", "")) for usr in data.get("assignees", [])
        ],
    )
