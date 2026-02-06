# Backtesting Pipeline (백테스팅 + 검증)

> Walk-Forward Validation, 과적합 방지, 승인 기준 기반

---

## 승인 기준 (모든 전략 필수 통과)

| 지표 | 최소 기준 | 우수 | 측정 기간 |
|------|----------|------|----------|
| Sharpe Ratio | ≥ 1.5 | ≥ 2.0 | 1년 |
| Max Drawdown | ≤ 15% | ≤ 10% | 전체 |
| Win Rate | ≥ 55% | ≥ 60% | 전체 |
| Profit Factor | ≥ 1.5 | ≥ 2.0 | 전체 |
| 거래 횟수 | ≥ 100 | ≥ 200 | 전체 |

---

## Walk-Forward Validation

```
전체 데이터 (3년)
├── Window 1: [학습 12M] [검증 3M] [테스트 3M]
├── Window 2:    [학습 12M] [검증 3M] [테스트 3M]
├── Window 3:       [학습 12M] [검증 3M] [테스트 3M]
└── Window 4:          [학습 12M] [검증 3M] [테스트 3M]

각 Window의 테스트 결과 합산 → 최종 성과 평가
```

### 데이터 분할 비율

| 구간 | 비율 | 용도 |
|------|------|------|
| 학습 (Train) | 60% | 파라미터 최적화 |
| 검증 (Validation) | 20% | 하이퍼파라미터 선택 |
| 테스트 (Test) | 20% | 최종 성과 평가 (1회만) |

---

## 과적합 방지

### Monte Carlo 시뮬레이션

- 거래 순서 1000회 셔플 → equity curve 재계산
- **95% 신뢰구간 하한**이 승인 기준 충족 시 승인
- `sharpe_lower` (5th percentile), `mdd_upper` (95th percentile) 계산

### 과적합 감지 지표

| 지표 | 경고 기준 | 의미 |
|------|----------|------|
| Train vs Test Sharpe | 차이 > 0.5 | 과적합 의심 |
| 파라미터 민감도 | ±10% 변경 시 성과 50%↓ | 과최적화 |
| 시장 레짐 별 성과 | 한 레짐에서만 수익 | 일반화 부족 |

---

## 기존 엔진 확장

`backtest_engine.py` + `BaseStrategy` 상속 전략을 `run_walkforward()` 메서드로 확장.
파라미터: `strategy`, `data`, `train_ratio=0.6`, `val_ratio=0.2`, `n_windows=4`

## 멀티 자산 백테스팅

| 자산군 | 데이터 소스 | 수수료 | 슬리피지 |
|--------|-----------|--------|---------|
| 미국 주식 | Yahoo/Polygon | 0.1% | ATR × 0.1 |
| 크립토 | Binance | 0.1% | ATR × 0.2 |
| 선물 | CME/MT5 | $2/계약 | 1 tick |

---

## DB 스키마

```sql
-- trading.backtest_results (백테스팅 결과)
CREATE TABLE trading.backtest_results (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(100),
    run_at TIMESTAMPTZ DEFAULT NOW(),
    data_start DATE,
    data_end DATE,
    symbols TEXT[],
    config JSONB,
    sharpe_ratio DECIMAL(6,3),
    max_drawdown DECIMAL(6,4),
    win_rate DECIMAL(5,4),
    profit_factor DECIMAL(6,3),
    total_trades INT,
    total_return DECIMAL(10,4),
    monte_carlo JSONB,          -- MC 시뮬레이션 결과
    walkforward JSONB,          -- WF 결과 (윈도우별)
    approved BOOLEAN DEFAULT false,
    approved_by VARCHAR(50)
);
```

---

**참조**: [risk-management.md](risk-management.md) | [paper-trading.md](paper-trading.md)
