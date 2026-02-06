#!/usr/bin/env python3
"""
JARVIS ML Predictor
scikit-learn 기반 시간대별 행동 패턴 학습 및 예측
"""

from __future__ import annotations

import threading
from datetime import datetime
from pathlib import Path
from typing import Any

# scikit-learn은 선택적 의존성
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("scikit-learn not installed. ML features disabled.")

from .manager import UsagePatternTracker
from .work_classifier import classify_work_type

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

    def predict_work_type(self, day_of_week: int | None = None, hour: int | None = None) -> dict[str, Any] | None:
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

    def suggest_next_action(self) -> str | None:
        """다음 행동 추천"""
        result = self.predict_work_type()
        if result:
            return f"{result['predicted_work_type']} (신뢰도: {result['confidence']}%)"
        return None


# 싱글톤 인스턴스
_predictor_instance: MLPredictor | None = None
_lock = threading.Lock()


def get_predictor() -> MLPredictor:
    """MLPredictor 싱글톤 반환"""
    global _predictor_instance
    with _lock:
        if _predictor_instance is None:
            _predictor_instance = MLPredictor()
        return _predictor_instance
