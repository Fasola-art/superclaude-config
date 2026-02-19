#!/bin/bash
# 환경변수를 cron이 읽을 수 있도록 파일로 저장
env | grep -E '^(DB_|ALPHA_|FRED_|PATH=)' > /app/env.sh
sed -i 's/^/export /' /app/env.sh

# 시작 시 1회 즉시 실행
echo "[$(date)] 초기 수집 시작..."
cd /app/collectors && python3 collect_all.py 2>&1 | tee -a /var/log/collector.log

# cron 시작 (포그라운드)
echo "[$(date)] cron 시작 (1시간 주기)"
cron -f
