#!/usr/bin/env python3
"""
텔레그램 메시지 AI 요약
- Claude Haiku를 사용한 메시지 요약
- 주요 이슈 추출
- 키워드 분석
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

MODULE_DIR = Path.home() / ".claude" / "modules" / "telegram"
DATA_DIR = MODULE_DIR / "data"
CREDENTIALS_FILE = Path.home() / ".claude" / "credentials" / "api-keys.json"

def load_api_key() -> str:
    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
    return creds['anthropic']['api_key']

def load_messages(hours: int = 24, chat_id: Optional[int] = None) -> List[Dict]:
    """메시지 로드"""
    messages_file = DATA_DIR / "messages.json"
    if not messages_file.exists():
        return []

    with open(messages_file, 'r', encoding='utf-8') as f:
        messages = json.load(f)

    cutoff = datetime.now() - timedelta(hours=hours)
    filtered = [
        m for m in messages
        if datetime.fromisoformat(m['timestamp']) > cutoff
    ]

    if chat_id:
        filtered = [m for m in filtered if m['chat_id'] == chat_id]

    return filtered

def format_messages_for_summary(messages: List[Dict]) -> str:
    """메시지를 요약용 텍스트로 변환"""
    if not messages:
        return ""

    lines = []
    for m in messages:
        time = datetime.fromisoformat(m['timestamp']).strftime('%H:%M')
        name = m['first_name'] or 'Unknown'
        text = m['text'][:500]  # 긴 메시지 제한
        lines.append(f"[{time}] {name}: {text}")

    return "\n".join(lines)

def summarize_messages(messages: List[Dict], topic: str = "일반") -> Dict:
    """Claude를 사용해 메시지 요약"""
    api_key = load_api_key()

    if not messages:
        return {
            'success': False,
            'error': '요약할 메시지 없음',
            'summary': None
        }

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        messages_text = format_messages_for_summary(messages)
        chat_title = messages[0].get('chat_title', 'Unknown')

        prompt = f"""다음은 텔레그램 그룹 "{chat_title}"의 최근 대화 내용입니다.

주제/목적: {topic}

대화 내용:
{messages_text}

위 대화를 분석하여 다음 형식으로 요약해주세요:

## 주요 내용 요약
(3-5개 핵심 포인트)

## 중요 이슈/토픽
(논의된 주요 주제들)

## 액션 아이템
(결정사항, 해야 할 일 등)

## 주목할 정보
(수치, 날짜, 링크 등 중요 정보)

간결하게 작성. 체언 종결 사용."""

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        summary_text = response.content[0].text

        # 비용 계산
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = (input_tokens * 0.80 + output_tokens * 4.00) / 1_000_000

        result = {
            'success': True,
            'chat_title': chat_title,
            'message_count': len(messages),
            'summary': summary_text,
            'tokens': {
                'input': input_tokens,
                'output': output_tokens
            },
            'cost': cost,
            'timestamp': datetime.now().isoformat()
        }

        # 요약 저장
        save_summary(result)

        return result

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'summary': None
        }

def save_summary(result: Dict):
    """요약 결과 저장"""
    summaries_dir = DATA_DIR / "summaries"
    summaries_dir.mkdir(exist_ok=True)

    date_str = datetime.now().strftime('%Y-%m-%d')
    summary_file = summaries_dir / f"summary_{date_str}.json"

    # 기존 요약 로드
    summaries = []
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            summaries = json.load(f)

    summaries.append(result)

    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

def get_chat_list() -> List[Dict]:
    """모니터링 중인 채팅방 목록"""
    messages = load_messages(hours=168)  # 7일

    chats = {}
    for m in messages:
        chat_id = m['chat_id']
        if chat_id not in chats:
            chats[chat_id] = {
                'chat_id': chat_id,
                'title': m['chat_title'],
                'message_count': 0
            }
        chats[chat_id]['message_count'] += 1

    return list(chats.values())

# CLI
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("사용법:")
        print("  python summarizer.py list          - 채팅방 목록")
        print("  python summarizer.py summary       - 전체 요약 (24시간)")
        print("  python summarizer.py summary 48    - 전체 요약 (48시간)")
        print("  python summarizer.py chat <ID>     - 특정 채팅방 요약")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
        chats = get_chat_list()
        if chats:
            print("모니터링 중인 채팅방:")
            for c in chats:
                print(f"  [{c['chat_id']}] {c['title']} - {c['message_count']}개 메시지")
        else:
            print("수집된 메시지 없음")

    elif cmd == "summary":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        messages = load_messages(hours=hours)
        print(f"최근 {hours}시간 메시지 {len(messages)}개 요약 중...")

        result = summarize_messages(messages)
        if result['success']:
            print(f"\n{'='*50}")
            print(f"채팅방: {result['chat_title']}")
            print(f"메시지: {result['message_count']}개")
            print(f"{'='*50}\n")
            print(result['summary'])
            print(f"\n{'='*50}")
            print(f"비용: ${result['cost']:.4f}")
        else:
            print(f"오류: {result['error']}")

    elif cmd == "chat":
        if len(sys.argv) < 3:
            print("채팅방 ID 필요")
            sys.exit(1)

        chat_id = int(sys.argv[2])
        hours = int(sys.argv[3]) if len(sys.argv) > 3 else 24
        messages = load_messages(hours=hours, chat_id=chat_id)

        if not messages:
            print(f"채팅방 {chat_id}의 메시지 없음")
            sys.exit(1)

        print(f"채팅방 {chat_id} 요약 중... ({len(messages)}개 메시지)")
        result = summarize_messages(messages)

        if result['success']:
            print(f"\n{result['summary']}")
            print(f"\n비용: ${result['cost']:.4f}")
        else:
            print(f"오류: {result['error']}")
