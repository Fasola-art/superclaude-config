-- ============================================
-- 물류 분석 쿼리 (Logistics Queries)
-- ============================================
-- Module: sql-trading
-- Version: 1.0
-- ============================================

-- ============================================
-- 1. 물류 지연 분석
-- ============================================

-- 1.1 항로별 지연 현황 (최근 30일)
-- @name: logistics_delays_by_route
SELECT
    origin_port,
    dest_port,
    COUNT(*) as total_shipments,
    COUNT(*) FILTER (WHERE status = 'delayed') as delayed_count,
    COUNT(*) FILTER (WHERE status = 'in_transit') as in_transit_count,
    COUNT(*) FILTER (WHERE status = 'delivered') as delivered_count,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'delayed') / COUNT(*), 2) as delay_rate_pct
FROM logistics_tracking
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY origin_port, dest_port
HAVING COUNT(*) >= 5  -- 최소 샘플 수
ORDER BY delay_rate_pct DESC;

-- 1.2 일별 지연 추이
-- @name: daily_delay_trend
SELECT
    DATE(timestamp) as date,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE status = 'delayed') as delayed,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'delayed') / COUNT(*), 2) as delay_rate
FROM logistics_tracking
WHERE timestamp > NOW() - INTERVAL '90 days'
GROUP BY DATE(timestamp)
ORDER BY date;

-- 1.3 지연 시간 분석
-- @name: delay_duration_analysis
SELECT
    origin_port,
    dest_port,
    AVG(EXTRACT(EPOCH FROM (NOW() - timestamp)) / 3600)::INT as avg_hours_since_update,
    MAX(EXTRACT(EPOCH FROM (NOW() - timestamp)) / 3600)::INT as max_hours_since_update,
    COUNT(*) as stuck_shipments
FROM logistics_tracking
WHERE status IN ('delayed', 'in_transit')
  AND timestamp < NOW() - INTERVAL '24 hours'
GROUP BY origin_port, dest_port
ORDER BY stuck_shipments DESC;

-- ============================================
-- 2. 선박/컨테이너 추적
-- ============================================

-- 2.1 최근 선박 위치
-- @name: recent_vessel_positions
SELECT DISTINCT ON (vessel_name)
    vessel_name,
    imo_number,
    lat,
    lng,
    status,
    origin_port,
    dest_port,
    estimated_arrival,
    timestamp as last_update
FROM logistics_tracking
WHERE vessel_name IS NOT NULL
ORDER BY vessel_name, timestamp DESC;

-- 2.2 화물 유형별 통계
-- @name: cargo_type_stats
SELECT
    cargo_type,
    COUNT(DISTINCT shipment_id) as shipments,
    COUNT(DISTINCT vessel_name) as vessels,
    COUNT(*) FILTER (WHERE status = 'delivered') as delivered,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'delivered') / COUNT(*), 2) as delivery_rate
FROM logistics_tracking
WHERE timestamp > NOW() - INTERVAL '30 days'
  AND cargo_type IS NOT NULL
GROUP BY cargo_type
ORDER BY shipments DESC;

-- 2.3 항구별 활동량
-- @name: port_activity
WITH port_stats AS (
    SELECT
        origin_port as port,
        'outbound' as direction,
        COUNT(*) as shipments
    FROM logistics_tracking
    WHERE timestamp > NOW() - INTERVAL '30 days'
    GROUP BY origin_port
    UNION ALL
    SELECT
        dest_port as port,
        'inbound' as direction,
        COUNT(*) as shipments
    FROM logistics_tracking
    WHERE timestamp > NOW() - INTERVAL '30 days'
    GROUP BY dest_port
)
SELECT
    port,
    SUM(shipments) FILTER (WHERE direction = 'inbound') as inbound,
    SUM(shipments) FILTER (WHERE direction = 'outbound') as outbound,
    SUM(shipments) as total
