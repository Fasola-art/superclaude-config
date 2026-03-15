# SQL Trading Rules

> **Version**: 2026.02
> **Target**: PostgreSQL 15+
> **Goal**: 효율적인 대체 데이터 분석 쿼리

---

## Priority Summary

| Priority | Category | Rules | Key Effect |
|----------|----------|-------|------------|
| CRITICAL | PERF | 5 | 쿼리 성능 최적화 |
| CRITICAL | SAFETY | 4 | 데이터 무결성 보장 |
| HIGH | TIMESERIES | 5 | 시계열 분석 패턴 |
| HIGH | AGGREGATE | 4 | 집계 쿼리 최적화 |
| MEDIUM | STYLE | 4 | 코드 가독성 |
| LOW | MAINTENANCE | 3 | 유지보수성 |

---

## CRITICAL: PERF (성능 최적화)

### PERF-001: 인덱스 활용 필수

```sql
-- BAD: 인덱스 없는 컬럼 조건
SELECT * FROM logistics_tracking WHERE cargo_type = 'container';

-- GOOD: 인덱스 있는 컬럼 우선 사용
SELECT * FROM logistics_tracking
WHERE timestamp > NOW() - INTERVAL '30 days'  -- 인덱스 있음
  AND cargo_type = 'container';
```

### PERF-002: LIMIT 항상 사용

```sql
-- BAD: 전체 데이터 조회
SELECT * FROM market_snapshots WHERE symbol = 'AAPL';

-- GOOD: 필요한 만큼만 조회
SELECT * FROM market_snapshots
WHERE symbol = 'AAPL'
ORDER BY timestamp DESC
LIMIT 100;
```

### PERF-003: SELECT * 지양

```sql
-- BAD: 모든 컬럼 조회
SELECT * FROM logistics_tracking;

-- GOOD: 필요한 컬럼만 명시
SELECT shipment_id, timestamp, status, origin_port, dest_port
FROM logistics_tracking;
```

### PERF-004: 서브쿼리 대신 CTE 또는 JOIN

```sql
-- BAD: 상관 서브쿼리
SELECT *
FROM logistics_tracking lt
WHERE (SELECT MAX(timestamp) FROM logistics_tracking lt2 WHERE lt2.shipment_id = lt.shipment_id) = lt.timestamp;

-- GOOD: 윈도우 함수 사용
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY shipment_id ORDER BY timestamp DESC) as rn
    FROM logistics_tracking
) t
WHERE rn = 1;
```

### PERF-005: 대용량 INSERT 배치 처리

```sql
-- BAD: 개별 INSERT
INSERT INTO market_snapshots VALUES (...);
INSERT INTO market_snapshots VALUES (...);

-- GOOD: 배치 INSERT
INSERT INTO market_snapshots (symbol, timestamp, price, volume)
VALUES
    ('AAPL', '2026-02-01', 185.50, 1000000),
    ('GOOGL', '2026-02-01', 142.30, 500000),
    ('MSFT', '2026-02-01', 405.20, 800000);
```

---

## CRITICAL: SAFETY (안전성)

### SAFETY-001: 트랜잭션 사용

```sql
-- 중요한 데이터 변경은 트랜잭션으로
BEGIN;

INSERT INTO trading_signals (timestamp, symbol, signal_type, confidence)
VALUES (NOW(), 'AAPL', 'BUY', 0.85);

UPDATE market_snapshots
SET metadata = metadata || '{"signaled": true}'::jsonb
WHERE symbol = 'AAPL' AND timestamp = (SELECT MAX(timestamp) FROM market_snapshots WHERE symbol = 'AAPL');

COMMIT;
```

### SAFETY-002: WHERE 절 필수 (UPDATE/DELETE)

```sql
-- BAD: WHERE 없는 UPDATE (위험!)
UPDATE logistics_tracking SET status = 'completed';

-- GOOD: 명확한 WHERE 조건
UPDATE logistics_tracking
SET status = 'completed'
WHERE shipment_id = 'SHIP-001'
  AND timestamp = '2026-02-01 10:00:00';
```

### SAFETY-003: NULL 처리

```sql
-- BAD: NULL 무시
SELECT AVG(change_pct) FROM market_snapshots;

-- GOOD: NULL 명시적 처리
SELECT
    AVG(COALESCE(change_pct, 0)) as avg_change,
    COUNT(*) FILTER (WHERE change_pct IS NULL) as null_count
FROM market_snapshots;
```

