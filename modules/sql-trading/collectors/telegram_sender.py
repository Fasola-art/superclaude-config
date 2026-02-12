#!/usr/bin/env python3
"""
텔레그램 메시지 전송 공통 모듈

Bot API를 직접 호출하여 메시지 전송.
외부 의존성 없이 requests만 사용.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import requests

# 크레덴셜 경로
_CREDS_PATH = Path.home() / ".claude" / "credentials" / "api-keys.json"
_API_BASE = "https://api.telegram.org/bot{token}"


def load_telegram_config() -> tuple[str, str]:
    """봇 토큰 + 사용자 ID 로드"""
    with open(_CREDS_PATH) as f:
        creds = json.load(f)
    tg = creds["telegram"]
    return tg["bot_token"], tg["user_id"]


def send_message(
    text: str,
    parse_mode: str = "Markdown",
    disable_preview: bool = True,
) -> bool:
    """텔레그램 메시지 전송

    Args:
        text: 전송할 메시지 (Markdown 지원)
        parse_mode: 파싱 모드 (Markdown / HTML)
        disable_preview: 링크 미리보기 비활성화

    Returns:
        전송 성공 여부
    """
    try:
        token, user_id = load_telegram_config()
        url = f"{_API_BASE.format(token=token)}/sendMessage"
        payload = {
            "chat_id": user_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_preview,
        }
        resp = requests.post(url, json=payload, timeout=10)
        if not resp.ok:
            # Markdown 파싱 실패 시 plain text 재시도
            if resp.status_code == 400 and "parse" in resp.text.lower():
                payload.pop("parse_mode", None)
                resp = requests.post(url, json=payload, timeout=10)
                return resp.ok
            print(f"  텔레그램 전송 실패: {resp.status_code} {resp.text[:100]}")
            return False
        return True
    except Exception as e:
        print(f"  텔레그램 오류: {e}")
        return False


def send_briefing(sections: list[str]) -> bool:
    """구조화된 브리핑 전송 (섹션 리스트 → 단일 메시지)

    Args:
        sections: 마크다운 섹션 문자열 리스트

    Returns:
        전송 성공 여부
    """
    text = "\n\n".join(s for s in sections if s)
    if not text:
        return False
    # 텔레그램 메시지 길이 제한 (4096자)
    if len(text) > 4000:
        text = text[:3997] + "..."
    return send_message(text)


if __name__ == "__main__":
    # 단독 실행 시 테스트 메시지 전송
    ok = send_message("테스트 메시지 from telegram_sender.py")
    print("✅ 전송 성공" if ok else "❌ 전송 실패")
    sys.exit(0 if ok else 1)
