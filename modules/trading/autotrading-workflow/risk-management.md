# Risk Management (3단계 리스크 관리)

> Per-Trade → Daily → Total 계층형 리스크 제어

---

## 서킷브레이커 (3단계)

| Level | 조건 | 동작 | 복구 |
|-------|------|------|------|
| WARNING | 일일 손실 -3% | 포지션 사이즈 50% 축소 | 자동 (익일) |
| CRITICAL | 일일 손실 -5% | 신규 진입 중단, 기존 유지 | 수동 승인 |
| EMERGENCY | 총 자산 -10% | 전 포지션 청산, 시스템 중지 | 수동 재개 |

---

## Per-Trade 리스크

### ATR 기반 손절

```python
# 포지션별 리스크 한도: 총 자본의 2%
risk_per_trade = capital * 0.02
atr = calculate_atr(symbol, period=14)
stop_distance = atr * 2.0  # ATR 2배
position_size = risk_per_trade / stop_distance
```

### 주문 유형별 설정

| 유형 | 기준 | 비고 |
|------|------|------|
| Stop-Loss | ATR × 2.0 | 패턴 무효화 가격 |
| Take-Profit | ATR × 3.0 (R:R 1:1.5) | 1차 익절 |
| Trailing Stop | ATR × 1.5 | 수익 보호 |

---

## Daily 리스크

### 일일 한도

| 항목 | 한도 | 동작 |
|------|------|------|
| 최대 일일 손실 | -5% | CRITICAL 발동 |
| 최대 동시 포지션 | 5개 | 신규 진입 거부 |
| 최대 동일 섹터 | 2개 | 섹터 과집중 방지 |
| 최대 일일 거래 횟수 | 20회 | 과거래 방지 |

### 상관관계 리스크

```python
# 동일 섹터 과집중 방지
sector_exposure = sum(position.weight for p in positions if p.sector == sector)
if sector_exposure > 0.30:  # 30% 초과
    reject_new_entry(symbol)

# 높은 상관관계 종목 제한
correlation = calculate_correlation(symbol_a, symbol_b, window=60)
if correlation > 0.8:
    reduce_combined_size(max_weight=0.20)
```

---

## Total 리스크 (포트폴리오)

| 항목 | 한도 | 모니터링 |
|------|------|---------|
| 최대 MDD | -15% | 실시간 |
| 최대 투자 비율 | 80% (20% 현금) | 일일 점검 |
| VaR (95%) | -3% | 일일 계산 |

---

## ATR 기반 동적 포지션 사이징

```python
def calculate_position_size(
    capital: float,
    price: float,
    atr: float,
    risk_pct: float = 0.02,
    atr_multiplier: float = 2.0
) -> float:
    """리스크 기반 포지션 크기 계산"""
    risk_amount = capital * risk_pct
    stop_distance = atr * atr_multiplier
    shares = risk_amount / stop_distance
    max_position = capital * 0.20  # 단일 포지션 최대 20%
    return min(shares, max_position / price)
```

---

## DB 스키마

```sql
-- trading.risk_events (리스크 이벤트 로그)
CREATE TABLE trading.risk_events (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    event_level VARCHAR(20),      -- WARNING, CRITICAL, EMERGENCY
    trigger_type VARCHAR(50),     -- daily_loss, mdd, sector_concentration
    trigger_value DECIMAL(10,4),
    threshold DECIMAL(10,4),
    action_taken TEXT,            -- reduce_size, stop_entry, liquidate_all
    affected_symbols TEXT[],
    portfolio_snapshot JSONB,
    resolved_at TIMESTAMPTZ,
    resolved_by VARCHAR(50)       -- auto, manual
);
```

---

**참조**: [execution-engine.md](execution-engine.md) | [monitoring-alerts.md](monitoring-alerts.md)
