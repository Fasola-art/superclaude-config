#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="/tmp/chart-doctor-preview.pid"
LOG_FILE="/tmp/chart-doctor-preview.log"

if [[ -f "$PID_FILE" ]]; then
  OLD_PID="$(cat "$PID_FILE")"
  if ps -p "$OLD_PID" >/dev/null 2>&1; then
    kill "$OLD_PID" || true
  fi
fi

cd "$ROOT"
nohup pnpm preview --host 127.0.0.1 --port 4173 >"$LOG_FILE" 2>&1 &
PID=$!
echo "$PID" > "$PID_FILE"

sleep 1
if ! curl -sSf http://127.0.0.1:4173/ >/dev/null; then
  echo "preview 서버 시작 실패. 로그: $LOG_FILE"
  exit 1
fi

echo "대시보드 실행됨: http://127.0.0.1:4173/"
echo "PID: $PID"
echo "로그: $LOG_FILE"
