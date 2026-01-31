---
description: 경제 지표 발표 일정 조회
---

# /calendar 명령어

향후 1개월 경제 지표 발표 일정을 조회하고 정리합니다.

## 실행 내용

1. **오늘/내일 주요 지표** - 긴급 알림
2. **이번 주 일정** - 주간 요약
3. **30일 일정표** - 마크다운 테이블 생성

## 추적 지표

### 🔴 CRITICAL (시장 급변동 가능)
- **CPI/Core CPI** - 매월 중순
- **비농업 고용 (NFP)** - 매월 첫째 금요일
- **FOMC 성명서** - 연 8회
- **GDP** - 분기별
- **PCE 물가지수** - 매월 말

### 🟠 HIGH
- 실업률, 실업수당 청구
- 소비자심리지수, 소매판매
- ISM 제조업/서비스업 PMI

### 🟡 MEDIUM
- 주택착공, 산업생산지수

## 사용법

```
/calendar        # 30일 일정표
/calendar week   # 이번 주만
/calendar today  # 오늘 일정
```

## 실행 스크립트

```bash
python3 ~/.claude/scripts/scheduled_collectors.py calendar
```

## 출력 위치
`~/.claude/modules/trading/data_sources/calendar/calendar_YYYYMMDD.md`

## FOMC 2026 일정
| 월 | 회의 일정 | 성명서 발표 |
|----|----------|-------------|
| 1월 | 27-28 | 28일 14:00 ET |
| 3월 | 17-18 | 18일 14:00 ET |
| 5월 | 5-6 | 6일 14:00 ET |
| 6월 | 16-17 | 17일 14:00 ET |
| 7월 | 28-29 | 29일 14:00 ET |
| 9월 | 15-16 | 16일 14:00 ET |
| 11월 | 3-4 | 4일 14:00 ET |
| 12월 | 15-16 | 16일 14:00 ET |
