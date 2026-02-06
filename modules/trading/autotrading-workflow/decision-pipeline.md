# Decision Pipeline (LLM → RL → Rule 의사결정)

> 3계층 의사결정: LLM 분석 → RL 최종 결정 → Rule-Based 폴백

---

## 의사결정 계층

```
LLM 분석 (Layer 1)    RL Agent (Layer 2)    Rule-Based (Layer 3)
  뉴스/매크로/감성       최종 의사결정          폴백 안전망
  컨피던스 생성          PPO/SAC              EMA/RSI/MACD
  4-Agent 파이프라인     행동 선택             기계적 실행
```

| 계층 | 트리거 | 출력 |
|------|--------|------|
| LLM | 뉴스/지표/차트 도착 | 컨피던스 스코어 (0~1) |
| RL | LLM 컨피던스 ≥ 0.5 | BUY/SELL/HOLD + 사이즈 |
| Rule | RL 미적용 또는 confidence < 0.7 | EMA Cross + RSI + BB |

---

## LLM 4-Agent 파이프라인

```
뉴스 도착 ──→ NewsAgent ──┐
지표 발표 ──→ MacroAgent ─┤──→ SignalAgent ──→ 컨피던스 합산
젯슨 YOLO ──→ TechAgent ──┤
스케줄   ──→ (정기 분석) ──┘
```

### Agent별 역할

| Agent | 모델 | 분석 대상 | 가중치 |
|-------|------|----------|--------|
| NewsAgent | Qwen 3B/7B | 뉴스 감성, 영향 종목 | 0.25 |
| MacroAgent | Qwen 3B/7B | FRED, FedWatch, COT | 0.25 |
| TechAgent | Qwen 3B + YOLO | EMA, 패턴, 볼륨프로파일 | 0.30 |
| SignalAgent | Qwen 7B | 통합 검증, 최종 스코어 | 0.20 |

### 컨피던스 합산 공식

```python
final_confidence = (
    news_conf * 0.25 +
    macro_conf * 0.25 +
    tech_conf * 0.30 +
    signal_conf * 0.20
)
# 범위: 0.0 ~ 1.0
# threshold: 0.7 (이상 시 시그널 발행)
```

---

## 에스컬레이션 패턴

```
Mac Studio (Qwen 3B/7B)
    │
    ├── confidence ≥ 0.6 → 시그널 발행
    │
    ├── confidence < 0.6 → 4090 노트북 (Qwen 14B~72B)
    │   ├── confidence ≥ 0.6 → 시그널 발행
    │   └── confidence < 0.6 → Claude API
    │       └── 최종 판단
    │
    └── 복잡한 추론 (다중 요소) → Claude API 직접
```

---

## RL Agent 인터페이스

`RLStrategy(BaseStrategy)` → `generate_signal()` 구현.
State 구성 → RL 모델 추론 → `TradeSignal` 반환 (confidence ≥ 0.7 시 발행).

상세 설계: [rl-agent.md](rl-agent.md)

---

## Rule-Based 폴백

### 적용 조건

- RL Agent 미배포 상태
- RL confidence < 0.7
- 시스템 장애 시 자동 전환

### 폴백 규칙

| 조건 | 시그널 | 신뢰도 |
|------|--------|--------|
| EMA 8 > 16 > 32 (정배열) + RSI < 70 | BUY | 0.6 |
| EMA 8 < 16 < 32 (역배열) + RSI > 30 | SELL | 0.6 |
| 볼린저 하단 터치 + RSI < 30 | BUY | 0.5 |
| 볼린저 상단 터치 + RSI > 70 | SELL | 0.5 |
| MACD 골든크로스 + 거래량 2배 | BUY | 0.7 |

---

## MQTT 토픽

| 토픽 | 발행자 | 내용 |
|------|--------|------|
| `analysis/{symbol}/news` | NewsAgent | 뉴스 분석 결과 |
| `analysis/{symbol}/macro` | MacroAgent | 매크로 분석 |
| `analysis/{symbol}/tech` | TechAgent | 기술적 분석 |
| `signal/{symbol}/decision` | SignalAgent/RL | 최종 시그널 |

---

**참조**: [rl-agent.md](rl-agent.md) | [execution-engine.md](execution-engine.md)
