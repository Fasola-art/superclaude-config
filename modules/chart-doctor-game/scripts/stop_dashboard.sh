#!/usr/bin/env bash
set -euo pipefail

PID_FILE="/tmp/chart-doctor-preview.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "실행 중인 preview PID 파일이 없습니다."
  exit 0
fi

PID="$(cat "$PID_FILE")"
if ps -p "$PID" >/dev/null 2>&1; then
  kill "$PID" || true
  echo "중지 완료: $PID"
else
  echo "프로세스가 이미 종료됨: $PID"
fi

rm -f "$PID_FILE"
