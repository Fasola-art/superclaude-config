#!/usr/bin/env python3
"""
트레이딩 신호 생성기 (Signal Generator)

수집 데이터 기반 매수/매도 신호 자동 생성
전략:
  1. momentum    - 섹터별 가격 모멘텀
  2. sentiment   - FinBERT 뉴스 감정분석
  3. freight_bdi - BDI 운임지수 기반 해운주
"""
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any

from _db_utils import run_sql, query_rows, escape_sql


def _parse_rows(raw: list[str], cols: list[str]) -> list[dict[str, Any]]:
    """psql 파이프 구분 결과 → dict 리스트"""
    results = []
    for line in raw:
        parts = line.split("|")
        if len(parts) >= len(cols):
            row = {}
            for i, col in enumerate(cols):
                val = parts[i].strip()
                row[col] = val
            results.append(row)
    return results


def strategy_momentum() -> list[dict[str, Any]]:
    """모멘텀 전략: 최근 수집 데이터에서 급등/급락 종목 감지"""
    sql = """
    SELECT DISTINCT ON (symbol)
        symbol,
        ROUND(change_pct::numeric, 4) as change_pct,
        ROUND(price::numeric, 4) as price,
        metadata->>'sector' as sector,
        metadata->>'name' as name
    FROM market_snapshots
    WHERE timestamp > NOW() - INTERVAL '2 hours'
      AND metadata->>'sector' IS NOT NULL
    ORDER BY symbol, timestamp DESC;
    """
    raw = query_rows(sql)
    rows = _parse_rows(raw, ["symbol", "change_pct", "price", "sector", "name"])

    signals = []
    for r in rows:
        try:
            chg = float(r["change_pct"])
            price = float(r["price"])
        except (ValueError, TypeError):
            continue

        symbol = r["symbol"]
        name = r.get("name", symbol)

        sector = r.get("sector", "")
        sector_kr = _sector_label(sector)

        if chg >= 4.0:
            signals.append(_make_signal(
                symbol, "STRONG_BUY", min(0.65 + (chg - 4) * 0.05, 0.95),
                price, price * 1.08, price * 0.95, "momentum",
                f"[강매수] {name} 2시간 내 {chg:+.1f}% 급등. "
                f"{sector_kr} 섹터 강세 흐름. "
                f"목표 +8%, 손절 -5%. 단기 모멘텀 추종 전략.",
            ))
        elif chg >= 2.5:
            signals.append(_make_signal(
                symbol, "BUY", min(0.55 + (chg - 2.5) * 0.06, 0.85),
                price, price * 1.05, price * 0.97, "momentum",
                f"[매수] {name} {chg:+.1f}% 상승 중. "
                f"{sector_kr} 섹터 상승세 확인. "
                f"목표 +5%, 손절 -3%. 추세 확인 후 진입 권장.",
            ))
        elif chg <= -4.0:
            signals.append(_make_signal(
                symbol, "STRONG_SELL", min(0.65 + abs(chg + 4) * 0.05, 0.95),
                price, price * 0.92, price * 1.05, "momentum",
                f"[강매도] {name} 2시간 내 {chg:+.1f}% 급락. "
                f"{sector_kr} 섹터 전반 약세. "
                f"추가 하락 위험. 보유 시 즉시 손절 권장.",
            ))
        elif chg <= -2.5:
            signals.append(_make_signal(
                symbol, "SELL", min(0.55 + abs(chg + 2.5) * 0.06, 0.85),
                price, price * 0.95, price * 1.03, "momentum",
                f"[매도] {name} {chg:+.1f}% 하락 중. "
                f"{sector_kr} 섹터 하락 압력. "
                f"반등 실패 시 추가 하락 가능. 비중 축소 권장.",
            ))

    return signals


