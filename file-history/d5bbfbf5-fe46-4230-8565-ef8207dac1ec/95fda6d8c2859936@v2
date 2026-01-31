#!/usr/bin/env python3
"""
JARVIS ML Predictor
scikit-learn 기반 시간대별 행동 패턴 학습 및 예측
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# scikit-learn은 선택적 의존성
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("scikit-learn not installed. ML features disabled.")

from manager import get_connection, UsagePatternTracker

MODEL_PATH = Path(__file__).parent / "predictor_model.json"
MIN_PATTERNS_FOR_PREDICTION = 10


class MLPredictor:
    """행동 패턴 예측기"""

    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.work_types = []
        self._load_or_train()

    def _load_or_train(self):
        """모델 로드 또는 학습"""
        if not SKLEARN_AVAILABLE:
            return

        patterns = UsagePatternTracker.get_patterns()

        if len(patterns) < MIN_PATTERNS_FOR_PREDICTION:
            return

        # 데이터 준비
        X = []
        y = []

        for p in patterns:
            # 빈도만큼 데이터 복제 (가중치 효과)
            for _ in range(min(p['frequency'], 10)):  # 최대 10번까지만
                X.append([p['day_of_week'], p['hour']])
                y.append(p['work_type'])

        if len(set(y)) < 2:  # 최소 2개 클래스 필요
            return

        X = np.array(X)

        # Label Encoding
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        self.work_types = list(self.label_encoder.classes_)

        # 모델 학습
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X, y_encoded)

    def predict_work_type(self, day_of_week: int = None, hour: int = None) -> Optional[Dict]:
        """현재 시간에 예상되는 작업 유형 예측"""
        if not SKLEARN_AVAILABLE or self.model is None:
            return None

        now = datetime.now()
        if day_of_week is None:
            day_of_week = now.weekday()
        if hour is None:
            hour = now.hour

        X_pred = np.array([[day_of_week, hour]])

        # 확률 예측
        proba = self.model.predict_proba(X_pred)[0]
        predicted_idx = np.argmax(proba)
        confidence = proba[predicted_idx]

        return {
            'predicted_work_type': self.work_types[predicted_idx],
            'confidence': round(confidence * 100, 1),
            'all_probabilities': {
                self.work_types[i]: round(p * 100, 1)
                for i, p in enumerate(proba)
            }
        }

    def get_peak_hours(self, work_type: str = None) -> List[Dict]:
        """특정 작업 유형의 피크 시간대 분석"""
        patterns = UsagePatternTracker.get_patterns()

        if work_type:
            patterns = [p for p in patterns if p['work_type'] == work_type]

        # 시간대별 집계
        hour_totals = {}
        for p in patterns:
            hour = p['hour']
            if hour not in hour_totals:
                hour_totals[hour] = 0
            hour_totals[hour] += p['frequency']

        # 상위 시간대 반환
        sorted_hours = sorted(hour_totals.items(), key=lambda x: x[1], reverse=True)

        return [
            {'hour': h, 'frequency': f, 'period': self._hour_to_period(h)}
            for h, f in sorted_hours[:5]
        ]

    def get_weekly_pattern(self) -> Dict[str, List]:
        """요일별 패턴 분석"""
        patterns = UsagePatternTracker.get_patterns()

        days = ['월', '화', '수', '목', '금', '토', '일']
        day_patterns = {day: [] for day in days}

        for p in patterns:
            day_name = days[p['day_of_week']]
            day_patterns[day_name].append({
                'hour': p['hour'],
                'work_type': p['work_type'],
                'frequency': p['frequency']
            })

        return day_patterns

    def suggest_next_action(self) -> Optional[str]:
        """다음 작업 제안"""
        prediction = self.predict_work_type()

        if not prediction or prediction['confidence'] < 50:
            return None

        work_type = prediction['predicted_work_type']
        confidence = prediction['confidence']

        suggestions = {
            'code_editing': "코드 작성/수정 작업이 예상됩니다.",
            'testing': "테스트 관련 작업이 예상됩니다.",
            'version_control': "Git 작업이 예상됩니다.",
            'documentation': "문서 작업이 예상됩니다.",
            'debugging': "디버깅 작업이 예상됩니다.",
            'review': "코드 리뷰가 예상됩니다."
        }

        base_suggestion = suggestions.get(work_type, f"{work_type} 작업이 예상됩니다.")

        return f"{base_suggestion} (신뢰도: {confidence}%)"

    @staticmethod
    def _hour_to_period(hour: int) -> str:
        """시간을 시간대 문자열로 변환"""
        if 5 <= hour < 9:
            return "이른 아침"
        elif 9 <= hour < 12:
            return "오전"
        elif 12 <= hour < 14:
            return "점심"
        elif 14 <= hour < 18:
            return "오후"
        elif 18 <= hour < 21:
            return "저녁"
        elif 21 <= hour < 24:
            return "밤"
        else:
            return "새벽"


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


# 싱글톤 인스턴스
_predictor = None

def get_predictor() -> MLPredictor:
    """MLPredictor 싱글톤 반환"""
    global _predictor
    if _predictor is None:
        _predictor = MLPredictor()
    return _predictor


if __name__ == "__main__":
    predictor = get_predictor()

    print("=== JARVIS ML Predictor ===")

    prediction = predictor.predict_work_type()
    if prediction:
        print(f"\n현재 시간 예측: {prediction['predicted_work_type']}")
        print(f"신뢰도: {prediction['confidence']}%")
    else:
        print("\n아직 충분한 데이터가 없습니다. (최소 10개 패턴 필요)")

    print("\n피크 시간대:")
    for peak in predictor.get_peak_hours():
        print(f"  {peak['hour']}시 ({peak['period']}): {peak['frequency']}회")
