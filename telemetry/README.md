# Telemetry 폴더

> **목적**: 시스템 사용 통계 및 성능 모니터링 데이터
> **갱신일**: 2026-01-30

---

## 📁 폴더 구조

```
telemetry/
├── README.md           # 이 파일
├── config.json         # 텔레메트리 설정
├── daily/              # 일별 통계
│   └── {YYYYMMDD}.json
├── weekly/             # 주별 요약
│   └── {YYYY-Www}.json
├── performance/        # 성능 메트릭
│   └── perf_{YYYYMMDD}.json
└── reports/            # 생성된 보고서
    └── report_{YYYYMMDD}.md
```

---

## 🎯 수집 데이터

| 카테고리 | 항목 | 용도 |
|----------|------|------|
| **사용량** | 세션 수, 토큰 사용량 | 리소스 관리 |
| **성능** | 응답 시간, 도구 실행 시간 | 최적화 |
| **패턴** | 자주 쓰는 명령어, 키워드 | UX 개선 |
| **에러** | 에러 빈도, 유형 | 안정성 향상 |
| **학습** | Ralph Loop 성공률 | Error KB 개선 |

---

## ⚙️ 설정

```json
// config.json
{
  "enabled": true,
  "anonymous": true,
  "retention_days": 30,
  "collect": {
    "usage": true,
    "performance": true,
    "errors": true,
    "patterns": false
  },
  "exclude": {
    "file_contents": true,
    "user_inputs": true,
    "api_keys": true
  }
}
```

---

## 📊 메트릭 구조

### 일별 통계
```json
// daily/20260130.json
{
  "date": "2026-01-30",
  "sessions": {
    "count": 5,
    "total_duration_minutes": 320,
    "avg_duration_minutes": 64
  },
  "tokens": {
    "input": 125000,
    "output": 45000,
    "total": 170000
  },
  "tools": {
    "total_calls": 450,
    "by_type": {
      "Read": 120,
      "Write": 45,
      "Edit": 80,
      "Bash": 65,
      "Grep": 50,
      "Task": 30,
      "Other": 60
    }
  },
  "errors": {
    "count": 3,
    "resolved": 2,
    "ralph_loop_triggered": 1
  },
  "keywords": {
    "빠르게": 8,
    "고쳐": 5,
    "확인해": 12
  }
}
```

### 성능 메트릭
```json
// performance/perf_20260130.json
{
  "date": "2026-01-30",
  "response_time_ms": {
    "avg": 1200,
    "p50": 950,
    "p95": 2500,
    "p99": 4000
  },
  "tool_execution_ms": {
    "Read": { "avg": 50, "max": 200 },
    "Write": { "avg": 80, "max": 300 },
    "Bash": { "avg": 1500, "max": 10000 }
  },
  "context_usage": {
    "avg_percent": 45,
    "max_percent": 85,
    "dcp_triggers": 2
  }
}
```

---

## 📈 보고서 생성

### 일일 보고서
```bash
# 오늘의 사용 통계
/project-status --telemetry daily

# 특정 날짜
/project-status --telemetry daily --date 20260130
```

### 주간 보고서
```bash
# 이번 주 요약
/project-status --telemetry weekly
```

### 트렌드 분석
```bash
# 최근 7일 트렌드
/project-status --telemetry trend --days 7
```

---

## 🔒 프라이버시

### 수집하지 않는 데이터
- ❌ 파일 내용
- ❌ 사용자 입력 텍스트
- ❌ API 키, 비밀번호
- ❌ 개인 식별 정보

### 데이터 보관
- 로컬 저장만 (외부 전송 없음)
- 30일 후 자동 삭제
- 수동 삭제 가능

---

## 🔧 관리 명령어

```bash
# 텔레메트리 활성화/비활성화
claude config set telemetry.enabled false

# 데이터 삭제
claude telemetry clear --all

# 특정 기간 삭제
claude telemetry clear --before 20260101
```

---

**META**
- Category: telemetry
- Last Updated: 2026-01-30
- Version: 1.0.0