def strategy_sentiment() -> list[dict[str, Any]]:
    """감정분석 전략: FinBERT 점수 기반 종목별 신호"""
    sql = """
    SELECT category,
           ROUND(AVG(sentiment)::numeric, 4) as avg_sent,
           COUNT(*) as cnt
    FROM market_news
    WHERE timestamp > NOW() - INTERVAL '6 hours'
      AND sentiment IS NOT NULL
    GROUP BY category
    HAVING COUNT(*) >= 2;
    """
    raw = query_rows(sql)
    rows = _parse_rows(raw, ["category", "avg_sent", "cnt"])

    # 카테고리 → 대표 종목 매핑
    category_symbols = {
        "stocks": ("^GSPC", "S&P 500"),
        "crypto": ("BTC", "Bitcoin"),
        "economy": ("DBC", "Commodities"),
    }

    signals = []
    for r in rows:
        try:
            sent = float(r["avg_sent"])
            cnt = int(r["cnt"])
        except (ValueError, TypeError):
            continue

        cat = r["category"]
        if cat not in category_symbols:
            continue

        symbol, name = category_symbols[cat]
        confidence = min(0.50 + abs(sent) * 0.4 + cnt * 0.02, 0.90)

        # 현재가 조회
        price_row = query_rows(
            f"SELECT ROUND(price::numeric, 4) FROM market_snapshots "
            f"WHERE symbol = '{symbol}' ORDER BY timestamp DESC LIMIT 1;"
        )
        price = float(price_row[0].strip()) if price_row else 0

        strength = "강한 " if abs(sent) >= 0.6 else ""
        if sent >= 0.3:
            signals.append(_make_signal(
                symbol, "BUY", confidence, price, price * 1.05, price * 0.97,
                "sentiment",
                f"[매수] FinBERT 감정분석: {name} 관련 {cnt}건 뉴스 "
                f"{strength}긍정 (점수 {sent:+.2f}). "
                f"시장 심리 개선 구간. 분할 매수 접근 권장.",
            ))
        elif sent <= -0.3:
            signals.append(_make_signal(
                symbol, "SELL", confidence, price, price * 0.95, price * 1.03,
                "sentiment",
                f"[매도] FinBERT 감정분석: {name} 관련 {cnt}건 뉴스 "
                f"{strength}부정 (점수 {sent:+.2f}). "
                f"시장 심리 악화 구간. 신규 매수 보류, 보유 시 비중 축소 권장.",
            ))

    return signals


def strategy_freight() -> list[dict[str, Any]]:
    """운임지수 전략: BDI 변동 → 해운주 연동"""
    sql = """
    SELECT ROUND(value::numeric, 2) as val,
           ROUND(change_pct::numeric, 2) as chg
    FROM freight_indices
    WHERE index_name = 'BDI'
    ORDER BY date DESC LIMIT 1;
    """
    raw = query_rows(sql)
    if not raw:
        return []

    rows = _parse_rows(raw, ["val", "chg"])
    if not rows:
        return []

    try:
        bdi_val = float(rows[0]["val"])
        bdi_chg = float(rows[0]["chg"])
    except (ValueError, TypeError):
        return []

    # BDI 변동이 크면 Dry Bulk 해운주에 신호
    shipping = [("SBLK", "Star Bulk"), ("GNK", "Genco"), ("EGLE", "Eagle Bulk")]
    signals = []

    if abs(bdi_chg) < 2.0:
        return []

    for symbol, name in shipping:
        price_row = query_rows(
            f"SELECT ROUND(price::numeric, 4) FROM market_snapshots "
            f"WHERE symbol = '{symbol}' ORDER BY timestamp DESC LIMIT 1;"
        )
        price = float(price_row[0].strip()) if price_row else 0

        confidence = min(0.55 + abs(bdi_chg) * 0.04, 0.90)

        if bdi_chg >= 2.0:
            signals.append(_make_signal(
                symbol, "BUY", confidence, price, price * 1.06, price * 0.96,
                "freight_bdi",
                f"[매수] BDI {bdi_val:.0f}pt ({bdi_chg:+.1f}%) 상승. "
                f"벌크 운임 강세 → {name} 운임 수익 개선 기대. "
                f"목표 +6%, 손절 -4%. BDI 추세 확인 후 진입.",
            ))
        elif bdi_chg <= -2.0:
            signals.append(_make_signal(
                symbol, "SELL", confidence, price, price * 0.94, price * 1.04,
                "freight_bdi",
                f"[매도] BDI {bdi_val:.0f}pt ({bdi_chg:+.1f}%) 하락. "
                f"벌크 운임 약세 → {name} 실적 악화 우려. "
                f"운임 반등 전까지 신규 매수 보류 권장.",
            ))

    return signals


