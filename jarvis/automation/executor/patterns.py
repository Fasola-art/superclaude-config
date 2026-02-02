#!/usr/bin/env python3
"""
의도 분석 패턴 정의
"""

from __future__ import annotations

# 의도별 정규식 패턴
INTENT_PATTERNS: dict[str, list[str]] = {
    "add_task": [
        r"할\s*일.*추가",
        r"작업.*추가",
        r"todo.*add",
        r"task.*create",
    ],
    "list_tasks": [
        r"할\s*일.*보여",
        r"작업.*목록",
        r"todo.*list",
        r"tasks?.*show",
    ],
    "complete_task": [
        r"완료.*표시",
        r"끝났",
        r"done",
        r"complete",
    ],
    "add_event": [
        r"일정.*추가",
        r"약속.*잡",
        r"미팅.*예약",
        r"event.*add",
    ],
    "list_events": [
        r"일정.*보여",
        r"오늘.*일정",
        r"스케줄",
        r"calendar",
    ],
    "remember": [
        r"기억해",
        r"저장해",
        r"컨텍스트.*저장",
        r"remember",
    ],
    "recall": [
        r"어디까지",
        r"마지막.*작업",
        r"이어서",
        r"recall",
        r"continue",
    ],
    "booking": [
        r"예약",
        r"book",
        r"reservation",
    ],
    "planning": [
        r"계획",
        r"plan",
        r"일정.*짜",
    ],
}

# 사용 가능한 명령어 목록
AVAILABLE_COMMANDS = [
    "/j briefing - 상세 브리핑",
    "/j remember - 작업 연속성 저장",
    "/j do <작업> - 자율 작업 수행",
    "/j book <예약> - 예약하기",
    "/j plan <이벤트> - 계획 수립",
]
