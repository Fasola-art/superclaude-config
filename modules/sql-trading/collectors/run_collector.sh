#!/bin/bash
# SQL Trading 데이터 수집기 래퍼 스크립트

# 환경 설정
export PATH="/opt/homebrew/opt/postgresql@16/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
export PYTHONPATH="/Users/reim/Library/Python/3.9/lib/python/site-packages:$PYTHONPATH"

# 로그 디렉토리
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"

# 실행
cd "$HOME/.claude/modules/sql-trading/collectors"
/usr/bin/python3 realtime_collector.py --quiet

# 타임스탬프 기록
echo "$(date '+%Y-%m-%d %H:%M:%S') - 수집 완료" >> "$LOG_DIR/sql-trading-collector.log"
