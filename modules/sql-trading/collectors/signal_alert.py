#!/usr/bin/env python3
"""
트레이딩 신호 알림 시스템 (Signal Alert System)

기능:
- 신규 매수/매도 신호 감지
- 급등/급락 종목 알림
- macOS 알림 센터 연동

Version: 1.0.0
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from telegram_sender import send_message as tg_send

# psql 경로
PSQL_PATHS = [
    "/opt/homebrew/opt/postgresql@16/bin/psql",
    "/opt/homebrew/bin/psql",
    "/usr/local/bin/psql",
]

# 알림 임계값
THRESHOLDS = {
    "price_change_alert": 3.0,      # 가격 변동 알림 (%)
    "signal_confidence": 0.70,       # 신호 신뢰도 임계값
    "volume_spike": 2.0,             # 거래량 급증 배수
}

# 상태 파일 경로
STATE_FILE = Path.home() / ".claude" / "modules" / "sql-trading" / ".alert_state.json"


def get_psql_path() -> Optional[str]:
    """psql 경로 찾기"""
    for path in PSQL_PATHS:
        if Path(path).exists():
            return path
    return None


def run_query(sql: str) -> List[Dict[str, Any]]:
    """SQL 쿼리 실행"""
    psql = get_psql_path()
    if not psql:
        return []

    try:
        result = subprocess.run(
            [psql, "-U", "reim", "-d", "claude_mcp", "-t", "-A", "-F", "|", "-c", sql],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return []

        rows = []
        for line in result.stdout.strip().split("\n"):
            if line:
                rows.append(line.split("|"))
        return rows

    except Exception as e:
        print(f"쿼리 오류: {e}")
        return []


def send_notification(title: str, message: str, sound: bool = True) -> bool:
    """macOS 알림 센터로 알림 전송"""
    script = f'''
    display notification "{message}" with title "{title}" sound name "Glass"
    '''
    if not sound:
        script = f'''
        display notification "{message}" with title "{title}"
        '''

    try:
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def load_state() -> Dict[str, Any]:
    """이전 상태 로드"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_check": None, "notified_signals": []}


