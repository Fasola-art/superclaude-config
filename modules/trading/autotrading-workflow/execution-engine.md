# Execution Engine (브로커 API + 주문 실행)

> 실행 디바이스: 사무용 데스크탑 (24h), 백업: 4090 노트북

---

## 브로커 API 연동

| 브로커 | 자산군 | API | 디바이스 |
|--------|--------|-----|---------|
| MT5 (키움) | 한국주식/선물 | MetaTrader5 Python | 사무용 데스크탑 |
| Binance | 크립토 | python-binance | 사무용 데스크탑 |
| IBKR | 해외주식/선물 | ib_insync | 사무용 데스크탑 |
| 토스증권 | 한국주식 (간편) | REST API | 모바일 (수동) |

---

## 주문 유형

| 유형 | 용도 | 파라미터 |
|------|------|---------|
| Market | 즉시 체결 (긴급) | symbol, side, qty |
| Limit | 지정가 진입 | + price |
| Stop-Loss | 손절 | trigger_price |
| Take-Profit | 익절 | target_price |
| Trailing Stop | 수익 보호 | trail_distance (ATR기반) |
| OCO | 손절+익절 동시 | stop_price + take_price |

---

## 주문 실행 파이프라인

```
시그널 수신 (MQTT: signal/{symbol}/decision)
    │
    ├── 1. 리스크 검증 (risk-management 참조)
    │   ├── 서킷브레이커 상태 확인
    │   ├── 일일 거래 한도 확인
    │   └── 포지션 사이즈 계산 (ATR 기반)
    │
    ├── 2. 주문 생성
    │   ├── 브로커 API 선택 (자산군 기반)
    │   ├── 슬리피지 보정 (±0.1%)
    │   └── 수수료 계산
    │
    ├── 3. 주문 전송
    │   ├── 체결 대기 (timeout: 30초)
    │   ├── 부분 체결 처리
    │   └── 실패 시 재시도 (최대 3회)
    │
    └── 4. 주문 추적
        ├── Redis Pub/Sub: order/{order_id}/status
        ├── 체결 확인 → DB 기록
        └── 연동 주문 설정 (SL/TP)
```

---

## 슬리피지 & 수수료

| 자산군 | 예상 슬리피지 | 수수료 | 스프레드 |
|--------|-------------|--------|---------|
| 한국주식 | 0.05% | 0.015% (키움) | - |
| 미국주식 | 0.03% | $0 (IBKR Lite) | - |
| 크립토 | 0.10% | 0.10% (Binance) | 0.01% |
| 선물 | 1 tick | $2/계약 | 1 tick |

---

## 주문 상태 관리

```python
class OrderStatus(Enum):
    PENDING = 'pending'          # 대기
    SUBMITTED = 'submitted'      # 전송됨
    PARTIALLY_FILLED = 'partial' # 부분 체결
    FILLED = 'filled'            # 전량 체결
    CANCELLED = 'cancelled'      # 취소
    REJECTED = 'rejected'        # 거부
    EXPIRED = 'expired'          # 만료
```

Redis Pub/Sub: `order/{order_id}/status` 채널로 상태 실시간 발행.

## DB 스키마

```sql
-- trading.execution_orders (주문 실행 기록)
CREATE TABLE trading.execution_orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE,
    signal_id INT REFERENCES trading.signals(id),
    symbol VARCHAR(20),
    broker VARCHAR(50),           -- mt5, binance, ibkr
    order_type VARCHAR(20),       -- market, limit, stop_loss
    side VARCHAR(10),             -- buy, sell
    quantity DECIMAL(20,8),
    requested_price DECIMAL(20,8),
    filled_price DECIMAL(20,8),
    slippage DECIMAL(10,6),
    commission DECIMAL(10,4),
    status VARCHAR(20),
    submitted_at TIMESTAMPTZ,
    filled_at TIMESTAMPTZ,
    error_message TEXT,
    metadata JSONB
);
```

---

**참조**: [risk-management.md](risk-management.md) | [decision-pipeline.md](decision-pipeline.md)
