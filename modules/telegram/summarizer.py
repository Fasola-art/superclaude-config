#!/usr/bin/env python3
"""
텔레그램 메시지 AI 요약
- Ollama (Qwen2.5-7B)를 사용한 메시지 요약
- 주요 이슈 추출
- 키워드 분석
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

MODULE_DIR = Path.home() / ".claude" / "modules" / "telegram"
DATA_DIR = MODULE_DIR / "data"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"

def check_ollama() -> bool:
    """Ollama 서버 상태 체크"""
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False

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
    """Ollama를 사용해 메시지 요약"""
    if not messages:
        return {
            'success': False,
            'error': '요약할 메시지 없음',
            'summary': None
        }

    if not check_ollama():
        return {
            'success': False,
            'error': 'Ollama 서버 연결 실패',
            'summary': None
        }

    try:
        messages_text = format_messages_for_summary(messages)
        chat_title = messages[0].get('chat_title', 'Unknown')

        prompt = f"""[필수 규칙]
- 100% 한국어로만 작성. 중국어(简体/繁體) 절대 금지.
- 아래 ## 형식 그대로 유지. 섹션 제목 변경 금지.
- 간결한 체언 종결 ("~함", "~됨", "~예정")

다음은 텔레그램 그룹 "{chat_title}"의 최근 대화 내용입니다.

주제/목적: {topic}

대화 내용:
{messages_text}

위 대화를 분석하여 아래 형식으로 요약:

## 주요 내용 요약
- (핵심 포인트 1)
- (핵심 포인트 2)
- (핵심 포인트 3)

## 중요 이슈/토픽
- (주요 주제 1)
- (주요 주제 2)

## 액션 아이템
- (결정사항/할 일)

## 주목할 정보
- (수치, 날짜, 링크 등)"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 1500, "temperature": 0.7}
            },
            timeout=120
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API 오류: {response.status_code}")

        summary_text = response.json().get("response", "")

        result = {
            'success': True,
            'chat_title': chat_title,
            'message_count': len(messages),
            'summary': summary_text,
            'tokens': {'input': 0, 'output': 0},
            'cost': 0.0,  # 로컬 모델은 무료
            'model': OLLAMA_MODEL,
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
