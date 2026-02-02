-- SQL Trading Module Schema
-- Version: 1.0
-- Database: PostgreSQL (claude_mcp)
-- Created: 2026-02-02

-- ============================================
-- 대체 데이터 테이블 (Alternative Data)
-- ============================================

-- 위성 데이터 (Satellite Data)
CREATE TABLE IF NOT EXISTS satellite_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    location_code VARCHAR(50),
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6),
    sensor VARCHAR(50),        -- sentinel-2, landsat-8, modis
    band VARCHAR(20),          -- B02, B03, B04, B08 등
    value DECIMAL(15, 6),
    ndvi DECIMAL(5, 4),        -- 정규 식생 지수 (-1 ~ 1)
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 물류 추적 (Logistics Tracking)
CREATE TABLE IF NOT EXISTS logistics_tracking (
    id SERIAL PRIMARY KEY,
    shipment_id VARCHAR(100) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6),
    status VARCHAR(50),        -- in_transit, delivered, delayed, at_port
    carrier VARCHAR(100),
    origin_port VARCHAR(100),
    dest_port VARCHAR(100),
    cargo_type VARCHAR(100),   -- container, bulk, tanker
    vessel_name VARCHAR(200),
    imo_number VARCHAR(20),    -- IMO 선박 번호
    estimated_arrival TIMESTAMPTZ,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 지리 활동 (Geo Activity)
CREATE TABLE IF NOT EXISTS geo_activity (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    region_code VARCHAR(50),
    activity_type VARCHAR(50), -- parking, traffic, construction, retail
    intensity DECIMAL(10, 4),  -- 활동 강도 (0-100)
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6),
    source VARCHAR(100),       -- google_maps, osm, satellite
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 트레이딩 데이터 테이블 (Trading Data)
-- ============================================

