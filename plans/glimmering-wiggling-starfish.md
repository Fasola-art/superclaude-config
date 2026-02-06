# Autotrading Workflow 모듈 설계 플랜

> TRADING-WORKFLOW.md (1776줄) 기반, 8개 모듈 파일로 분할
> 위치: `~/.claude/modules/trading/autotrading-workflow/`

---

## 모듈 구조

```
autotrading-workflow/
├── index.md                  # ~35줄: 인덱스 + 실행 순서
├── decision-pipeline.md      # ~95줄: LLM→RL→Rule 의사결정
├── execution-engine.md       # ~90줄: 브로커 API + 주문 실행
├── risk-management.md        # ~85줄: 3단계 리스크 관리
├── backtesting-pipeline.md   # ~80줄: 백테스팅 + 검증
├── paper-trading.md          # ~70줄: 모의투자 + 전환 기준
├── rl-agent.md               # ~95줄: 강화학습 에이전트
└── monitoring-alerts.md      # ~80줄: 모니터링 + 알림
```

---

## 핵심 설계 결정

### 1. AI 의사결정 계층 (사용자 지정)

```
LLM 분석 (#4)  →  RL Agent (#3)  →  Rule-Based (#1)
  뉴스/매크로       최종 의사결정       폴백 안전망
  감성 분석         PPO/SAC            EMA/RSI/MACD
  컨피던스 생성     행동 선택           기계적 실행
```

- LLM: 4개 에이전트 (News/Macro/Tech/Signal) → 컨피던스 스코어 생성
- RL: 컨피던스 + 시장 상태 → BUY/SELL/HOLD 결정 (threshold: 0.7)
- Rule: RL 미적용/저신뢰 시 폴백 (EMA 크로스 + RSI + 볼린저)

### 2. 진행 순서 (사용자 지정: 3→1→2)

| 단계 | 내용 | 최소 기간 | 승인 기준 |
|------|------|----------|----------|
| Step 1 | 백테스팅 | 2주 | Sharpe≥1.5, MDD≤15%, Win≥55% |
| Step 2 | 페이퍼 트레이딩 | 30일 | 실시간 성과 일치, 시스템 안정성 |
| Step 3 | 소액 실거래 | 점진적 | 월 수익 양수, 리스크 한도 내 |

### 3. 디바이스 역할 배분

| 디바이스 | 역할 | 24h |
|----------|------|-----|
| Mac Studio M2 Ultra | Hub: LLM 분석, 오케스트레이션, DB | ✅ |
| 4090 Laptop | RL 학습 (야간), 대형 LLM 추론 | ❌ |
| Jetson Orin Nano | Edge: YOLO 차트 패턴, TensorRT | ✅ |
| RPi5 + Hailo8 | Edge: 뉴스 필터링, 감성 분류 | ✅ |
| 사무용 데스크탑 | 브로커 API 실행, MT5/거래소 연결 | ✅ |
| LG Gram | 백업 노드, 외출 시 모니터링 | ❌ |
| Galaxy Tab S8 Ultra | 대시보드, 알림 확인, 수동 개입 | ❌ |

### 4. 리스크 관리 (3단계 서킷브레이커)

| 레벨 | 조건 | 동작 |
|------|------|------|
| WARNING | 일일 손실 -3% | 포지션 사이즈 50% 축소 |
| CRITICAL | 일일 손실 -5% | 신규 진입 중단, 기존 유지 |
| EMERGENCY | 총 자산 -10% | 전 포지션 청산, 시스템 중지 |

---

## 각 파일 상세 설계

### index.md (~35줄)
- 모듈 개요 + 파일 링크
- 실행 순서 다이어그램
- 의사결정 계층 요약
- 디바이스 역할 요약 테이블

### decision-pipeline.md (~95줄)
- LLM 4-Agent 파이프라인 (News→Macro→Tech→Signal)
- RL Agent 인터페이스 (BaseStrategy 상속)
- Rule-Based 폴백 로직
- 컨피던스 스코어 합산 공식 (가중평균)
- 에스컬레이션 패턴: Mac Studio(3B/7B) → 4090(14B~72B) → Claude API
- MQTT 토픽: `signal/{symbol}/decision`

