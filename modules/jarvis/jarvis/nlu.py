"""
Natural Language Understanding
"""
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class NLUParser:
    """Natural language command parser"""

    INTENT_PATTERNS = {
        "add_task": [
            r"할\s*일\s*추가",
            r"task\s*add",
            r"todo",
            r"해야\s*할",
        ],
        "add_event": [
            r"일정\s*추가",
            r"event\s*add",
            r"calendar",
            r"예약",
        ],
        "list_tasks": [
            r"할\s*일\s*목록",
            r"task\s*list",
            r"할\s*일\s*보여",
        ],
        "list_events": [
            r"일정\s*목록",
            r"event\s*list",
            r"일정\s*보여",
        ],
    }

    PRIORITY_PATTERNS = {
        "high": [r"긴급", r"중요", r"urgent", r"high"],
        "medium": [r"보통", r"medium"],
        "low": [r"나중에", r"low"],
    }

    def parse(self, text: str) -> Dict[str, Any]:
        """Parse natural language command"""
        result = {
            "intent": None,
            "entities": {},
            "confidence": 0.0,
            "raw_text": text,
        }

        # Detect intent
        intent = self._detect_intent(text)
        if intent:
            result["intent"] = intent
            result["confidence"] = 0.8

        # Extract entities
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

        # Extract priority
        priority = self._extract_priority(text)
        if priority:
            entities["priority"] = priority

        # Extract date/time
        date_time = self._extract_datetime(text)
        if date_time:
            entities.update(date_time)

        # Extract title (remaining text)
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

        # Today/Tomorrow
        if re.search(r"오늘|today", text, re.IGNORECASE):
            result["date"] = datetime.now().strftime("%Y-%m-%d")
        elif re.search(r"내일|tomorrow", text, re.IGNORECASE):
            result["date"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        # Time patterns (HH:MM)
        time_match = re.search(r"(\d{1,2}):(\d{2})", text)
        if time_match:
            result["time"] = f"{time_match.group(1)}:{time_match.group(2)}"

        return result

    def _extract_title(self, text: str, intent: str) -> Optional[str]:
        """Extract main content/title"""
        # Remove intent keywords
        cleaned = text
        if intent in self.INTENT_PATTERNS:
            for pattern in self.INTENT_PATTERNS[intent]:
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Remove priority keywords
        for patterns in self.PRIORITY_PATTERNS.values():
            for pattern in patterns:
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Remove date/time keywords
        cleaned = re.sub(r"오늘|내일|today|tomorrow", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\d{1,2}:\d{2}", "", cleaned)

        cleaned = cleaned.strip()
        return cleaned if cleaned else None
