#!/bin/bash
# Skills 설치 재시도 스크립트
# 예약 시간: 1시간 후

LOG_FILE="$HOME/.claude/logs/skills-install-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$HOME/.claude/logs"

echo "=== Skills 설치 재시도 시작: $(date) ===" >> "$LOG_FILE"

npx claude-code-templates@latest --skill document-processing --yes >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Skills 설치 성공!" >> "$LOG_FILE"
    osascript -e 'display notification "Skills 설치 완료!" with title "Claude Code"'
else
    echo "❌ Skills 설치 실패 - 로그 확인: $LOG_FILE" >> "$LOG_FILE"
    osascript -e 'display notification "Skills 설치 실패. 로그를 확인하세요." with title "Claude Code"'
fi

echo "=== 완료: $(date) ===" >> "$LOG_FILE"
