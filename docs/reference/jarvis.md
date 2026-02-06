# Jarvis System

> 개인 비서 시스템 - 작업 연속성, ML 예측, 자율 태스크 실행

## Folder Structure

```
~/.claude/jarvis/
├── memory/
│   ├── manager.py         # Memory manager (SQLite)
│   ├── jarvis.db          # SQLite database
│   └── ml_predictor.py    # ML pattern learning & prediction
├── automation/
│   ├── browser.py         # Browser automation
│   └── task_executor.py   # Task execution engine
├── data/
│   ├── tasks.json         # Task list
│   └── calendar.json      # Calendar
├── daemon.py              # Background Daemon
└── test_jarvis.py         # Tests
```

## Core Features (6 Phases)

| Phase | Feature | Description |
|-------|---------|-------------|
| 1 | Morning Briefing | 어제 작업/오늘 일정 자동 표시 |
| 2 | Work Continuity | `/j remember` - 마지막 작업 컨텍스트 복원 |
| 3 | Auto Task Exec | `/j do <task>` - 의도 분석, 자동 실행 |
| 4 | ML Learning | scikit-learn 기반 시간-패턴 학습 |
| 5 | Life Management | `/j book`, `/j plan` - 예약/이벤트 계획 |
| 6 | Background Daemon | 자동 재학습/백업/패턴 업데이트 |

## Commands

| Command | Purpose |
|---------|---------|
| `/j` | Jarvis 호출 |
| `/j briefing` | 상세 브리핑 |
| `/j remember` | 작업 연속성 확인 |
| `/j do <task>` | 태스크 실행 |
| `/j book <item>` | 레스토랑/영화/호텔 예약 |
| `/j plan <event>` | 여행/파티/프로젝트 계획 |

## Database Schema

| Table | Purpose |
|-------|---------|
| work_sessions | 작업 세션 기록 (시간, 프로젝트, 파일) |
| usage_patterns | ML 학습 패턴 (요일, 시간, 태스크 유형, 빈도) |
| tasks | 태스크 목록 (제목, 상태, 우선순위, 마감일) |
| calendar_events | 캘린더 (제목, 시간, 장소, 이벤트 유형) |

## ML Learning Features

- scikit-learn 기반 패턴 학습
- 시간/요일 행동 예측 (신뢰도 포함)
- 피크 타임 분석
- 최소 10개 패턴 필요

## Privacy

- **Local-First**: 모든 데이터 로컬 SQLite에 저장
- **No Cloud**: 외부 서버 전송 없음
- **Optional Encryption**: 데이터베이스 암호화 가능

---

**Related**: [index.md](index.md)