FROM port_stats
WHERE port IS NOT NULL
GROUP BY port
ORDER BY total DESC;

-- ============================================
-- 3. 무역 통계 분석
-- ============================================

-- 3.1 국가별 무역 요약
-- @name: trade_by_country
SELECT
    reporter_name,
    SUM(trade_value) FILTER (WHERE flow_code = 'X') as exports,
    SUM(trade_value) FILTER (WHERE flow_code = 'M') as imports,
    SUM(trade_value) FILTER (WHERE flow_code = 'X') - SUM(trade_value) FILTER (WHERE flow_code = 'M') as trade_balance
FROM trade_statistics
WHERE period >= TO_CHAR(NOW() - INTERVAL '12 months', 'YYYYMM')
GROUP BY reporter_name
ORDER BY exports + imports DESC;

-- 3.2 상품별 무역 추이
-- @name: trade_by_commodity
SELECT
    commodity_code,
    commodity_desc,
    period,
    SUM(trade_value) as total_value,
    LAG(SUM(trade_value)) OVER (PARTITION BY commodity_code ORDER BY period) as prev_period,
    ROUND(100.0 * (SUM(trade_value) - LAG(SUM(trade_value)) OVER (PARTITION BY commodity_code ORDER BY period))
        / NULLIF(LAG(SUM(trade_value)) OVER (PARTITION BY commodity_code ORDER BY period), 0), 2) as change_pct
FROM trade_statistics
WHERE period >= TO_CHAR(NOW() - INTERVAL '12 months', 'YYYYMM')
GROUP BY commodity_code, commodity_desc, period
ORDER BY commodity_code, period;

-- 3.3 미중 무역 현황
-- @name: us_china_trade
SELECT
    period,
    reporter_name,
    partner_name,
    flow_code,
    SUM(trade_value) as total_value
FROM trade_statistics
WHERE (reporter_code = '842' AND partner_code = '156')
   OR (reporter_code = '156' AND partner_code = '842')
GROUP BY period, reporter_name, partner_name, flow_code
ORDER BY period DESC, reporter_name;

-- 3.4 월별 무역 트렌드
-- @name: monthly_trade_trend
SELECT
    period,
    SUM(trade_value) FILTER (WHERE flow_code = 'X') as total_exports,
    SUM(trade_value) FILTER (WHERE flow_code = 'M') as total_imports,
    COUNT(DISTINCT reporter_code) as countries
FROM trade_statistics
WHERE period >= TO_CHAR(NOW() - INTERVAL '24 months', 'YYYYMM')
GROUP BY period
ORDER BY period;

-- ============================================
-- 4. 운임 지수 분석
-- ============================================

-- 4.1 최신 운임 지수
-- @name: latest_freight_indices
SELECT DISTINCT ON (index_name, route)
    date,
    index_name,
    route,
    value,
    change_pct,
    unit
FROM freight_indices
ORDER BY index_name, route, date DESC;

