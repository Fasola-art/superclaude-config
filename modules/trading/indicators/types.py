#!/usr/bin/env python3
"""기술 지표 공통 타입"""

from dataclasses import dataclass


@dataclass
class OHLCV:
    """캔들스틱 데이터"""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float
