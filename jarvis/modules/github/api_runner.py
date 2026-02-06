#!/usr/bin/env python3
"""
GitHub CLI 실행기
"""

from __future__ import annotations

import subprocess
import json
from typing import Optional


class GitHubError(Exception):
    """GitHub API 에러"""
    pass


class GitHubCLI:
    """GitHub CLI 실행 헬퍼"""

    def __init__(self, repo: Optional[str] = None) -> None:
        """
        Args:
            repo: 레포지토리 (owner/repo 형식, None이면 현재 디렉토리)
        """
        self.repo = repo

    def run(self, args: list[str]) -> dict | list | None:
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