### SAFETY-004: 타입 캐스팅 명시

```sql
-- BAD: 암시적 타입 변환
SELECT * FROM economic_indicators WHERE value > '100';

-- GOOD: 명시적 타입 캐스팅
SELECT * FROM economic_indicators WHERE value > 100::DECIMAL;
```

---

## HIGH: TIMESERIES (시계열 분석)

### TS-001: 날짜 범위 인덱스 활용

```sql
-- 시계열 데이터 조회 시 인덱스 범위 스캔 활용
SELECT *
FROM market_snapshots
WHERE timestamp >= '2026-01-01'
  AND timestamp < '2026-02-01'
ORDER BY timestamp;
```

### TS-002: 윈도우 함수 활용

```sql
-- 이동평균, 누적합 등
SELECT
    timestamp,
    symbol,
    price,
    AVG(price) OVER (
        PARTITION BY symbol
        ORDER BY timestamp
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as ma_30,
    price - LAG(price) OVER (PARTITION BY symbol ORDER BY timestamp) as price_change
FROM market_snapshots
WHERE timestamp > NOW() - INTERVAL '90 days';
```

### TS-003: 날짜 트렁케이션

```sql
-- 일별/주별/월별 집계
SELECT
    DATE_TRUNC('week', timestamp) as week,
    symbol,
    AVG(price) as avg_price,
    SUM(volume) as total_volume
FROM market_snapshots
WHERE timestamp > NOW() - INTERVAL '1 year'
GROUP BY DATE_TRUNC('week', timestamp), symbol
ORDER BY week DESC;
```

### TS-004: 시계열 갭 처리

```sql
-- generate_series로 날짜 갭 채우기
WITH date_series AS (
    SELECT generate_series(
        '2026-01-01'::date,
        '2026-01-31'::date,
        '1 day'::interval
    )::date as date
),
daily_data AS (
    SELECT DATE(timestamp) as date, AVG(price) as avg_price
    FROM market_snapshots
    WHERE symbol = 'AAPL'
    GROUP BY DATE(timestamp)
)
SELECT
    ds.date,
    COALESCE(dd.avg_price, LAG(dd.avg_price) OVER (ORDER BY ds.date)) as price
FROM date_series ds
LEFT JOIN daily_data dd ON ds.date = dd.date;
```

### TS-005: 전기 대비 변화율

```sql
-- YoY, MoM 변화율 계산
SELECT
    DATE_TRUNC('month', date) as month,
    series_id,
    value,
    LAG(value, 12) OVER (PARTITION BY series_id ORDER BY date) as value_1y_ago,
    ROUND(100.0 * (value - LAG(value, 12) OVER (PARTITION BY series_id ORDER BY date))
        / NULLIF(LAG(value, 12) OVER (PARTITION BY series_id ORDER BY date), 0), 2) as yoy_change
FROM economic_indicators
WHERE category = 'inflation';
```

---

## HIGH: AGGREGATE (집계 쿼리)

### AGG-001: FILTER 절 활용

```sql
-- BAD: CASE WHEN 사용
SELECT
    COUNT(CASE WHEN status = 'delayed' THEN 1 END) as delayed,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered
FROM logistics_tracking;

-- GOOD: FILTER 절 사용
SELECT
    COUNT(*) FILTER (WHERE status = 'delayed') as delayed,
    COUNT(*) FILTER (WHERE status = 'delivered') as delivered,
    COUNT(*) as total
FROM logistics_tracking;
```

### AGG-002: GROUP BY 롤업

```sql
-- 다중 수준 집계
SELECT
    COALESCE(origin_port, 'ALL') as origin,
    COALESCE(dest_port, 'ALL') as dest,
    COUNT(*) as shipments,
    AVG(EXTRACT(EPOCH FROM (estimated_arrival - timestamp))/3600) as avg_hours
FROM logistics_tracking
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY ROLLUP (origin_port, dest_port)
ORDER BY origin_port NULLS LAST, dest_port NULLS LAST;
```

### AGG-003: 백분위수 계산

```sql
-- 가격 분포 분석
SELECT
    symbol,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) as p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price) as median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) as p75,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY price) as p95
FROM market_snapshots
WHERE timestamp > NOW() - INTERVAL '90 days'
GROUP BY symbol;
```

### AGG-004: DISTINCT ON 활용

