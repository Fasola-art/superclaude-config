#!/usr/bin/env python3
"""Coach 모듈 공통 타입"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MealType(Enum):
    """식사 종류"""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


@dataclass
class CoachLog:
    """Coach 기록 베이스"""
    timestamp: datetime
    notes: str = ""
