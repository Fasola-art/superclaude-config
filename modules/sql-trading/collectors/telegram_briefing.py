#!/usr/bin/env python3
"""
텔레그램 마켓 브리핑 모듈

1시간마다 수집 파이프라인 마지막에 실행.
DB에서 최신 데이터를 조회하여 텔레그램으로 브리핑 전송.
"""

import sys
from datetime import datetime

import _briefing_sections as sections
from telegram_sender import send_briefing, send_message


def collect_and_save(verbose: bool = False) -> int:
    """브리핑 생성 및 텔레그램 전송 (collect_all.py 호환 인터페이스)

    Returns:
        전송 건수 (성공 1, 실패 0)
    """
    parts = [
        sections.header(),
        sections.crypto(),
        sections.news(),
        sections.signals(),
        sections.alerts(),
    ]
    # 헤더 외에 내용이 없으면 간결 메시지
    has_content = any(parts[1:])
    if not has_content:
        now = datetime.now().strftime("%H:%M")
        ok = send_message(f"✅ [{now}] 시장 안정 — 특이사항 없음")
    else:
        ok = send_briefing(parts)

    if verbose:
        status = "✅ 전송 성공" if ok else "❌ 전송 실패"
        print(f"  {status}")
    return 1 if ok else 0


if __name__ == "__main__":
    count = collect_and_save(verbose=True)
    sys.exit(0 if count > 0 else 1)
