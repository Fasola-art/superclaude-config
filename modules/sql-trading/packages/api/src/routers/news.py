"""뉴스 API 라우터"""
from fastapi import APIRouter, Query
from db import fetch_all

router = APIRouter()

# 프론트엔드 → DB 카테고리 매핑 (호환성)
CATEGORY_MAP = {"macro": "economy", "commodities": "commodities"}

COLS = """title, summary, url, source, category,
       sentiment, symbols, timestamp, metadata"""


@router.get("/")
def get_news(
    category: str | None = Query(None, description="all, stocks, crypto, economy, realestate"),
    limit: int = Query(20, le=50),
):
    """시장 뉴스 (category='all' 또는 미지정 시 전체 반환)"""
    if category and category != "all":
        db_cat = CATEGORY_MAP.get(category, category)
        rows = fetch_all(f"""
            SELECT {COLS} FROM market_news
            WHERE category = %s
            ORDER BY timestamp DESC LIMIT %s
        """, (db_cat, limit))
    else:
        rows = fetch_all(f"""
            SELECT {COLS} FROM market_news
            ORDER BY timestamp DESC LIMIT %s
        """, (limit,))
    return rows
