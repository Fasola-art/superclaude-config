-- ============================================
-- 시장 분석 쿼리 (Market Analysis Queries)
-- ============================================
-- Module: sql-trading
-- Version: 1.0
-- ============================================

-- ============================================
-- 1. 시장 현황 조회
-- ============================================

-- 1.1 최신 시장 데이터
-- @name: latest_market_data
SELECT DISTINCT ON (symbol)
    symbol,
    timestamp,
    price,
    open_price,
    high_price,
    low_price,
    close_price,
    change_pct,
    volume,
    asset_type,
    source
FROM market_snapshots
ORDER BY symbol, timestamp DESC;

-- 1.2 자산 유형별 요약
-- @name: market_summary_by_type
SELECT
    asset_type,
    COUNT(DISTINCT symbol) as symbols,
    AVG(change_pct) as avg_change_pct,
    MIN(change_pct) as min_change_pct,
    MAX(change_pct) as max_change_pct,
    SUM(volume) as total_volume
FROM (
    SELECT DISTINCT ON (symbol)
        symbol, change_pct, volume, asset_type
    FROM market_snapshots
    WHERE timestamp > NOW() - INTERVAL '24 hours'
    ORDER BY symbol, timestamp DESC
) latest
GROUP BY asset_type;

-- 1.3 상위/하위 변동 종목
-- @name: top_movers
WITH latest AS (
    SELECT DISTINCT ON (symbol)
        symbol, price, change_pct, volume, asset_type, timestamp
    FROM market_snapshots
    WHERE timestamp > NOW() - INTERVAL '24 hours'
    ORDER BY symbol, timestamp DESC
)
(
    SELECT 'TOP_GAINER' as category, symbol, price, change_pct, volume
    FROM latest
    ORDER BY change_pct DESC
    LIMIT 10
)
UNION ALL
(
    SELECT 'TOP_LOSER', symbol, price, change_pct, volume
    FROM latest
    ORDER BY change_pct ASC
    LIMIT 10
);

-- ============================================
-- 2. 가격 분석
-- ============================================

-- 2.1 가격 이동평균
-- @name: price_moving_averages
SELECT
    timestamp,
    symbol,
    price,
    AVG(price) OVER (
        PARTITION BY symbol
        ORDER BY timestamp
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) as ma_5,
    AVG(price) OVER (
        PARTITION BY symbol
        ORDER BY timestamp
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    ) as ma_20,
    AVG(price) OVER (
        PARTITION BY symbol
        ORDER BY timestamp
        ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
    ) as ma_50
FROM market_snapshots
WHERE symbol = $1  -- 파라미터: 심볼
  AND timestamp > NOW() - INTERVAL '90 days'
ORDER BY timestamp;

-- 2.2 변동성 분석 (표준편차)
-- @name: volatility_analysis
SELECT
    symbol,
    COUNT(*) as data_points,
    AVG(price) as avg_price,
    STDDEV(price) as price_stddev,
    STDDEV(price) / AVG(price) * 100 as volatility_pct,
    AVG(change_pct) as avg_daily_change,
    STDDEV(change_pct) as daily_change_stddev
FROM market_snapshots
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY symbol
ORDER BY volatility_pct DESC;

-- 2.3 가격 분포 (백분위수)
-- @name: price_distribution
SELECT
    symbol,
    PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY price) as p10,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) as p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price) as median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) as p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY price) as p90,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM market_snapshots
WHERE timestamp > NOW() - INTERVAL '90 days'
GROUP BY symbol;

-- ============================================
-- 3. 거래량 분석
-- ============================================

-- 3.1 거래량 추이
-- @name: volume_trend
SELECT
    DATE(timestamp) as date,
    symbol,
    SUM(volume) as daily_volume,
    AVG(SUM(volume)) OVER (
        PARTITION BY symbol
        ORDER BY DATE(timestamp)
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    ) as volume_ma_20
FROM market_snapshots
WHERE timestamp > NOW() - INTERVAL '60 days'
GROUP BY DATE(timestamp), symbol
ORDER BY symbol, date;

-- 3.2 거래량 이상 감지
-- @name: volume_anomalies
WITH daily_volume AS (
    SELECT
        DATE(timestamp) as date,
        symbol,
        SUM(volume) as volume
    FROM market_snapshots
    WHERE timestamp > NOW() - INTERVAL '90 days'
    GROUP BY DATE(timestamp), symbol
),
volume_stats AS (
    SELECT
        symbol,
        AVG(volume) as avg_volume,
        STDDEV(volume) as stddev_volume
    FROM daily_volume
    GROUP BY symbol
)
SELECT
    dv.date,
    dv.symbol,
    dv.volume,
    vs.avg_volume,
    ROUND((dv.volume - vs.avg_volume) / NULLIF(vs.stddev_volume, 0), 2) as z_score
