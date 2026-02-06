#!/bin/bash
# SuperClaude v2.0.9 셋업 스크립트
# 다른 컴퓨터에서 실행: curl -sL <raw-url> | bash
# 또는: bash setup.sh

set -euo pipefail

REPO="https://github.com/Fasola-art/superclaude-config.git"
TARGET="$HOME/.claude"

echo "=== SuperClaude v2.0.9 Setup ==="

# 1. 기존 디렉토리 확인
if [ -d "$TARGET/.git" ]; then
    echo "[INFO] 기존 설치 발견 → git pull"
    cd "$TARGET" && git pull origin main
else
    if [ -d "$TARGET" ]; then
        echo "[INFO] ~/.claude 존재하지만 git 아님 → 백업 후 클론"
        mv "$TARGET" "${TARGET}.backup.$(date +%Y%m%d%H%M%S)"
    fi
    echo "[CLONE] $REPO → $TARGET"
    git clone "$REPO" "$TARGET"
fi

cd "$TARGET"

# 2. credentials 디렉토리 생성
mkdir -p credentials
echo "[INFO] credentials/ 폴더 생성됨 → API 키를 수동으로 추가하세요"
echo "  파일: credentials/api-keys.json"

# 3. 런타임 디렉토리 생성
for dir in cache debug logs file-history session-env shell-snapshots paste-cache statsig telemetry sessions todos tasks backups downloads; do
    mkdir -p "$dir"
done
echo "[INFO] 런타임 디렉토리 생성 완료"

# 4. Python 의존성 (jarvis)
if command -v python3 &>/dev/null; then
    echo "[INFO] Python3 감지됨"
    pip3 install --quiet aiohttp httpx pydantic 2>/dev/null || true
else
    echo "[WARN] Python3 미설치 → jarvis 모듈 사용 불가"
fi

# 5. Node.js 의존성 (sql-trading dashboard)
if command -v pnpm &>/dev/null; then
    echo "[INFO] pnpm 감지됨 → sql-trading 의존성 설치"
    cd modules/sql-trading && pnpm install 2>/dev/null || true
    cd "$TARGET"
elif command -v npm &>/dev/null; then
    echo "[INFO] npm 감지됨 (pnpm 권장)"
    echo "  설치: npm install -g pnpm"
fi

# 6. hooks 실행 권한
chmod +x hooks/**/*.py 2>/dev/null || true
chmod +x scripts/*.py scripts/*.sh 2>/dev/null || true
echo "[INFO] hooks/scripts 실행 권한 설정"

# 7. 완료
echo ""
echo "=== 셋업 완료 ==="
echo ""
echo "필수 후속 작업:"
echo "  1. API 키 설정: ~/.claude/credentials/api-keys.json"
echo "  2. MCP 서버: ~/.claude/mcp.json (기기별 설정 필요)"
echo "  3. settings.local.json: 기기별 커스텀 설정"
echo ""
echo "확인: claude --version"