### execution-engine.md (~90줄)
- 브로커 API: MT5 (주식), Binance (크립토), IBKR (해외주식)
- 주문 유형: Market, Limit, Stop-Loss, Take-Profit, Trailing Stop
- ATR 기반 동적 포지션 사이징 공식
- 슬리피지/수수료 처리
- 주문 상태 추적 (Redis Pub/Sub)
- 실행 디바이스: 사무용 데스크탑 (24h)

### risk-management.md (~85줄)
- Per-Trade: ATR 기반 손절, 리스크 2% 제한
- Daily: 일일 손실 한도, 최대 동시 포지션 수
- Total: 전체 자산 대비 MDD 제한
- 서킷브레이커 3단계 (위 표 참조)
- 상관관계 리스크 (동일 섹터 과집중 방지)
- 리스크 이벤트 로깅 (PostgreSQL trading.risk_events)

### backtesting-pipeline.md (~80줄)
- 기존 `backtest_engine.py` 확장 방안
- Walk-Forward Validation (학습/검증/테스트 분할)
- 과적합 방지: Out-of-Sample 검증, Monte Carlo 시뮬레이션
- 승인 기준: Sharpe≥1.5, MDD≤15%, Win Rate≥55%, Profit Factor≥1.5
- 멀티 자산 백테스팅 지원
- 결과 저장: `trading.backtest_results` 테이블

### paper-trading.md (~70줄)
- 가상 포트폴리오 ($10K 시작)
- 실시간 시장 데이터 + 가상 주문 실행
- 슬리피지 시뮬레이션 (실제와 유사하게)
- 최소 30일 운영 후 평가
- 실거래 전환 기준: 월 수익률 양수, MDD ≤ 10%, 시스템 다운타임 < 1%
- 전환 시 초기 자본 제한 ($500 → 점진적 증가)

### rl-agent.md (~95줄)
- 알고리즘: PPO (기본) / SAC (고급) via Stable-Baselines3
- State Space (~30차원): 가격, 기술지표, LLM 컨피던스, 포지션 상태, 매크로 지표
- Action Space: {BUY, SELL, HOLD} × 포지션 사이즈 (0.1~1.0)
- Reward Function: PnL + Sharpe 보너스 - MDD 페널티 - 과거래 페널티
- 학습 스케줄: 4090에서 야간 학습, Mac Studio에서 추론
- BaseStrategy 인터페이스 준수 (`generate_signal()` 구현)
- 모델 저장: `~/.claude/modules/trading/models/rl/`

### monitoring-alerts.md (~80줄)
- 4단계 알림: EMERGENCY / CRITICAL / WARNING / INFO
- 알림 채널: Telegram (긴급), 대시보드 (일반), Galaxy Tab (모니터링)
- Grafana 대시보드: PnL, 포지션, 리스크, 시스템 상태
- 시스템 헬스체크: 디바이스 상태, DB 연결, 브로커 API 상태
- 로그 수집: PostgreSQL `meta.system_logs`
- 일일 리포트: 자동 생성 → Telegram 전송

---

## DB 스키마 확장

기존 `schema.sql` 테이블에 추가 필요:

```sql
-- 새 테이블
trading.rl_decisions        -- RL 에이전트 의사결정 기록
trading.paper_trades        -- 페이퍼 트레이딩 기록
trading.backtest_results    -- 백테스팅 결과
trading.risk_events         -- 리스크 이벤트 로그
trading.execution_orders    -- 주문 실행 기록
```

---

## 구현 순서 (~3주)

| 순서 | 파일 | 의존성 | 예상 기간 |
|------|------|--------|----------|
| 1 | risk-management.md | 없음 | Day 1 |
| 2 | backtesting-pipeline.md | risk | Day 2 |
| 3 | execution-engine.md | risk | Day 3 |
| 4 | paper-trading.md | execution, risk | Day 4 |
| 5 | decision-pipeline.md | 없음 | Day 5-6 |
| 6 | rl-agent.md | decision | Day 7-8 |
| 7 | monitoring-alerts.md | 전체 | Day 9 |
| 8 | index.md | 전체 | Day 10 |

---

## 참조 문서

| 문서 | 경로 |
|------|------|
| Trading Workflow | `~/.claude/modules/local-llm/knowledge/TRADING-WORKFLOW.md` |
| DB Schema | `~/.claude/modules/sql-trading/schema.sql` |
| Base Strategy | `~/.claude/modules/trading/strategies/base_strategy.py` |
| Trading Config | `~/.claude/modules/trading/config.json` |
| Trading Module | `~/.claude/modules/trading/CLAUDE.md` |