FROM daily_volume dv
JOIN volume_stats vs ON dv.symbol = vs.symbol
WHERE ABS((dv.volume - vs.avg_volume) / NULLIF(vs.stddev_volume, 0)) > 2
ORDER BY dv.date DESC, ABS((dv.volume - vs.avg_volume) / NULLIF(vs.stddev_volume, 0)) DESC;

-- ============================================
-- 4. 경제 지표 분석
-- ============================================

-- 4.1 최신 경제 지표
-- @name: latest_indicators
SELECT DISTINCT ON (series_id)
    series_id,
    indicator_name,
    date,
    value,
    previous_value,
    change_pct,
    category,
    importance
FROM economic_indicators
ORDER BY series_id, date DESC;

-- 4.2 카테고리별 지표 현황
-- @name: indicators_by_category
SELECT
    category,
    COUNT(DISTINCT series_id) as indicator_count,
    COUNT(*) FILTER (WHERE importance = 'high') as high_importance,
    AVG(change_pct) as avg_change
FROM (
    SELECT DISTINCT ON (series_id)
        series_id, category, importance, change_pct
    FROM economic_indicators
    ORDER BY series_id, date DESC
) latest
GROUP BY category;

-- 4.3 경제 지표 추이
-- @name: indicator_trend
SELECT
    date,
    series_id,
    indicator_name,
    value,
    LAG(value, 1) OVER (PARTITION BY series_id ORDER BY date) as prev_value,
    LAG(value, 12) OVER (PARTITION BY series_id ORDER BY date) as value_1y_ago,
    ROUND(100.0 * (value - LAG(value, 12) OVER (PARTITION BY series_id ORDER BY date))
        / NULLIF(LAG(value, 12) OVER (PARTITION BY series_id ORDER BY date), 0), 2) as yoy_change
FROM economic_indicators
WHERE series_id = $1  -- 파라미터: 시리즈 ID
ORDER BY date;

-- ============================================
-- 5. 트레이딩 신호 분석
-- ============================================

-- 5.1 최신 신호
-- @name: latest_signals
SELECT DISTINCT ON (symbol)
    symbol,
    timestamp,
    signal_type,
    confidence,
    price,
    target_price,
    stop_loss,
    strategy,
    reason,
    alt_data_source
FROM trading_signals
ORDER BY symbol, timestamp DESC;

-- 5.2 신호 유형별 통계
-- @name: signal_stats_by_type
SELECT
    signal_type,
    COUNT(*) as signal_count,
    AVG(confidence) as avg_confidence,
    COUNT(DISTINCT symbol) as symbols_affected,
    COUNT(DISTINCT strategy) as strategies_used
FROM trading_signals
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY signal_type
ORDER BY signal_count DESC;

-- 5.3 전략별 신호 성과 (백테스팅용)
-- @name: strategy_performance
WITH signal_outcomes AS (
    SELECT
        ts.id,
        ts.symbol,
        ts.signal_type,
        ts.price as signal_price,
        ts.strategy,
        ts.timestamp as signal_time,
        ms.price as current_price,
        ms.timestamp as price_time,
        CASE
            WHEN ts.signal_type = 'BUY' THEN (ms.price - ts.price) / ts.price * 100
            WHEN ts.signal_type = 'SELL' THEN (ts.price - ms.price) / ts.price * 100
            ELSE 0
        END as return_pct
    FROM trading_signals ts
    LEFT JOIN LATERAL (
        SELECT price, timestamp
        FROM market_snapshots
        WHERE symbol = ts.symbol
          AND timestamp > ts.timestamp
        ORDER BY timestamp
        LIMIT 1
    ) ms ON true
    WHERE ts.timestamp > NOW() - INTERVAL '30 days'
)
SELECT
    strategy,
    signal_type,
    COUNT(*) as signals,
    AVG(return_pct) as avg_return,
    COUNT(*) FILTER (WHERE return_pct > 0) as winning,
    ROUND(100.0 * COUNT(*) FILTER (WHERE return_pct > 0) / COUNT(*), 2) as win_rate
FROM signal_outcomes
GROUP BY strategy, signal_type
ORDER BY avg_return DESC;

-- 5.4 대체 데이터 기반 신호
-- @name: alt_data_signals
SELECT
    alt_data_source,
    signal_type,
    COUNT(*) as signals,
    AVG(confidence) as avg_confidence,
    STRING_AGG(DISTINCT symbol, ', ') as symbols
FROM trading_signals
WHERE alt_data_source IS NOT NULL
  AND timestamp > NOW() - INTERVAL '30 days'
