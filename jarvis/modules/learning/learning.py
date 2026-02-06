"""
JARVIS 학습 시스템 - 사용자 패턴 학습 및 제안

사용자 입력 → 행동 패턴을 학습하여 자동 제안 생성
"""
import json
from difflib import SequenceMatcher
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import Pattern, Feedback
from .db import LearningDB


class LearningSystem:
    """패턴 학습 및 제안 시스템"""

    def __init__(self, db_path: str = "~/.claude/jarvis/data/learning.db"):
        self.db = LearningDB(db_path)

    def record_pattern(
        self,
        category: str,
        input_text: str,
        output_action: str,
        context: Optional[dict] = None
    ) -> Pattern:
        """패턴 기록"""
        ctx = context or {}
        pattern_id = self.db.insert_pattern(
            category, input_text, output_action, ctx
        )
        return Pattern(
            id=pattern_id,
            category=category,
            input_text=input_text,
            output_action=output_action,
            context=ctx,
            confidence=1.0,
            created_at=datetime.now().isoformat()
        )

    def get_pattern(self, pattern_id: int) -> Optional[Pattern]:
        """패턴 조회"""
        return self.db.get_pattern(pattern_id)

    def find_similar(self, query: str, top_k: int = 5) -> list[Pattern]:
        """유사 패턴 검색 (문자열 유사도 기반)"""
        rows = self.db.get_all_patterns()

        scored = []
        for row in rows:
            sim = SequenceMatcher(None, query.lower(), row[2].lower()).ratio()
            scored.append((sim * row[5], row))  # 유사도 * 신뢰도

        scored.sort(key=lambda x: x[0], reverse=True)
        return [self.db._row_to_pattern(r) for _, r in scored[:top_k]]

    def record_feedback(self, pattern_id: int, positive: bool) -> None:
        """피드백 기록 및 신뢰도 업데이트"""
        delta = 0.1 if positive else -0.15
        self.db.insert_feedback(pattern_id, positive)
        self.db.update_confidence(pattern_id, delta)

    def get_suggestions(
        self,
        context: Optional[dict] = None,
        limit: int = 3
    ) -> list[Pattern]:
        """컨텍스트 기반 제안 생성"""
        return self.db.get_top_patterns(limit)

    def export_data(self, path: str) -> None:
        """학습 데이터 내보내기"""
        rows = self.db.get_all_patterns()
        data = {
            "patterns": [
                {
                    "category": p[1], "input_text": p[2],
                    "output_action": p[3], "context": json.loads(p[4]),
                    "confidence": p[5]
                }
                for p in rows
            ],
            "exported_at": datetime.now().isoformat()
        }
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def import_data(self, path: str) -> int:
        """학습 데이터 가져오기"""
        data = json.loads(Path(path).read_text())
        count = 0
        for p in data.get("patterns", []):
            self.record_pattern(
                p["category"], p["input_text"],
                p["output_action"], p.get("context")
            )
            count += 1
        return count
