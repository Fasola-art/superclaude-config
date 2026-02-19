"""원자재/물류 API 라우터 (기존 데이터 활용)"""
from fastapi import APIRouter
from db import fetch_all

router = APIRouter()


@router.get("/freight")
def get_freight():
    """운임 지수"""
    rows = fetch_all("""
        SELECT DISTINCT ON (index_name, route)
            index_name, route, value, change_pct, date
        FROM freight_indices
        ORDER BY index_name, route, date DESC
    """)
    return rows


@router.get("/oil")
def get_oil_prices():
    """유가 (WTI, Brent)"""
    rows = fetch_all("""
        SELECT DISTINCT ON (series_id)
            series_id, indicator_name, value, change_pct, date
        FROM economic_indicators
        WHERE series_id IN ('DCOILWTICO', 'DCOILBRENTEU')
        ORDER BY series_id, date DESC
    """)
    return rows


@router.get("/logistics")
def get_logistics():
    """물류 추적"""
    rows = fetch_all("""
        SELECT DISTINCT ON (shipment_id)
            shipment_id, lat, lng, status, origin_port, dest_port,
            vessel_name, cargo_type, timestamp, estimated_arrival
        FROM logistics_tracking
        WHERE timestamp > NOW() - INTERVAL '30 days'
        ORDER BY shipment_id, timestamp DESC
        LIMIT 30
    """)
    return rows


@router.get("/trade")
def get_trade_stats():
    """무역 통계"""
    rows = fetch_all("""
        SELECT
            period, reporter_name, partner_name,
            flow_code, commodity_desc,
            trade_value, net_weight
        FROM trade_statistics
        ORDER BY period DESC, trade_value DESC
        LIMIT 50
    """)
    return rows
