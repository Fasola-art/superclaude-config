#!/bin/bash
# SQL Trading 데이터 수집기 래퍼 스크립트 (크로스플랫폼)

# 플랫폼별 환경 설정
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Windows: PostgreSQL 경로 추가
    export PATH="/c/Program Files/PostgreSQL/16/bin:/c/Program Files/PostgreSQL/15/bin:$PATH"
    PYTHON_CMD="python"
else
    # macOS/Linux
    export PATH="/opt/homebrew/opt/postgresql@16/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
    PYTHON_CMD="python3"
fi

# 로그 디렉토리
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"

# 실행
cd "$HOME/.claude/modules/sql-trading/collectors"
$PYTHON_CMD realtime_collector.py --quiet

# 타임스탬프 기록
echo "$(date '+%Y-%m-%d %H:%M:%S') - 수집 완료" >> "$LOG_DIR/sql-trading-collector.log"