def save_state(state: Dict[str, Any]) -> None:
    """상태 저장"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def check_new_signals() -> List[Dict[str, Any]]:
    """신규 트레이딩 신호 확인"""
    sql = """
    SELECT
        symbol,
        signal_type,
        ROUND(confidence::numeric * 100),
        ROUND(price::numeric, 2),
        reason
    FROM trading_signals
    WHERE timestamp > NOW() - INTERVAL '30 minutes'
      AND signal_type IN ('BUY', 'STRONG_BUY', 'SELL', 'STRONG_SELL', 'OVERSOLD')
      AND confidence >= 0.65
    ORDER BY timestamp DESC
    LIMIT 10;
    """

    rows = run_query(sql)
    signals = []
    for row in rows:
        if len(row) >= 5:
            signals.append({
                "symbol": row[0],
                "signal_type": row[1],
                "confidence": row[2],
                "price": row[3],
                "reason": row[4],
            })
    return signals


def check_price_alerts() -> List[Dict[str, Any]]:
    """급등/급락 종목 확인"""
    sql = f"""
    SELECT DISTINCT ON (symbol)
        symbol,
        ROUND(change_pct::numeric, 2),
        ROUND(price::numeric, 2),
        metadata->>'name'
    FROM market_snapshots
    WHERE timestamp > NOW() - INTERVAL '1 hour'
      AND ABS(change_pct) >= {THRESHOLDS['price_change_alert']}
    ORDER BY symbol, timestamp DESC;
    """

    rows = run_query(sql)
    alerts = []
    for row in rows:
        if len(row) >= 4:
            alerts.append({
                "symbol": row[0],
                "change_pct": float(row[1]),
                "price": row[2],
                "name": row[3] or row[0],
            })
    return alerts


def check_sector_shift() -> List[Dict[str, Any]]:
    """섹터 급변동 확인"""
    sql = """
    WITH sector_changes AS (
        SELECT
            metadata->>'sector' as sector,
            AVG(change_pct) as avg_change
        FROM market_snapshots
        WHERE timestamp > NOW() - INTERVAL '2 hours'
          AND metadata->>'sector' IS NOT NULL
        GROUP BY metadata->>'sector'
    )
    SELECT sector, ROUND(avg_change::numeric, 2)
    FROM sector_changes
    WHERE ABS(avg_change) >= 2.0
    ORDER BY ABS(avg_change) DESC;
    """

    rows = run_query(sql)
    shifts = []
    for row in rows:
        if len(row) >= 2:
            shifts.append({
                "sector": row[0],
                "change": float(row[1]),
            })
    return shifts


def format_signal_message(signal: Dict[str, Any]) -> str:
    """신호 메시지 포맷팅"""
    emoji = {
        "STRONG_BUY": "🔥",
        "BUY": "📈",
        "STRONG_SELL": "💥",
        "SELL": "📉",
        "OVERSOLD": "🔄",
    }.get(signal["signal_type"], "📊")

    return f"{emoji} {signal['symbol']} ${signal['price']} ({signal['confidence']}%)"


def main():
    """메인 실행"""
    state = load_state()
    notified = set(state.get("notified_signals", []))
    alerts_sent = 0

    # 1. 신규 트레이딩 신호 확인
    signals = check_new_signals()
    new_signals = []
    for sig in signals:
        sig_key = f"{sig['symbol']}_{sig['signal_type']}"
        if sig_key not in notified:
            new_signals.append(sig)
            notified.add(sig_key)

    if new_signals:
        # 매수 신호
        buy_signals = [s for s in new_signals if "BUY" in s["signal_type"]]
        if buy_signals:
            msg = ", ".join([format_signal_message(s) for s in buy_signals[:3]])
            send_notification("📈 매수 신호", msg)
            tg_send(f"📈 *매수 신호*\n{msg}")
            alerts_sent += 1

        # 매도 신호
        sell_signals = [s for s in new_signals if "SELL" in s["signal_type"]]
        if sell_signals:
            msg = ", ".join([format_signal_message(s) for s in sell_signals[:3]])
            send_notification("📉 매도 신호", msg)
            tg_send(f"📉 *매도 신호*\n{msg}")
            alerts_sent += 1

    # 2. 급등/급락 알림
    price_alerts = check_price_alerts()
    for alert in price_alerts:
        alert_key = f"price_{alert['symbol']}_{datetime.now().strftime('%Y%m%d%H')}"
        if alert_key not in notified:
            direction = "급등 🚀" if alert["change_pct"] > 0 else "급락 💥"
            msg = f"{alert['symbol']} {alert['change_pct']:+.1f}% (${alert['price']})"
            send_notification(f"⚠️ {direction}", msg)
            tg_send(f"⚠️ *{direction}*\n{msg}")
            notified.add(alert_key)
            alerts_sent += 1

    # 3. 섹터 급변동 알림
    sector_shifts = check_sector_shift()
    for shift in sector_shifts:
        shift_key = f"sector_{shift['sector']}_{datetime.now().strftime('%Y%m%d%H')}"
        if shift_key not in notified:
            direction = "강세" if shift["change"] > 0 else "약세"
            sector_name = {
                "dry_bulk": "🏭 Dry Bulk",
                "container": "📦 Container",
                "tanker": "🛢️ Tanker",
                "commodity": "💎 Commodity",
            }.get(shift["sector"], shift["sector"])
            msg = f"{sector_name} {shift['change']:+.1f}%"
            send_notification(f"📊 섹터 {direction}", msg)
            notified.add(shift_key)
            alerts_sent += 1

    # 상태 저장 (최근 100개만 유지)
    state["last_check"] = datetime.now().isoformat()
    state["notified_signals"] = list(notified)[-100:]
    save_state(state)

    # 로그
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 알림 체크 완료: {alerts_sent}개 전송")

    return 0


if __name__ == "__main__":
    sys.exit(main())