def _sector_label(sector: str) -> str:
    """섹터 영문 → 한글 레이블"""
    return {
        "dry_bulk": "벌크 해운", "container": "컨테이너 해운",
        "tanker": "유조선", "commodity": "원자재",
        "index": "시장 지수",
    }.get(sector, sector or "해운")


def _make_signal(
    symbol: str, signal_type: str, confidence: float,
    price: float, target: float, stop_loss: float,
    strategy: str, reason: str,
) -> dict[str, Any]:
    """신호 dict 생성"""
    return {
        "symbol": symbol,
        "signal_type": signal_type,
        "confidence": round(confidence, 4),
        "price": round(price, 4),
        "target_price": round(target, 4),
        "stop_loss": round(stop_loss, 4),
        "strategy": strategy,
        "reason": reason,
    }


def save_signals(signals: list[dict[str, Any]]) -> int:
    """신호 DB 저장 (중복 방지: 같은 종목+전략 1시간 내 스킵)"""
    saved = 0
    for s in signals:
        # 중복 체크
        dup = query_rows(
            f"SELECT id FROM trading_signals "
            f"WHERE symbol = '{s['symbol']}' AND strategy = '{s['strategy']}' "
            f"AND timestamp > NOW() - INTERVAL '1 hour' LIMIT 1;"
        )
        if dup:
            continue

        reason_escaped = escape_sql(s["reason"])
        sql = (
            f"INSERT INTO trading_signals "
            f"(timestamp, symbol, signal_type, confidence, price, "
            f"target_price, stop_loss, strategy, reason, alt_data_source) "
            f"VALUES (NOW(), '{s['symbol']}', '{s['signal_type']}', "
            f"{s['confidence']}, {s['price']}, {s['target_price']}, "
            f"{s['stop_loss']}, '{s['strategy']}', '{reason_escaped}', "
            f"'{s['strategy']}');"
        )
        if run_sql(sql):
            saved += 1

    return saved


def collect_and_save(verbose: bool = True) -> int:
    """전체 전략 실행 및 저장"""
    all_signals = []

    # 1. 모멘텀
    momentum = strategy_momentum()
    if verbose and momentum:
        print(f"    momentum: {len(momentum)}건")
    all_signals.extend(momentum)

    # 2. 감정분석
    sentiment = strategy_sentiment()
    if verbose and sentiment:
        print(f"    sentiment: {len(sentiment)}건")
    all_signals.extend(sentiment)

    # 3. 운임지수
    freight = strategy_freight()
    if verbose and freight:
        print(f"    freight_bdi: {len(freight)}건")
    all_signals.extend(freight)

    if not all_signals:
        if verbose:
            print("  ℹ️ 임계값 미달, 신호 없음")
        return 0

    saved = save_signals(all_signals)
    if verbose:
        for s in all_signals:
            emoji = {"BUY": "📈", "STRONG_BUY": "🔥", "SELL": "📉", "STRONG_SELL": "💥"}.get(s["signal_type"], "📊")
            print(f"    {emoji} {s['symbol']:5} {s['signal_type']:12} {s['confidence']:.0%} - {s['reason']}")
        print(f"  ✅ {saved}건 신호 저장 ({len(all_signals) - saved}건 중복 스킵)")

    return saved


if __name__ == "__main__":
    print("📊 트레이딩 신호 생성 중...")
    cnt = collect_and_save(verbose=True)
    print(f"완료: {cnt}건")
    sys.exit(0)
