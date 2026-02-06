# Paper Trading (모의투자 + 전환 기준)

> 가상 $10K 포트폴리오, 최소 30일 운영 후 실거래 전환 평가

---

## 가상 포트폴리오 설정

| 항목 | 값 | 비고 |
|------|------|------|
| 초기 자본 | $10,000 | 실거래 전환 시 $500 시작 |
| 수수료 | 실제와 동일 | 브로커별 수수료 적용 |
| 슬리피지 | 실제 + 0.05% | 보수적 추정 |
| 체결 | 다음 캔들 시가 | 즉시 체결 안 함 |
| 리스크 규칙 | 실거래와 동일 | 서킷브레이커 포함 |

---

## 실시간 운영

```
실시간 시장 데이터 (Binance/Polygon WebSocket)
    │
    ├── decision-pipeline (LLM→RL→Rule)
    │   └── 시그널 생성 (실거래와 동일 로직)
    │
    ├── 가상 주문 실행
    │   ├── 슬리피지 시뮬레이션
    │   ├── 수수료 차감
    │   └── 다음 캔들 시가 체결
    │
    └── 성과 기록
        ├── PostgreSQL: trading.paper_trades
        └── 일일 리포트 생성
```

---

## 실거래 전환 기준

| 기준 | 최소 요건 | 측정 기간 |
|------|----------|----------|
| 운영 기간 | ≥ 30일 | - |
| 월 수익률 | > 0% (양수) | 최근 30일 |
| Max Drawdown | ≤ 10% | 전체 |
| Win Rate | ≥ 50% | 전체 |
| 시스템 다운타임 | < 1% | 전체 |
| 시그널 지연 | < 5초 평균 | 최근 7일 |
| 백테스트 일치율 | ≥ 80% | 동일 기간 비교 |

---

## 전환 프로세스 (점진적)

| 단계 | 자본 | 기간 | 조건 |
|------|------|------|------|
| Phase 1 | $500 | 2주 | 페이퍼 기준 충족 |
| Phase 2 | $2,000 | 4주 | Phase 1 수익 양수 |
| Phase 3 | $5,000 | 4주 | Phase 2 MDD ≤ 8% |
| Phase 4 | $10,000+ | 지속 | Phase 3 Sharpe ≥ 1.5 |

**롤백 조건**: 각 Phase에서 MDD > 15% → 이전 Phase 복귀

---

## 페이퍼 vs 실거래 비교 지표

| 지표 | 허용 차이 | 초과 시 |
|------|----------|--------|
| 수익률 | ±5%p | 슬리피지 모델 재조정 |
| 체결률 | ≥ 95% | 주문 로직 점검 |
| 지연 시간 | < 2초 추가 | 네트워크/API 최적화 |

---

## DB 스키마

```sql
-- trading.paper_trades (페이퍼 트레이딩 기록)
CREATE TABLE trading.paper_trades (
    id SERIAL PRIMARY KEY,
    signal_id INT,
    symbol VARCHAR(20),
    side VARCHAR(10),
    quantity DECIMAL(20,8),
    entry_price DECIMAL(20,8),
    exit_price DECIMAL(20,8),
    simulated_slippage DECIMAL(10,6),
    commission DECIMAL(10,4),
    pnl DECIMAL(20,4),
    pnl_pct DECIMAL(10,4),
    entry_at TIMESTAMPTZ,
    exit_at TIMESTAMPTZ,
    strategy VARCHAR(100),
    metadata JSONB
);
```

---

**참조**: [backtesting-pipeline.md](backtesting-pipeline.md) | [execution-engine.md](execution-engine.md)
