"""
Natural Language Understanding
"""
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from .nlu_patterns import (
    INTENT_PATTERNS, PRIORITY_PATTERNS, PLACE_CATEGORIES,
    REGION_PATTERN, DATE_KEYWORDS,
)


class NLUParser:
    """Natural language command parser"""

    INTENT_PATTERNS = INTENT_PATTERNS
    PRIORITY_PATTERNS = PRIORITY_PATTERNS

    def parse(self, text: str) -> Dict[str, Any]:
        """Parse natural language command"""
        result = {
            "intent": None, "entities": {},
            "confidence": 0.0, "raw_text": text,
        }
        intent = self._detect_intent(text)
        if intent:
            result["intent"] = intent
            result["confidence"] = 0.8
        result["entities"] = self._extract_entities(text, intent)
        return result

    def _detect_intent(self, text: str) -> Optional[str]:
        """Detect intent from text"""
        text_lower = text.lower()
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        return None

    def _extract_entities(self, text: str, intent: str) -> Dict[str, Any]:
        """Extract entities from text"""
        entities = {}

        priority = self._extract_priority(text)
        if priority:
            entities["priority"] = priority

        date_time = self._extract_datetime(text)
        if date_time:
            entities.update(date_time)

        # 장소 카테고리 추출
        for cat, pats in PLACE_CATEGORIES.items():
            if any(re.search(p, text) for p in pats):
                entities["place_category"] = cat
                break

        # 지역 추출
        loc_match = re.search(REGION_PATTERN, text)
        if loc_match:
            entities["region"] = loc_match.group(0).strip()

        title = self._extract_title(text, intent)
        if title:
            entities["title"] = title

        return entities

    def _extract_priority(self, text: str) -> Optional[str]:
        """Extract priority level"""
        text_lower = text.lower()
        for priority, patterns in self.PRIORITY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return priority
        return "medium"

    def _extract_datetime(self, text: str) -> Dict[str, str]:
        """Extract date/time information"""
        result = {}
        if re.search(r"오늘|today", text, re.IGNORECASE):
            result["date"] = datetime.now().strftime("%Y-%m-%d")
        elif re.search(r"내일|tomorrow", text, re.IGNORECASE):
            result["date"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif re.search(r"주말|이번\s*주\s*토|weekend", text, re.IGNORECASE):
            today = datetime.now()
            days_until_sat = (5 - today.weekday()) % 7
            if days_until_sat == 0 and today.weekday() != 5:
                days_until_sat = 7
            result["date"] = (today + timedelta(days=days_until_sat)).strftime("%Y-%m-%d")

        time_match = re.search(r"(\d{1,2}):(\d{2})", text)
        if time_match:
            result["time"] = f"{time_match.group(1)}:{time_match.group(2)}"
        return result

    def _extract_title(self, text: str, intent: str) -> Optional[str]:
        """Extract main content/title"""
        cleaned = text
        if intent in self.INTENT_PATTERNS:
            for pattern in self.INTENT_PATTERNS[intent]:
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        for patterns in self.PRIORITY_PATTERNS.values():
            for pattern in patterns:
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        cleaned = re.sub(DATE_KEYWORDS, "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\d{1,2}:\d{2}", "", cleaned)
        cleaned = cleaned.strip()
        return cleaned if cleaned else None
