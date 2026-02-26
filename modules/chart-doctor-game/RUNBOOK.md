# Dashboard Runbook

## 실행
- `cd /Users/reim/.claude/modules/chart-doctor-game`
- `./scripts/start_dashboard.sh`
- 접속: `http://127.0.0.1:4173/`

## 중지
- `./scripts/stop_dashboard.sh`

## 상태 확인
- 로그: `/tmp/chart-doctor-preview.log`
- PID: `/tmp/chart-doctor-preview.pid`
- 포트 확인: `lsof -nP -iTCP:4173 -sTCP:LISTEN`

## 화면 확인 실패 시
1. `./scripts/stop_dashboard.sh`
2. `./scripts/start_dashboard.sh`
3. `pnpm capture:dashboard` 실행 후 `test-results/dashboard.png` 확인

## 품질 검증
- `pnpm build`
- `pnpm test:e2e`
