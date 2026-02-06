#!/usr/bin/env python3
"""
에이전트 조율 모델
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowStep:
    """워크플로우 단계"""

    name: str
    agent_type: str
    config: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)


@dataclass
class Workflow:
    """워크플로우 정의"""

    name: str
    steps: list[WorkflowStep]
    description: str = ""