GROUP BY alt_data_source, signal_type
ORDER BY signals DESC;

-- ============================================
-- 6. 상관관계 분석
-- ============================================

-- 6.1 자산간 상관관계 (일별 수익률)
-- @name: asset_correlation
WITH daily_returns AS (
    SELECT
        DATE(timestamp) as date,
        symbol,
        (price - LAG(price) OVER (PARTITION BY symbol ORDER BY timestamp)) / LAG(price) OVER (PARTITION BY symbol ORDER BY timestamp) as daily_return
    FROM market_snapshots
    WHERE timestamp > NOW() - INTERVAL '90 days'
)
SELECT
    a.symbol as symbol_a,
    b.symbol as symbol_b,
    CORR(a.daily_return, b.daily_return) as correlation
FROM daily_returns a
JOIN daily_returns b ON a.date = b.date AND a.symbol < b.symbol
WHERE a.daily_return IS NOT NULL AND b.daily_return IS NOT NULL
GROUP BY a.symbol, b.symbol
HAVING COUNT(*) >= 30
ORDER BY ABS(CORR(a.daily_return, b.daily_return)) DESC;

-- 6.2 시장과 개별 종목 베타
-- @name: beta_calculation
WITH market_returns AS (
    SELECT
        DATE(timestamp) as date,
        AVG((price - LAG(price) OVER (PARTITION BY symbol ORDER BY timestamp)) / LAG(price) OVER (PARTITION BY symbol ORDER BY timestamp)) as market_return
    FROM market_snapshots
    WHERE asset_type = 'stock'
      AND timestamp > NOW() - INTERVAL '90 days'
    GROUP BY DATE(timestamp)
),
stock_returns AS (
    SELECT
        DATE(timestamp) as date,
        symbol,
        (price - LAG(price) OVER (PARTITION BY symbol ORDER BY timestamp)) / LAG(price) OVER (PARTITION BY symbol ORDER BY timestamp) as stock_return
    FROM market_snapshots
    WHERE timestamp > NOW() - INTERVAL '90 days'
)
SELECT
    sr.symbol,
    COVAR_POP(sr.stock_return, mr.market_return) / VAR_POP(mr.market_return) as beta,
    CORR(sr.stock_return, mr.market_return) as correlation
FROM stock_returns sr
JOIN market_returns mr ON sr.date = mr.date
WHERE sr.stock_return IS NOT NULL AND mr.market_return IS NOT NULL
GROUP BY sr.symbol
HAVING COUNT(*) >= 30
ORDER BY beta DESC;

-- ============================================
-- 7. 복합 분석 (대체 데이터 연동)
-- ============================================

-- 7.1 물류 지연과 섹터 영향
-- @name: logistics_sector_impact
WITH delay_trend AS (
    SELECT
        DATE(timestamp) as date,
        ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'delayed') / COUNT(*), 2) as delay_rate
    FROM logistics_tracking
    WHERE timestamp > NOW() - INTERVAL '90 days'
    GROUP BY DATE(timestamp)
),
sector_returns AS (
    SELECT
        DATE(timestamp) as date,
        metadata->>'sector' as sector,
        AVG(change_pct) as avg_return
    FROM market_snapshots
    WHERE timestamp > NOW() - INTERVAL '90 days'
      AND metadata->>'sector' IS NOT NULL
    GROUP BY DATE(timestamp), metadata->>'sector'
)
SELECT
    sr.sector,
    CORR(dt.delay_rate, sr.avg_return) as correlation_with_delays,
    COUNT(*) as data_points
FROM delay_trend dt
JOIN sector_returns sr ON dt.date = sr.date
GROUP BY sr.sector
HAVING COUNT(*) >= 30
ORDER BY ABS(CORR(dt.delay_rate, sr.avg_return)) DESC;

-- 7.2 운임과 해운주 상관관계
-- @name: freight_shipping_correlation
WITH freight_data AS (
    SELECT
        date,
        AVG(value) as avg_freight
    FROM freight_indices
    WHERE index_name IN ('BDI', 'FBX')
    GROUP BY date
),
shipping_returns AS (
    SELECT
        DATE(timestamp) as date,
        symbol,
        price,
        change_pct
    FROM market_snapshots
    WHERE symbol IN ('SBLK', 'GOGL', 'DSX', 'ZIM', 'MATX')  -- 해운주
)
SELECT
    sr.symbol,
    CORR(fd.avg_freight, sr.price) as price_correlation,
    CORR(fd.avg_freight, sr.change_pct) as return_correlation,
    COUNT(*) as data_points
FROM freight_data fd
JOIN shipping_returns sr ON fd.date = sr.date
GROUP BY sr.symbol
ORDER BY price_correlation DESC;
