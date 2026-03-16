# Autotrading Workflow

> LLM → RL → Rule 기반 자동매매 시스템 | 분산 엣지-허브 아키텍처

---

## 실행 순서 (3→1→2)

| Step | 내용 | 최소 기간 | 승인 기준 |
|------|------|----------|----------|
| 1 | [백테스팅](backtesting-pipeline.md) | 2주 | Sharpe≥1.5, MDD≤15% |
| 2 | [페이퍼 트레이딩](paper-trading.md) | 30일 | 월수익 양수, 시스템 안정 |
| 3 | 소액 실거래 | 점진적 | $500→$2K→$5K→$10K+ |

---

## 의사결정 계층

```
LLM 4-Agent → RL Agent (PPO/SAC) → Rule-Based 폴백
 (컨피던스)    (최종 결정)          (EMA/RSI/BB)
```

---

## 모듈 파일

| 파일 | 내용 |
|------|------|
| [decision-pipeline.md](decision-pipeline.md) | LLM→RL→Rule 의사결정 |
| [rl-agent.md](rl-agent.md) | 강화학습 에이전트 설계 |
| [execution-engine.md](execution-engine.md) | 브로커 API + 주문 실행 |
| [risk-management.md](risk-management.md) | 3단계 리스크 관리 |
| [backtesting-pipeline.md](backtesting-pipeline.md) | 백테스팅 + 검증 |
| [paper-trading.md](paper-trading.md) | 모의투자 + 전환 기준 |
| [monitoring-alerts.md](monitoring-alerts.md) | 모니터링 + 알림 |

---

## 디바이스 역할

| 디바이스 | 역할 | 24h |
|---------|------|-----|
| Windows RTX 4090 Laptop | LLM 분석, 오케스트레이션, DB | ✅ |
| 4090 Laptop | RL 학습 (야간), 대형 LLM | ❌ |
| Jetson Orin Nano | YOLO 차트 패턴, TensorRT | ✅ |
| RPi5 + Hailo8 | 뉴스 필터링, 감성 분류 | ✅ |
| 사무용 데스크탑 | 브로커 API, 주문 실행 | ✅ |

---

## 참조

| 문서 | 경로 |
|------|------|
| 원본 워크플로우 | `modules/local-llm/knowledge/TRADING-WORKFLOW.md` |
| DB 스키마 | `modules/sql-trading/schema.sql` |
| BaseStrategy | `modules/trading/strategies/base_strategy.py` |
