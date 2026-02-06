"""
Client Tracker Types
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Client:
    """클라이언트 정보"""

    id: int
    name: str
    project: str
    created_at: datetime
    active: bool = True


@dataclass
class WorkLog:
    """작업 로그"""

    id: int
    client_id: int
    date: datetime
    hours: float
    description: str
    hourly_rate: float = 0.0