```sql
-- 그룹별 최신 레코드
SELECT DISTINCT ON (symbol)
    symbol,
    timestamp,
    price,
    change_pct
FROM market_snapshots
ORDER BY symbol, timestamp DESC;
```

---

## MEDIUM: STYLE (코딩 스타일)

### STYLE-001: CTE로 가독성 향상

```sql
-- 복잡한 쿼리는 CTE로 분리
WITH recent_trades AS (
    SELECT *
    FROM trade_statistics
    WHERE period >= TO_CHAR(NOW() - INTERVAL '6 months', 'YYYYMM')
),
monthly_summary AS (
    SELECT
        period,
        reporter_name,
        SUM(trade_value) as total_value
    FROM recent_trades
    GROUP BY period, reporter_name
)
SELECT
    period,
    reporter_name,
    total_value,
    RANK() OVER (PARTITION BY period ORDER BY total_value DESC) as rank
FROM monthly_summary;
```

### STYLE-002: 명확한 별칭 사용

```sql
-- BAD: 불명확한 별칭
SELECT a.id, b.name FROM t1 a JOIN t2 b ON a.id = b.fk;

-- GOOD: 의미 있는 별칭
SELECT
    lt.shipment_id,
    lt.status,
    fi.value as freight_index
FROM logistics_tracking lt
JOIN freight_indices fi ON lt.timestamp::date = fi.date;
```

### STYLE-003: 조건절 정렬

```sql
-- WHERE 조건은 선택성 높은 순서로
SELECT *
FROM logistics_tracking
WHERE shipment_id = 'SHIP-001'      -- 가장 선택적
  AND timestamp > NOW() - INTERVAL '7 days'  -- 범위 조건
  AND status IN ('in_transit', 'delayed');   -- 다중 값
```

### STYLE-004: 주석 활용

```sql
-- 복잡한 쿼리에 주석 추가
-- 목적: 물류 지연과 관련 주식 영향 분석
-- 작성: 2026-02-02
-- 업데이트: 지연율 계산 로직 수정

WITH delay_stats AS (
    -- 항로별 지연 통계 계산
    SELECT
        origin_port,
        dest_port,
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE status = 'delayed') as delayed
    FROM logistics_tracking
    WHERE timestamp > NOW() - INTERVAL '30 days'
    GROUP BY origin_port, dest_port
)
SELECT
    origin_port,
    dest_port,
    total,
    delayed,
    ROUND(100.0 * delayed / total, 2) as delay_rate  -- 백분율
FROM delay_stats
WHERE total >= 10  -- 통계적 유의성을 위한 최소 샘플
ORDER BY delay_rate DESC;
```

---

## LOW: MAINTENANCE (유지보수)

### MAINT-001: EXPLAIN 분석

```sql
-- 쿼리 성능 분석
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT *
FROM logistics_tracking
WHERE timestamp > NOW() - INTERVAL '30 days'
  AND status = 'delayed';
```

### MAINT-002: 통계 업데이트

```sql
-- 대량 데이터 변경 후 통계 갱신
ANALYZE logistics_tracking;
ANALYZE market_snapshots;
```

### MAINT-003: 오래된 데이터 정리

```sql
-- 파티셔닝 또는 아카이브 전략
-- 1년 이상 된 상세 데이터 아카이브
WITH archived AS (
    DELETE FROM market_snapshots
    WHERE timestamp < NOW() - INTERVAL '1 year'
    RETURNING *
)
INSERT INTO market_snapshots_archive
SELECT * FROM archived;
```

---

## Quick Reference

### 자주 사용하는 패턴

```sql
-- 최신 N개 레코드
SELECT * FROM table ORDER BY timestamp DESC LIMIT N;

-- 그룹별 최신 레코드
SELECT DISTINCT ON (group_col) * FROM table ORDER BY group_col, timestamp DESC;

-- 이동평균
AVG(col) OVER (ORDER BY timestamp ROWS BETWEEN N PRECEDING AND CURRENT ROW)

-- 전기 대비 변화
col - LAG(col) OVER (ORDER BY timestamp)

-- 날짜 범위 생성
generate_series('2026-01-01'::date, '2026-01-31'::date, '1 day'::interval)

-- NULL 안전 나눗셈
NULLIF(denominator, 0)
```

---

**META**
- Version: 2026.02
- Last Updated: 2026-02-02
- Category: SQL / Trading
