#!/usr/bin/env bash
# SuperClaude Status Line v1.0
# Usage: bash ~/.claude/statusline.sh
# WSL2 alias: alias cst='bash ~/.claude/statusline.sh'

CLAUDE_DIR="/mnt/c/Users/MSI/.claude"

# Model info from settings.json
model=$(python3 -c "
import json, pathlib
try:
    d = json.loads(pathlib.Path('$CLAUDE_DIR/settings.json').read_text())
    print(d.get('model', 'sonnet'))
except:
    print('sonnet')
" 2>/dev/null || echo "sonnet")

# Git info
branch=$(git branch --show-current 2>/dev/null)
dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')

# Context usage estimation from JSONL files
ctx=$(python3 -c "
import os, pathlib
d = pathlib.Path('$CLAUDE_DIR/projects')
files = list(d.rglob('*.jsonl')) if d.exists() else []
if not files:
    print('0%')
else:
    f = max(files, key=os.path.getmtime)
    size_mb = os.path.getsize(f) / 1024 / 1024
    pct = min(int(size_mb * 50), 100)
    print(f'{pct}%')
" 2>/dev/null || echo "?%")

# Color codes (for terminal support)
if [ -t 1 ]; then
    BOLD='\033[1m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    RED='\033[0;31m'
    NC='\033[0m'
else
    BOLD='' GREEN='' YELLOW='' BLUE='' RED='' NC=''
fi

# Context color
ctx_num=${ctx//%/}
if [ "$ctx_num" -ge 85 ] 2>/dev/null; then
    ctx_color=$RED
elif [ "$ctx_num" -ge 70 ] 2>/dev/null; then
    ctx_color=$YELLOW
else
    ctx_color=$GREEN
fi

# Display
echo -e "${BOLD}[${BLUE}${model}${NC}${BOLD}]${NC} $(basename $PWD) | ${GREEN}${branch:-no-git}${NC}(${dirty} uncommitted) | ctx:${ctx_color}${ctx}${NC}"
