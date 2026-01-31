#!/usr/bin/env python3
"""
텔레그램 그룹 메시지 모니터링 및 요약
- 실시간 메시지 수집
- 일일/주간 요약 생성
- 키워드 알림
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# 설정
MODULE_DIR = Path.home() / ".claude" / "modules" / "telegram"
DATA_DIR = MODULE_DIR / "data"
LOGS_DIR = MODULE_DIR / "logs"
CREDENTIALS_FILE = Path.home() / ".claude" / "credentials" / "api-keys.json"

# 토큰 로드
def load_token() -> str:
    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
    return creds['telegram']['bot_token']

BOT_TOKEN = load_token()

# 메시지 저장소
class MessageStore:
    def __init__(self):
        self.messages_file = DATA_DIR / "messages.json"
        self.messages: List[Dict] = []
        self.load()

    def load(self):
        if self.messages_file.exists():
            with open(self.messages_file, 'r', encoding='utf-8') as f:
                self.messages = json.load(f)

    def save(self):
        with open(self.messages_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)

    def add(self, msg: Dict):
        self.messages.append(msg)
        # 최근 7일만 유지
        cutoff = datetime.now() - timedelta(days=7)
        self.messages = [
            m for m in self.messages
            if datetime.fromisoformat(m['timestamp']) > cutoff
        ]
        self.save()

    def get_recent(self, hours: int = 24) -> List[Dict]:
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            m for m in self.messages
            if datetime.fromisoformat(m['timestamp']) > cutoff
        ]

    def get_by_chat(self, chat_id: int, hours: int = 24) -> List[Dict]:
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            m for m in self.messages
            if m['chat_id'] == chat_id and datetime.fromisoformat(m['timestamp']) > cutoff
        ]

store = MessageStore()

# 메시지 핸들러
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """모든 그룹 메시지 수집"""
    if not update.message or not update.message.text:
        return

    msg = update.message

    message_data = {
        'message_id': msg.message_id,
        'chat_id': msg.chat_id,
        'chat_title': msg.chat.title or "Private",
        'user_id': msg.from_user.id if msg.from_user else None,
        'username': msg.from_user.username if msg.from_user else None,
        'first_name': msg.from_user.first_name if msg.from_user else None,
        'text': msg.text,
        'timestamp': datetime.now().isoformat()
    }

    store.add(message_data)

    # 로그
    log_file = LOGS_DIR / f"messages_{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{message_data['timestamp']}] {message_data['chat_title']} | {message_data['first_name']}: {message_data['text'][:100]}\n")

# 명령어: 요약 요청
async def cmd_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """최근 24시간 메시지 요약"""
    chat_id = update.effective_chat.id
    messages = store.get_by_chat(chat_id, hours=24)

    if not messages:
        await update.message.reply_text("최근 24시간 내 메시지 없음")
        return

    # 메시지 텍스트 추출
    texts = [f"{m['first_name']}: {m['text']}" for m in messages]
    summary = f"최근 24시간 메시지 {len(messages)}개 수집됨\n\n"
    summary += "요약 생성은 /summarize_ai 명령어 사용"

    await update.message.reply_text(summary)

# 명령어: 통계
async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """메시지 통계"""
    messages = store.get_recent(hours=24)

    # 채팅방별 통계
    chat_stats = {}
    for m in messages:
        title = m['chat_title']
        chat_stats[title] = chat_stats.get(title, 0) + 1

    # 사용자별 통계
    user_stats = {}
    for m in messages:
        name = m['first_name'] or 'Unknown'
        user_stats[name] = user_stats.get(name, 0) + 1

    stats_text = f"📊 최근 24시간 통계\n\n"
    stats_text += f"총 메시지: {len(messages)}개\n\n"

    stats_text += "채팅방별:\n"
    for chat, count in sorted(chat_stats.items(), key=lambda x: -x[1])[:5]:
        stats_text += f"  - {chat}: {count}개\n"

    stats_text += "\n활발한 사용자:\n"
    for user, count in sorted(user_stats.items(), key=lambda x: -x[1])[:5]:
        stats_text += f"  - {user}: {count}개\n"

    await update.message.reply_text(stats_text)

# 명령어: 모니터링 중인 채팅방
async def cmd_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """모니터링 중인 채팅방 목록"""
    messages = store.get_recent(hours=168)  # 7일

    chats = {}
    for m in messages:
        chat_id = m['chat_id']
        if chat_id not in chats:
            chats[chat_id] = {
                'title': m['chat_title'],
                'count': 0,
                'last_message': m['timestamp']
            }
        chats[chat_id]['count'] += 1

    text = "모니터링 중인 채팅방:\n\n"
    for chat_id, info in chats.items():
        text += f"• {info['title']}\n"
        text += f"  ID: {chat_id}\n"
        text += f"  메시지: {info['count']}개 (7일)\n\n"

    if not chats:
        text = "모니터링 중인 채팅방 없음.\n봇을 그룹에 추가해주세요."

    await update.message.reply_text(text)

# 메인
def main():
    """봇 실행"""
    print(f"[{datetime.now()}] 텔레그램 모니터 시작...")

    app = Application.builder().token(BOT_TOKEN).build()

    # 핸들러 등록
    app.add_handler(CommandHandler("summary", cmd_summary))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("chats", cmd_chats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("봇 명령어:")
    print("  /summary - 최근 24시간 요약")
    print("  /stats - 메시지 통계")
    print("  /chats - 모니터링 중인 채팅방")
    print("\n봇을 그룹에 추가하면 자동으로 메시지 수집 시작")
    print("Ctrl+C로 종료\n")

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
