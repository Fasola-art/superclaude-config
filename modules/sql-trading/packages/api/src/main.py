"""
마켓브리핑 API 서버

FastAPI + psycopg2 커넥션 풀
"""
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db import close_pool
from routers import stocks, crypto, realestate, commodities, signals, news, portfolio, fx


@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 시작/종료 이벤트"""
    yield
    close_pool()


app = FastAPI(
    title="마켓브리핑 API",
    version="2.0.0",
    lifespan=lifespan,
)


@app.exception_handler(HTTPException)
def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"message": exc.detail, "type": "http_error"}},
    )


@app.exception_handler(Exception)
def unhandled_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": {"message": "Internal Server Error", "type": "server_error"}},
    )

# CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080")
allow_origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static 파일
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# 라우터 등록
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(crypto.router, prefix="/api/crypto", tags=["crypto"])
app.include_router(realestate.router, prefix="/api/realestate", tags=["realestate"])
app.include_router(commodities.router, prefix="/api/commodities", tags=["commodities"])
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(fx.router, prefix="/api/fx", tags=["fx"])


@app.get("/api/summary")
def get_summary():
    """전체 시장 요약"""
    from db import fetch_one, fetch_all

    count = fetch_one("SELECT COUNT(*) as cnt FROM market_snapshots WHERE timestamp > NOW() - INTERVAL '24 hours'")
    total_records = count["cnt"] if count else 0

    signal_rows = fetch_all("""
        SELECT signal_type, COUNT(*) as cnt
        FROM trading_signals
        WHERE timestamp > NOW() - INTERVAL '24 hours'
        GROUP BY signal_type
    """)
    sigs = {r["signal_type"]: r["cnt"] for r in signal_rows}

    latest = fetch_one("SELECT MAX(timestamp) as ts FROM market_snapshots")

    return {
        "total_records": total_records,
        "buy_signals": sigs.get("BUY", 0) + sigs.get("STRONG_BUY", 0),
        "sell_signals": sigs.get("SELL", 0) + sigs.get("STRONG_SELL", 0),
        "last_update": latest["ts"] if latest else None,
        "server_time": datetime.now().isoformat(),
    }


@app.get("/api/summary/detail")
async def get_summary_detail():
    """테이블별 데이터 현황 상세"""
    from db import fetch_all
    tables = [
        ("market_snapshots", "시장 스냅샷", "24 hours", "timestamp"),
        ("trading_signals", "트레이딩 신호", "24 hours", "timestamp"),
        ("market_news", "시장 뉴스", "24 hours", "timestamp"),
        ("crypto_prices", "암호화폐 시세", "24 hours", "timestamp"),
        ("interest_rates", "금리 데이터", "7 days", "date"),
        ("freight_indices", "운임 지수", "30 days", "date"),
        ("economic_indicators", "경제 지표", "30 days", "date"),
    ]
    result = []
    for table, label, interval, col in tables:
        rows = fetch_all(f"""
            SELECT COUNT(*) as cnt,
                   MAX({col}) as latest
            FROM {table}
            WHERE {col} > NOW() - INTERVAL '{interval}'
        """)
        r = rows[0] if rows else {"cnt": 0, "latest": None}
        result.append({"table": table, "label": label, "count": r["cnt"], "latest": r["latest"]})
    return result


if __name__ == "__main__":
    import uvicorn
    print("🚀 마켓브리핑 API Server")
    print("📊 Dashboard: http://localhost:8080")
    print("📡 API Docs: http://localhost:8080/docs")
    uvicorn.run(app, host="0.0.0.0", port=8080)
