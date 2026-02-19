"""포트폴리오 API 라우터"""
from fastapi import APIRouter
from pydantic import BaseModel
from db import fetch_all, execute

router = APIRouter()


class PortfolioItem(BaseModel):
    """포트폴리오 아이템"""
    symbol: str
    asset_type: str
    quantity: float
    avg_price: float
    currency: str = "KRW"


@router.get("/")
def get_portfolio():
    """포트폴리오 현황"""
    rows = fetch_all("""
        SELECT symbol, asset_type, quantity, avg_price,
               current_price, currency, metadata
        FROM portfolio_items
        ORDER BY symbol
    """)
    return rows


@router.post("/")
def add_item(item: PortfolioItem):
    """포트폴리오 아이템 추가"""
    execute("""
        INSERT INTO portfolio_items (symbol, asset_type, quantity, avg_price, currency)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (symbol) DO UPDATE SET
            quantity = EXCLUDED.quantity,
            avg_price = EXCLUDED.avg_price,
            updated_at = NOW()
    """, (item.symbol, item.asset_type, item.quantity, item.avg_price, item.currency))
    return {"status": "ok"}
