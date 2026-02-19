#!/bin/bash
# Crypto data collector wrapper

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"

cd "$HOME/.claude/modules/sql-trading/collectors" || exit 1
/opt/homebrew/bin/python3 crypto_collector.py

echo "$(date '+%Y-%m-%d %H:%M:%S') - crypto 수집 완료" >> "$LOG_DIR/sql-trading-crypto.log"
