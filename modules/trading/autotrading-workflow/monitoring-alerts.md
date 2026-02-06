# Monitoring & Alerts (모니터링 + 알림)

> 4단계 알림, Grafana 대시보드, 시스템 헬스체크

---

## 알림 레벨

| Level | 예시 | 채널 | 응답 시간 |
|-------|------|------|----------|
| EMERGENCY | 전 포지션 청산, 시스템 다운 | Telegram + 전화 | 즉시 |
| CRITICAL | 일일 손실 -5%, API 장애 | Telegram | 5분 |
| WARNING | 일일 손실 -3%, 지연 증가 | Telegram + 대시보드 | 30분 |
| INFO | 시그널 발행, 체결 확인 | 대시보드 | - |

---

## 알림 채널

| 채널 | 용도 | 대상 레벨 |
|------|------|----------|
| Telegram Bot | 긴급 알림 (주 채널) | EMERGENCY ~ WARNING |
| Grafana Dashboard | 전체 모니터링 | 전체 |
| Galaxy Tab Widget | 실시간 요약 | INFO 이상 |
| 일일 리포트 | 종합 요약 (자동 생성) | INFO |

### Telegram 메시지 포맷

```
🔴 EMERGENCY: 전 포지션 청산
━━━━━━━━━━━━━━━━━━━
총 손실: -10.2% ($-1,020)
청산 종목: BTCUSDT, AAPL, NQ
시간: 2026-02-07 14:30 KST
━━━━━━━━━━━━━━━━━━━
시스템 상태: 중지됨
복구 필요: 수동 재개
```

---

## Grafana 대시보드

### 패널 구성

| 패널 | 데이터 소스 | 갱신 주기 |
|------|-----------|----------|
| PnL 커브 | PostgreSQL | 1분 |
| 포지션 현황 | PostgreSQL | 5초 |
| 리스크 게이지 | PostgreSQL | 10초 |
| 시스템 상태 | InfluxDB | 30초 |
| 최근 시그널 | PostgreSQL | 즉시 |
| 디바이스 헬스 | InfluxDB | 30초 |

---

## 시스템 헬스체크

### 디바이스 모니터링

| 디바이스 | 체크 항목 | 주기 | 장애 시 |
|---------|---------|------|--------|
| Mac Studio | CPU, RAM, Disk, Ollama | 30초 | CRITICAL |
| 사무용 데스크탑 | 브로커 API 연결 | 10초 | EMERGENCY |
| 젯슨 오린 | YOLO 추론, GPU 온도 | 30초 | WARNING |
| RPi5 + Hailo | 뉴스 수집, MQTT | 30초 | WARNING |
| 4090 노트북 | 가동 상태 (WoL) | 5분 | INFO |

### 서비스 모니터링

| 서비스 | 포트 | 체크 방법 | 장애 시 |
|--------|------|----------|--------|
| PostgreSQL | 5432 | `SELECT 1` | EMERGENCY |
| Redis | 6379 | `PING` | CRITICAL |
| Ollama | 11434 | `/api/tags` | CRITICAL |
| MQTT | 1883 | connection check | WARNING |
| InfluxDB | 8086 | `/health` | WARNING |

---

## 로그 수집

```sql
-- meta.system_logs (시스템 로그)
CREATE TABLE meta.system_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    device VARCHAR(50),
    service VARCHAR(50),
    level VARCHAR(20),          -- DEBUG, INFO, WARNING, ERROR, CRITICAL
    message TEXT,
    details JSONB,
    resolved BOOLEAN DEFAULT false
);
```

---

## 일일 리포트 (자동 생성)

| 섹션 | 내용 |
|------|------|
| PnL 요약 | 일일/주간/월간 수익률 |
| 거래 내역 | 체결 목록, 승률, 평균 R:R |
| 리스크 | MDD, 최대 손실 거래, 서킷브레이커 |
| 시그널 | 발행 수, 적중률, 소스별 성과 |
| 시스템 | 다운타임, 지연, 에러 수 |

### 리포트 전송

```
매일 16:00 KST → Telegram 자동 전송
주간: 일요일 09:00 KST (주간 요약)
월간: 1일 09:00 KST (월간 요약)
```

---

**참조**: [risk-management.md](risk-management.md) | [execution-engine.md](execution-engine.md)
