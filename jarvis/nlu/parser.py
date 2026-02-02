#!/usr/bin/env python3
"""
NLU 파서 메인 모듈
"""

from __future__ import annotations

from .types import Intent, ParseResult
from .intent import classify_intent
from .entities import extract_entities


class NLUParser:
    """자연어 파서"""

    def parse(self, text: str) -> ParseResult:
        """
        텍스트 파싱

        Args:
            text: 입력 텍스트

        Returns:
            ParseResult: 파싱 결과
        """
        # 의도 분류
        intent, confidence = classify_intent(text)

        # 엔티티 추출
        entities = extract_entities(text)

        return ParseResult(
            intent=intent,
            entities=entities,
            confidence=confidence,
            raw_text=text,
        )

    def parse_with_context(
        self,
        text: str,
        previous_intent: Intent | None = None,
    ) -> ParseResult:
        """
        컨텍스트를 고려한 파싱

        Args:
            text: 입력 텍스트
            previous_intent: 이전 대화의 의도

        Returns:
            ParseResult: 파싱 결과
        """
        result = self.parse(text)

        # 불명확한 의도인데 이전 컨텍스트가 있으면 참조
        if result.intent == Intent.UNKNOWN and previous_intent:
            # "그거", "이거" 등의 대명사 처리
            if any(kw in text for kw in ["그거", "이거", "그것", "이것"]):
                result = ParseResult(
                    intent=previous_intent,
                    entities=result.entities,
                    confidence=0.6,
                    raw_text=text,
                )

        return result
