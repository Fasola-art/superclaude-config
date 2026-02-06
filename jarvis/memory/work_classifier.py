#!/usr/bin/env python3
"""
Work Type Classifier
도구와 파일 경로 기반 작업 유형 분류
"""


def classify_work_type(tool_name: str, file_path: str = "") -> str:
    """도구와 파일 경로로 작업 유형 분류"""

    # 도구 기반 분류
    tool_mapping = {
        'Edit': 'code_editing',
        'Write': 'code_editing',
        'Read': 'code_reading',
        'Bash': 'command_execution',
        'Grep': 'code_search',
        'Glob': 'file_search',
        'Task': 'agent_execution',
    }

    work_type = tool_mapping.get(tool_name, 'other')

    # 파일 경로 기반 세분화
    if file_path:
        lower_path = file_path.lower()
        if 'test' in lower_path or 'spec' in lower_path:
            work_type = 'testing'
        elif '.md' in lower_path or 'readme' in lower_path or 'doc' in lower_path:
            work_type = 'documentation'
        elif '.git' in lower_path:
            work_type = 'version_control'

    return work_type


# 싱글톤 인스턴스 (thread-safe)
from threading import Lock

_predictor = None
_predictor_lock = Lock()


def get_predictor():
    """MLPredictor 싱글톤 반환 (thread-safe)"""
    from .ml_predictor import MLPredictor

    global _predictor
    if _predictor is None:
        with _predictor_lock:
            # Double-checked locking
            if _predictor is None:
                _predictor = MLPredictor()
    return _predictor


if __name__ == "__main__":
    from .pattern_analyzer import PatternAnalyzer

    predictor = get_predictor()

    print("=== JARVIS ML Predictor ===")

    prediction = predictor.predict_work_type()
    if prediction:
        print(f"\n현재 시간 예측: {prediction['predicted_work_type']}")
        print(f"신뢰도: {prediction['confidence']}%")
    else:
        print("\n아직 충분한 데이터가 없습니다. (최소 10개 패턴 필요)")

    print("\n피크 시간대:")
    for peak in PatternAnalyzer.get_peak_hours():
        print(f"  {peak['hour']}시 ({peak['period']}): {peak['frequency']}회")
