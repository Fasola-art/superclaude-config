#!/usr/bin/env python3
"""
브리핑 섹션 빌더

텔레그램 브리핑 메시지의 각 섹션을 DB에서 조회하여 마크다운 문자열로 반환.
"""

from datetime import datetime

from _db_utils import query_rows

# 감정분석 점수 → 이모지 매핑
_SENT_EMOJI = {True: "📈", False: "📉"}

# 신호 타입 → 라벨
_SIGNAL_LABELS = {
    "STRONG_BUY": "🔥 적극매수", "BUY": "📈 매수",
    "STRONG_SELL": "💥 적극매도", "SELL": "📉 매도",
    "OVERSOLD": "🔄 과매도",
}


def header() -> str:
    """시장 요약 헤더"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    next_h = (datetime.now().hour + 1) % 24
    return f"📊 *마켓브리핑* | {now}\n\n✅ 다음 브리핑: {next_h:02d}:00"


def crypto() -> str:
    """코인 가격 + 김프"""
    rows = query_rows("""
        SELECT cp.symbol,
               ROUND(cp.price_usd::numeric, 0),
               ROUND(cp.change_pct_24h::numeric, 1),
               ROUND(COALESCE(kp.premium_pct, 0)::numeric, 1)
        FROM (
            SELECT DISTINCT ON (symbol) symbol, price_usd, change_pct_24h
            FROM crypto_prices ORDER BY symbol, timestamp DESC
        ) cp
        LEFT JOIN (
            SELECT DISTINCT ON (symbol) symbol, premium_pct
            FROM kimchi_premium ORDER BY symbol, timestamp DESC
        ) kp ON cp.symbol = kp.symbol
        WHERE cp.symbol IN ('BTC', 'ETH')
        ORDER BY cp.symbol;
    """)
    if not rows:
        return ""
    lines = ["💰 *코인*"]
    for row in rows:
        parts = row.split("|")
        if len(parts) >= 4:
            sym, price, chg, prem = parts[0], parts[1], parts[2], parts[3]
            sign = "+" if float(chg) >= 0 else ""
            lines.append(f"{sym} ${price} ({sign}{chg}%) | 김프 {prem}%")
    return "\n".join(lines) if len(lines) > 1 else ""


def news() -> str:
    """주요 뉴스 (최근 2시간 내 신규)"""
    rows = query_rows("""
        SELECT title, category, ROUND(sentiment::numeric, 2)
        FROM market_news
        WHERE timestamp > NOW() - INTERVAL '2 hours'
          AND sentiment IS NOT NULL
        ORDER BY ABS(sentiment) DESC
        LIMIT 5;
    """)
    if not rows:
        return ""
    lines = [f"📰 *주요 뉴스* ({len(rows)}건 신규)"]
    for row in rows[:3]:
        parts = row.split("|")
        if len(parts) >= 3:
            title = parts[0].strip()[:40]
            sent = float(parts[2])
            emoji = _SENT_EMOJI[sent > 0]
            pct = abs(int(sent * 100))
            label = "긍정" if sent > 0 else "부정"
            lines.append(f"• {emoji} {label} {pct}% | {title}")
    return "\n".join(lines)


def signals() -> str:
    """트레이딩 신호 (최근 2시간)"""
    rows = query_rows("""
        SELECT symbol, signal_type, ROUND(confidence::numeric * 100),
               ROUND(price::numeric, 2)
        FROM trading_signals
        WHERE timestamp > NOW() - INTERVAL '2 hours'
          AND confidence >= 0.65
        ORDER BY confidence DESC
        LIMIT 3;
    """)
    if not rows:
        return ""
    lines = ["📈 *트레이딩 신호*"]
    for row in rows:
        parts = row.split("|")
        if len(parts) >= 4:
            sym, sig, conf, price = parts[0], parts[1], parts[2], parts[3]
            label = _SIGNAL_LABELS.get(sig.strip(), sig)
            lines.append(f"{label} {sym} ${price} (신뢰도 {conf}%)")
    return "\n".join(lines)


def alerts() -> str:
    """급등/급락 알림 (±3% 이상)"""
    rows = query_rows("""
        SELECT DISTINCT ON (symbol) symbol,
               ROUND(change_pct::numeric, 1), ROUND(price::numeric, 2)
        FROM market_snapshots
        WHERE timestamp > NOW() - INTERVAL '2 hours'
          AND ABS(change_pct) >= 3.0
        ORDER BY symbol, timestamp DESC
        LIMIT 5;
    """)
    if not rows:
        return ""
    lines = ["⚠️ *급등/급락*"]
    for row in rows:
        parts = row.split("|")
        if len(parts) >= 3:
            sym, chg, price = parts[0], float(parts[1]), parts[2]
            emoji = "🚀" if chg > 0 else "💥"
            lines.append(f"{emoji} {sym} {chg:+.1f}% (${price})")
    return "\n".join(lines)
