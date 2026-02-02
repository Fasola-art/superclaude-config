#!/usr/bin/env python3
"""
공통 파싱 유틸리티
"""

from __future__ import annotations

import re
from typing import Any


def parse_title(command: str, keywords: list[str] | None = None) -> str | None:
    """
    명령어에서 제목 추출

    Args:
        command: 명령어 문자열
        keywords: 제거할 키워드 목록

    Returns:
        추출된 제목 또는 None
    """
    # 따옴표 내 텍스트 우선 추출
    title_match = re.search(r'["\'](.+?)["\']', command)
    if title_match:
        return title_match.group(1)

    # 키워드 제거 후 반환
    if keywords is None:
        keywords = []
    title = command
    for keyword in keywords:
        title = re.sub(keyword, "", title, flags=re.IGNORECASE)
    title = title.strip()

    return title if title else None


def extract_id(command: str) -> int | None:
    """
    명령어에서 숫자(ID) 추출

    Args:
        command: 명령어 문자열

    Returns:
        추출된 ID 또는 None
    """
    id_match = re.search(r"(\d+)", command)
    return int(id_match.group(1)) if id_match else None


def build_response(
    success: bool,
    message: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    응답 객체 생성

    Args:
        success: 성공 여부
        message: 메시지
        **kwargs: 추가 데이터

    Returns:
        응답 딕셔너리
    """
    result: dict[str, Any] = {"success": success, "message": message}
    result.update(kwargs)
    return result