-- 시장 스냅샷 (Market Snapshots)
CREATE TABLE IF NOT EXISTS market_snapshots (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(15, 6),
    open_price DECIMAL(15, 6),
    high_price DECIMAL(15, 6),
    low_price DECIMAL(15, 6),
    close_price DECIMAL(15, 6),
    change_pct DECIMAL(10, 4),
    volume BIGINT,
    source VARCHAR(50),        -- yahoo, alpha_vantage, binance
    asset_type VARCHAR(20),    -- stock, crypto, forex, commodity
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 경제 지표 (Economic Indicators)
CREATE TABLE IF NOT EXISTS economic_indicators (
    id SERIAL PRIMARY KEY,
    series_id VARCHAR(50) NOT NULL,    -- FRED 시리즈 ID 등
    indicator_name VARCHAR(200),
    date DATE NOT NULL,
    value DECIMAL(20, 6),
    previous_value DECIMAL(20, 6),
    change_pct DECIMAL(10, 4),
    category VARCHAR(50),              -- employment, inflation, gdp, trade
    country VARCHAR(10) DEFAULT 'US',
    importance VARCHAR(20),            -- high, medium, low
    source VARCHAR(50),                -- fred, bls, census
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(series_id, date)
);

-- 트레이딩 신호 (Trading Signals)
CREATE TABLE IF NOT EXISTS trading_signals (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20),
    signal_type VARCHAR(20),   -- BUY, SELL, HOLD, STRONG_BUY, STRONG_SELL
    confidence DECIMAL(5, 4),  -- 신뢰도 (0-1)
    price DECIMAL(15, 6),
    target_price DECIMAL(15, 6),
    stop_loss DECIMAL(15, 6),
    strategy VARCHAR(50),      -- momentum, mean_reversion, satellite_alpha
    timeframe VARCHAR(20),     -- 1d, 1w, 1m
    indicators JSONB,          -- 사용된 지표들
    reason TEXT,               -- 신호 생성 이유
    alt_data_source VARCHAR(50), -- 대체 데이터 소스 (있는 경우)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 무역 데이터 테이블 (Trade Statistics)
-- ============================================

-- UN Comtrade 무역 데이터
CREATE TABLE IF NOT EXISTS trade_statistics (
    id SERIAL PRIMARY KEY,
    period VARCHAR(10) NOT NULL,       -- YYYYMM 형식
    reporter_code VARCHAR(10),
    reporter_name VARCHAR(100),
    partner_code VARCHAR(10),
    partner_name VARCHAR(100),
    flow_code VARCHAR(10),             -- M (import), X (export)
    commodity_code VARCHAR(20),        -- HS 코드
    commodity_desc TEXT,
    trade_value DECIMAL(20, 2),        -- USD
    net_weight DECIMAL(20, 2),         -- kg
    qty DECIMAL(20, 2),
    qty_unit VARCHAR(50),
    source VARCHAR(50) DEFAULT 'UN_COMTRADE',
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 운임 지수 (Freight Indices)
CREATE TABLE IF NOT EXISTS freight_indices (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    index_name VARCHAR(100),           -- BDI, FBX, SCFI
    route VARCHAR(100),                -- China-USWC, Asia-Europe
    value DECIMAL(15, 4),
    change_pct DECIMAL(10, 4),
    unit VARCHAR(20),                  -- points, USD/FEU
    source VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(date, index_name, route)
);

-- ============================================
-- 인덱스 (Indexes)
-- ============================================

-- 위성 데이터 인덱스
CREATE INDEX IF NOT EXISTS idx_satellite_timestamp ON satellite_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_satellite_location ON satellite_data(location_code);
CREATE INDEX IF NOT EXISTS idx_satellite_sensor ON satellite_data(sensor);

-- 물류 추적 인덱스
CREATE INDEX IF NOT EXISTS idx_logistics_shipment ON logistics_tracking(shipment_id);
CREATE INDEX IF NOT EXISTS idx_logistics_timestamp ON logistics_tracking(timestamp);
CREATE INDEX IF NOT EXISTS idx_logistics_status ON logistics_tracking(status);
CREATE INDEX IF NOT EXISTS idx_logistics_ports ON logistics_tracking(origin_port, dest_port);

-- 지리 활동 인덱스
CREATE INDEX IF NOT EXISTS idx_geo_region ON geo_activity(region_code);
CREATE INDEX IF NOT EXISTS idx_geo_timestamp ON geo_activity(timestamp);
CREATE INDEX IF NOT EXISTS idx_geo_type ON geo_activity(activity_type);

-- 시장 스냅샷 인덱스
CREATE INDEX IF NOT EXISTS idx_market_symbol ON market_snapshots(symbol, timestamp);
CREATE INDEX IF NOT EXISTS idx_market_timestamp ON market_snapshots(timestamp);
CREATE INDEX IF NOT EXISTS idx_market_asset_type ON market_snapshots(asset_type);

-- 경제 지표 인덱스
CREATE INDEX IF NOT EXISTS idx_indicators_series ON economic_indicators(series_id, date);
CREATE INDEX IF NOT EXISTS idx_indicators_category ON economic_indicators(category);
CREATE INDEX IF NOT EXISTS idx_indicators_date ON economic_indicators(date);

-- 트레이딩 신호 인덱스
CREATE INDEX IF NOT EXISTS idx_signals_symbol ON trading_signals(symbol, timestamp);
CREATE INDEX IF NOT EXISTS idx_signals_type ON trading_signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_signals_strategy ON trading_signals(strategy);

-- 무역 데이터 인덱스
CREATE INDEX IF NOT EXISTS idx_trade_period ON trade_statistics(period);
CREATE INDEX IF NOT EXISTS idx_trade_reporter ON trade_statistics(reporter_code);
CREATE INDEX IF NOT EXISTS idx_trade_commodity ON trade_statistics(commodity_code);

-- 운임 지수 인덱스
CREATE INDEX IF NOT EXISTS idx_freight_date ON freight_indices(date);
CREATE INDEX IF NOT EXISTS idx_freight_name ON freight_indices(index_name);

-- ============================================
-- 뷰 (Views)
-- ============================================

-- 최신 시장 데이터 뷰
CREATE OR REPLACE VIEW v_latest_market AS
SELECT DISTINCT ON (symbol)
    symbol,
    timestamp,
    price,
    change_pct,
    volume,
    asset_type,
    source
FROM market_snapshots
ORDER BY symbol, timestamp DESC;

-- 최신 트레이딩 신호 뷰
CREATE OR REPLACE VIEW v_latest_signals AS
SELECT DISTINCT ON (symbol)
    symbol,
    timestamp,
    signal_type,
    confidence,
    price,
    strategy,
    reason
FROM trading_signals
ORDER BY symbol, timestamp DESC;

-- 물류 지연 현황 뷰
CREATE OR REPLACE VIEW v_logistics_delays AS
SELECT
    origin_port,
    dest_port,
    COUNT(*) as total_shipments,
    COUNT(*) FILTER (WHERE status = 'delayed') as delayed_count,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'delayed') / COUNT(*), 2) as delay_rate
FROM logistics_tracking
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY origin_port, dest_port
ORDER BY delayed_count DESC;

-- 최신 경제 지표 뷰
CREATE OR REPLACE VIEW v_latest_indicators AS
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

-- ============================================
-- 코멘트 (Comments)
-- ============================================

COMMENT ON TABLE satellite_data IS '위성 이미지 데이터 - NDVI, 변화 감지 등';
COMMENT ON TABLE logistics_tracking IS '물류/선박 추적 데이터';
COMMENT ON TABLE geo_activity IS '지리 활동 데이터 - 주차장, 교통량 등';
COMMENT ON TABLE market_snapshots IS '시장 가격 스냅샷';
COMMENT ON TABLE economic_indicators IS '경제 지표 데이터 (FRED 등)';
COMMENT ON TABLE trading_signals IS '트레이딩 신호 및 알림';
COMMENT ON TABLE trade_statistics IS 'UN Comtrade 국제 무역 통계';
COMMENT ON TABLE freight_indices IS '운임 지수 (BDI, FBX 등)';
