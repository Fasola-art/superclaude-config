#!/usr/bin/env python3
"""
예약(Booking) 및 계획(Planning) 핸들러
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

_root = str(Path(__file__).parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from utils import build_response  # noqa: E402


@dataclass
class BookingRequest:
    """예약 요청 데이터"""

    venue_type: str  # restaurant, movie, hotel
    venue_name: str | None
    date: str | None
    time: str | None
    party_size: int | None


def parse_booking_request(command: str) -> BookingRequest:
    """
    예약 명령어 파싱

    Args:
        command: 명령어

    Returns:
        파싱된 예약 요청
    """
    command_lower = command.lower()

    # 예약 유형 감지
    venue_type = "unknown"
    if any(kw in command_lower for kw in ["레스토랑", "식당", "맛집", "restaurant"]):
        venue_type = "restaurant"
    elif any(kw in command_lower for kw in ["영화", "movie", "cinema"]):
        venue_type = "movie"
    elif any(kw in command_lower for kw in ["호텔", "숙소", "hotel", "숙박"]):
        venue_type = "hotel"

    # 날짜 추출
    date_match = re.search(r"(\d{1,2})월\s*(\d{1,2})일", command)
    date = None
    if date_match:
        month, day = date_match.groups()
        year = datetime.now().year
        date = f"{year}-{int(month):02d}-{int(day):02d}"

    # 시간 추출
    time_match = re.search(r"(\d{1,2})\s*시", command)
    time = None
    if time_match:
        hour = int(time_match.group(1))
        time = f"{hour:02d}:00"

    # 인원 추출
    party_match = re.search(r"(\d+)\s*명", command)
    party_size = int(party_match.group(1)) if party_match else None

    # 장소명 추출 (따옴표 내)
    venue_match = re.search(r'["\'](.+?)["\']', command)
    venue_name = venue_match.group(1) if venue_match else None

    return BookingRequest(
        venue_type=venue_type,
        venue_name=venue_name,
        date=date,
        time=time,
        party_size=party_size,
    )


def handle_booking(command: str) -> dict[str, Any]:
    """
    예약 처리

    Args:
        command: 명령어

    Returns:
        처리 결과

    Note:
        현재는 파싱만 수행, 실제 예약은 외부 API 연동 필요
    """
    request = parse_booking_request(command)

    if request.venue_type == "unknown":
        return build_response(
            success=False,
            message="예약 유형을 인식하지 못했습니다.",
            hint="레스토랑/영화/호텔 등 예약 유형을 포함해주세요.",
        )

    # 필수 정보 검증
    missing = []
    if not request.venue_name:
        missing.append("장소명")
    if not request.date:
        missing.append("날짜")
    if request.venue_type == "restaurant" and not request.party_size:
        missing.append("인원")

    if missing:
        return build_response(
            success=False,
            message=f"예약에 필요한 정보가 부족합니다: {', '.join(missing)}",
            hint='/j book "장소명" MM월 DD일 HH시 N명 형식으로 입력해주세요.',
            parsed=request.__dict__,
        )

    return build_response(
        success=True,
        message=f"{request.venue_type} 예약 요청이 준비되었습니다.",
        booking=request.__dict__,
        status="pending_api_integration",
    )


def handle_planning(command: str) -> dict[str, Any]:
    """
    계획 수립 처리

    Args:
        command: 명령어

    Returns:
        처리 결과

    Note:
        데이트 코스, 여행 일정 등 계획 수립
        추후 LLM 기반 추천 기능 연동 예정
    """
    command_lower = command.lower()

    # 계획 유형 감지
    plan_type = "general"
    if any(kw in command_lower for kw in ["데이트", "date"]):
        plan_type = "date"
    elif any(kw in command_lower for kw in ["여행", "trip", "travel"]):
        plan_type = "travel"
    elif any(kw in command_lower for kw in ["회의", "미팅", "meeting"]):
        plan_type = "meeting"

    return build_response(
        success=False,
        message="계획 수립 기능은 추후 구현 예정입니다.",
        hint="/j plan 이벤트명 형식으로 사용 예정",
        plan_type=plan_type,
        status="pending_llm_integration",
    )
