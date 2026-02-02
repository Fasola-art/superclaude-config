#!/usr/bin/env python3
"""
GitHub 모듈 타입 정의
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional


class PRState(Enum):
    """PR 상태"""

    OPEN = auto()
    CLOSED = auto()
    MERGED = auto()


class ReviewState(Enum):
    """리뷰 상태"""

    PENDING = auto()
    APPROVED = auto()
    CHANGES_REQUESTED = auto()
    COMMENTED = auto()


@dataclass
class User:
    """GitHub 사용자"""

    login: str
    avatar_url: str = ""


@dataclass
class Label:
    """GitHub 라벨"""

    name: str
    color: str = ""


@dataclass
class Review:
    """PR 리뷰"""

    id: int
    user: User
    state: ReviewState
    body: str = ""
    submitted_at: Optional[datetime] = None


@dataclass
class PullRequest:
    """Pull Request"""

    number: int
    title: str
    state: PRState
    author: User
    created_at: datetime
    updated_at: datetime
    url: str
    body: str = ""
    labels: list[Label] = field(default_factory=list)
    reviews: list[Review] = field(default_factory=list)
    draft: bool = False
    mergeable: bool = True
    additions: int = 0
    deletions: int = 0
    changed_files: int = 0


@dataclass
class Issue:
    """GitHub Issue"""

    number: int
    title: str
    state: str  # open, closed
    author: User
    created_at: datetime
    updated_at: datetime
    url: str
    body: str = ""
    labels: list[Label] = field(default_factory=list)
    assignees: list[User] = field(default_factory=list)


@dataclass
class Notification:
    """GitHub 알림"""

    type: str  # pr_opened, pr_review_requested, pr_merged, issue_assigned
    title: str
    url: str
    repo: str
    timestamp: datetime
    actor: Optional[User] = None
    priority: str = "normal"  # low, normal, high, urgent
