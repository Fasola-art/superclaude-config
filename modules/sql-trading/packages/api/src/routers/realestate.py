"""부동산 API 라우터"""
from fastapi import APIRouter
from db import fetch_all

router = APIRouter()


@router.get("/indices")
async def get_indices():
    """매매/전세 지수"""
    rows = fetch_all("""
        SELECT DISTINCT ON (region, index_type)
            region, index_type, index_value, change_pct, date
        FROM realestate_indices
        ORDER BY region, index_type, date DESC
    """)
    return rows


@router.get("/rates")
async def get_rates():
    """기준금리/주담대 금리"""
    rows = fetch_all("""
        SELECT DISTINCT ON (rate_type)
            rate_type, rate_value, date, country
        FROM interest_rates
        ORDER BY rate_type, date DESC
    """)
    return rows


@router.get("/regions")
async def get_by_region():
    """지역별 부동산 시세"""
    rows = fetch_all("""
        SELECT region,
            MAX(CASE WHEN index_type = 'sale' THEN index_value END) as sale_index,
            MAX(CASE WHEN index_type = 'jeonse' THEN index_value END) as jeonse_index,
            MAX(CASE WHEN index_type = 'sale' THEN change_pct END) as sale_change,
            MAX(CASE WHEN index_type = 'jeonse' THEN change_pct END) as jeonse_change
        FROM realestate_indices
        WHERE date = (SELECT MAX(date) FROM realestate_indices)
        GROUP BY region
        ORDER BY region
    """)
    return rows