-- 4.2 운임 지수 추이 (30일)
-- @name: freight_index_trend
SELECT
    date,
    index_name,
    route,
    value,
    AVG(value) OVER (
        PARTITION BY index_name, route
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7,
    AVG(value) OVER (
        PARTITION BY index_name, route
        ORDER BY date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as ma_30
FROM freight_indices
WHERE date > NOW() - INTERVAL '90 days'
ORDER BY index_name, route, date;

-- 4.3 운임 변동성
-- @name: freight_volatility
SELECT
    index_name,
    route,
    AVG(value) as avg_value,
    STDDEV(value) as std_dev,
    MIN(value) as min_value,
    MAX(value) as max_value,
    MAX(value) - MIN(value) as range
FROM freight_indices
WHERE date > NOW() - INTERVAL '90 days'
GROUP BY index_name, route
ORDER BY std_dev DESC;

-- 4.4 BDI vs FBX 비교
-- @name: bdi_fbx_comparison
SELECT
    f1.date,
    f1.value as bdi,
    f2.value as fbx_asia_uswc,
    CORR(f1.value, f2.value) OVER (
        ORDER BY f1.date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as rolling_correlation
FROM freight_indices f1
JOIN freight_indices f2
    ON f1.date = f2.date
    AND f2.index_name = 'FBX'
    AND f2.route LIKE '%West Coast%'
WHERE f1.index_name = 'BDI'
ORDER BY f1.date;

-- ============================================
-- 5. 통합 분석 쿼리
-- ============================================

-- 5.1 물류 지연과 운임 상관관계
-- @name: delay_freight_correlation
WITH daily_delays AS (
    SELECT
        DATE(timestamp) as date,
        ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'delayed') / COUNT(*), 2) as delay_rate
    FROM logistics_tracking
    GROUP BY DATE(timestamp)
),
daily_freight AS (
    SELECT
        date,
        AVG(value) as avg_freight
    FROM freight_indices
    WHERE index_name = 'FBX'
    GROUP BY date
)
SELECT
    d.date,
    d.delay_rate,
    f.avg_freight,
    CORR(d.delay_rate, f.avg_freight) OVER (
        ORDER BY d.date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as correlation_30d
FROM daily_delays d
JOIN daily_freight f ON d.date = f.date
ORDER BY d.date;

-- 5.2 무역량과 물류 활동 비교
-- @name: trade_logistics_comparison
WITH monthly_trade AS (
    SELECT
        period,
        SUM(trade_value) as total_trade
    FROM trade_statistics
    GROUP BY period
),
monthly_logistics AS (
    SELECT
        TO_CHAR(timestamp, 'YYYYMM') as period,
        COUNT(*) as shipments
    FROM logistics_tracking
    GROUP BY TO_CHAR(timestamp, 'YYYYMM')
)
SELECT
    t.period,
    t.total_trade,
    l.shipments,
    ROUND(t.total_trade / NULLIF(l.shipments, 0), 2) as value_per_shipment
FROM monthly_trade t
JOIN monthly_logistics l ON t.period = l.period
ORDER BY t.period;

-- ============================================
-- 6. 데이터 품질 검사
-- ============================================

-- 6.1 데이터 수집 현황
-- @name: data_collection_status
SELECT
    'logistics_tracking' as table_name,
    COUNT(*) as total_rows,
    COUNT(DISTINCT shipment_id) as unique_shipments,
    MIN(timestamp) as earliest,
    MAX(timestamp) as latest,
    COUNT(*) FILTER (WHERE timestamp > NOW() - INTERVAL '24 hours') as last_24h
FROM logistics_tracking
UNION ALL
SELECT
    'trade_statistics',
    COUNT(*),
    COUNT(DISTINCT period || reporter_code || partner_code),
    MIN(created_at),
    MAX(created_at),
    COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '24 hours')
FROM trade_statistics
UNION ALL
SELECT
    'freight_indices',
    COUNT(*),
    COUNT(DISTINCT date || index_name || route),
    MIN(date)::timestamp,
    MAX(date)::timestamp,
    COUNT(*) FILTER (WHERE date > NOW() - INTERVAL '24 hours')
FROM freight_indices;

-- 6.2 결측값 검사
-- @name: missing_data_check
SELECT
    'logistics_tracking' as table_name,
    COUNT(*) FILTER (WHERE origin_port IS NULL) as null_origin,
    COUNT(*) FILTER (WHERE dest_port IS NULL) as null_dest,
    COUNT(*) FILTER (WHERE status IS NULL) as null_status,
    COUNT(*) as total
FROM logistics_tracking
UNION ALL
SELECT
    'trade_statistics',
    COUNT(*) FILTER (WHERE reporter_code IS NULL),
    COUNT(*) FILTER (WHERE partner_code IS NULL),
    COUNT(*) FILTER (WHERE trade_value IS NULL),
    COUNT(*)
FROM trade_statistics;
