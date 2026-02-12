#!/usr/bin/env python3
"""
FinBERT 뉴스 감정분석기

모델: ProsusAI/finbert (금융 특화 BERT)
출력: sentiment 점수(-1~1) + 투자의견(매수/매도/관망)
"""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

_model = None
_tokenizer = None
_device = None

# (min_score, key, 한국어 라벨)
REC_RULES = [
    (0.6, "strong_buy", "적극 매수"),
    (0.3, "buy", "매수"),
    (0.1, "hold_pos", "관망(긍정)"),
    (-0.1, "hold_neg", "관망"),
    (-0.3, "sell", "매도"),
    (None, "strong_sell", "적극 매도"),
]


def _load_model() -> None:
    """FinBERT 모델 로드 (MPS 가속 지원)"""
    global _model, _tokenizer, _device
    if _model is not None:
        return
    name = "ProsusAI/finbert"
    _tokenizer = AutoTokenizer.from_pretrained(name)
    _model = AutoModelForSequenceClassification.from_pretrained(name)
    _device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    _model.to(_device)
    _model.eval()
    print(f"  FinBERT 로드 완료 (device: {_device})")


def get_recommendation(score: float) -> dict:
    """점수 기반 투자의견"""
    for threshold, key, label in REC_RULES:
        if threshold is None or score >= threshold:
            return {"key": key, "label": label}
    return {"key": "hold_neg", "label": "관망"}


def analyze_batch(texts: list[str]) -> list[dict]:
    """배치 감정분석 (MPS 가속)

    Returns: [{"positive": 0.8, "negative": 0.1, "neutral": 0.1,
               "score": 0.7, "recommendation": {...}}, ...]
    """
    _load_model()
    inputs = _tokenizer(
        texts, return_tensors="pt", truncation=True,
        max_length=512, padding=True,
    )
    inputs = {k: v.to(_device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = _model(**inputs).logits
        probs = torch.nn.functional.softmax(logits, dim=-1)

    results = []
    for p in probs.cpu().tolist():
        pos, neg, neu = p  # FinBERT: positive(0), negative(1), neutral(2)
        score = round(pos - neg, 4)
        results.append({
            "positive": round(pos, 4),
            "negative": round(neg, 4),
            "neutral": round(neu, 4),
            "score": score,
            "recommendation": get_recommendation(score),
        })
    return results


def analyze_text(text: str) -> dict:
    """단일 텍스트 감정분석"""
    return analyze_batch([text])[0]
