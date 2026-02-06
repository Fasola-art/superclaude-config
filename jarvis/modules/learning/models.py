"""학습 시스템 데이터 모델"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Pattern:
    """학습된 패턴"""
    id: Optional[int]
    category: str
    input_text: str
    output_action: str
    context: dict
    confidence: float
    created_at: str


@dataclass
class Feedback:
    """사용자 피드백"""
    pattern_id: int
    positive: bool
    timestamp: str
