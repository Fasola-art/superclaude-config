#!/usr/bin/env python3
"""
NLU 모듈 테스트 (TDD)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from nlu import NLUParser, Intent


class TestIntent:
    """의도 분류 테스트"""

    def test_task_intent(self) -> None:
        """작업 관련 의도"""
        parser = NLUParser()

        result = parser.parse("할 일 추가해줘")
        assert result.intent == Intent.ADD_TASK

        result = parser.parse("작업 목록 보여줘")
        assert result.intent == Intent.LIST_TASKS

        result = parser.parse("1번 작업 완료")
        assert result.intent == Intent.COMPLETE_TASK

    def test_event_intent(self) -> None:
        """일정 관련 의도"""
        parser = NLUParser()

        result = parser.parse("내일 3시 미팅 일정 추가")
        assert result.intent == Intent.ADD_EVENT

        result = parser.parse("오늘 일정 보여줘")
        assert result.intent == Intent.LIST_EVENTS

    def test_context_intent(self) -> None:
        """컨텍스트 관련 의도"""
        parser = NLUParser()

        result = parser.parse("이거 기억해줘")
        assert result.intent == Intent.REMEMBER

        result = parser.parse("어디까지 했더라")
        assert result.intent == Intent.RECALL

    def test_booking_intent(self) -> None:
        """예약 관련 의도"""
        parser = NLUParser()

        result = parser.parse("레스토랑 예약해줘")
        assert result.intent == Intent.BOOKING

        result = parser.parse("영화 예매")
        assert result.intent == Intent.BOOKING

    def test_planning_intent(self) -> None:
        """계획 관련 의도"""
        parser = NLUParser()

        result = parser.parse("데이트 계획 짜줘")
        assert result.intent == Intent.PLANNING

    def test_unknown_intent(self) -> None:
        """알 수 없는 의도"""
        parser = NLUParser()

        result = parser.parse("안녕하세요")
        assert result.intent == Intent.UNKNOWN


class TestEntity:
    """엔티티 추출 테스트"""

    def test_extract_date(self) -> None:
        """날짜 추출"""
        parser = NLUParser()

        result = parser.parse("2월 10일 예약")
        assert any(e.type == "date" and e.value == "2026-02-10" for e in result.entities)

        result = parser.parse("내일 미팅")
        assert any(e.type == "date" for e in result.entities)

        result = parser.parse("다음주 월요일")
        assert any(e.type == "date" for e in result.entities)

    def test_extract_time(self) -> None:
        """시간 추출"""
        parser = NLUParser()

        result = parser.parse("오후 3시 미팅")
        assert any(e.type == "time" and e.value == "15:00" for e in result.entities)

        result = parser.parse("7시 저녁")
        assert any(e.type == "time" for e in result.entities)

    def test_extract_number(self) -> None:
        """숫자 추출"""
        parser = NLUParser()

        result = parser.parse("4명 예약")
        assert any(e.type == "number" and e.value == 4 for e in result.entities)

        result = parser.parse("3번 작업 완료")
        assert any(e.type == "task_id" and e.value == 3 for e in result.entities)

    def test_extract_quoted_text(self) -> None:
        """따옴표 텍스트 추출"""
        parser = NLUParser()

        result = parser.parse('"API 리팩토링" 작업 추가')
        assert any(e.type == "title" and e.value == "API 리팩토링" for e in result.entities)


class TestParseResult:
    """파싱 결과 테스트"""

    def test_confidence(self) -> None:
        """신뢰도"""
        parser = NLUParser()

        # 명확한 의도
        result = parser.parse("할 일 목록 보여줘")
        assert result.confidence >= 0.8

        # 불명확한 의도
        result = parser.parse("뭔가 해줘")
        assert result.confidence < 0.5

    def test_get_entity(self) -> None:
        """엔티티 조회"""
        parser = NLUParser()

        result = parser.parse('"테스트" 2월 5일 3시 2명')
        assert result.get_entity("title") == "테스트"
        assert result.get_entity("date") is not None
        assert result.get_entity("time") is not None
        assert result.get_entity("number") == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
