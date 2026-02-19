"""주식 API 라우터"""
from fastapi import APIRouter
from db import fetch_all

router = APIRouter()


@router.get("/indices")
def get_indices():
    """글로벌 주요 지수 (8개)"""
    indices = ["^GSPC", "^IXIC", "^DJI", "^KS11", "^KQ11", "^N225", "000001.SS", "^STOXX50E"]
    placeholders = ",".join([f"'{s}'" for s in indices])
    rows = fetch_all(f"""
        SELECT DISTINCT ON (symbol)
            symbol, price, change_pct, volume, timestamp,
            metadata->>'name' as name
        FROM market_snapshots
        WHERE symbol IN ({placeholders})
        ORDER BY symbol, timestamp DESC
    """)
    return rows


@router.get("/top-movers")
def get_top_movers():
    """등락 상위 종목"""
    rows = fetch_all("""
        SELECT DISTINCT ON (symbol)
            symbol, price, change_pct, volume,
            metadata->>'name' as name,
            metadata->>'sector' as sector
        FROM market_snapshots
        WHERE timestamp > NOW() - INTERVAL '3 hours'
          AND asset_type = 'stock'
        ORDER BY symbol, timestamp DESC
    """)
    sorted_rows = sorted(rows, key=lambda r: abs(float(r.get("change_pct") or 0)), reverse=True)
    return sorted_rows[:20]


@router.get("/sectors")
def get_sectors():
    """섹터별 현황"""
    rows = fetch_all("""
        SELECT
            metadata->>'sector' as sector,
            ROUND(AVG(change_pct)::numeric, 2) as avg_change,
            COUNT(DISTINCT symbol) as count
        FROM market_snapshots
        WHERE timestamp > NOW() - INTERVAL '3 hours'
          AND metadata->>'sector' IS NOT NULL
        GROUP BY metadata->>'sector'
        ORDER BY AVG(change_pct) DESC
    """)
    return rows


@router.get("/quotes")
def get_quotes(symbols: str):
    """심볼별 최신 시세"""
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    if not symbol_list:
        return []
    rows = fetch_all("""
        SELECT DISTINCT ON (symbol)
            symbol, price, change_pct, volume, timestamp,
            metadata->>'name' as name
        FROM market_snapshots
        WHERE symbol = ANY(%s)
        ORDER BY symbol, timestamp DESC
    """, (symbol_list,))
    return rows
