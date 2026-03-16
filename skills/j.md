---
name: j
description: JARVIS - 개인 비서 자동화 시스템
version: "2.1.0"
triggers:
  - /j
  - jarvis
  - 자비스
allowed_tools:
  - Bash
  - Read
  - Write
  - Edit
---

# JARVIS (Just A Rather Very Intelligent System)

개인 비서 자동화 시스템 - 작업/일정/습관 관리, 자율 실행, ML 예측

## Quick Start

| 명령 | 설명 |
|------|------|
| `/j` | 상세 브리핑 (어제요약, 일정, 작업, AI추천) |
| `/j task "제목"` | 작업 추가 |
| `/j tasks` | 작업 목록 |
| `/j done <id>` | 작업 완료 |
| `/j event "제목" 날짜` | 일정 추가 |
| `/j events` | 일정 목록 |
| `/j remember "내용"` | 컨텍스트 저장 |
| `/j recall` | 컨텍스트 복원 |
| `/j do "명령"` | 자율 실행 |

**상세 기능**: [j-actions.md](j-actions.md), [j-advanced.md](j-advanced.md)

## Core Execution

### 브리핑

```bash
# 상세 브리핑 (기본)
cd C:/Users/MSI/.claude/jarvis && python briefing.py

# 간단 브리핑
cd C:/Users/MSI/.claude/jarvis && python briefing.py --simple
```

### 작업 관리

```python
import sys; sys.path.insert(0, "C:/Users/MSI/.claude/jarvis")
from memory import TaskManager

TaskManager.add_task("작업 제목", priority=2)  # 추가
tasks = TaskManager.get_pending_tasks()        # 목록
TaskManager.complete_task(task_id)             # 완료
```

### 일정 관리

```python
from memory import CalendarManager

CalendarManager.add_event("일정", "2026-02-05 14:00", event_type="meeting")
events = CalendarManager.get_today_events()
```

## Output Format

브리핑은 다음 섹션 포함:
- 📊 **어제 작업 요약**: 세션 수, 작업 시간
- 📅 **오늘 일정**: 시간, 제목, 장소
- 📋 **대기 작업**: 🔴 높은 우선순위 (마감일, 설명), 🟡 일반
- 🧠 **AI 추천**: ML 기반 다음 행동 예측 (신뢰도 %)
- ⚙️ **시스템**: 현재 시각, DB 상태

## Reference

| 리소스 | 경로 |
|--------|------|
| 액션 상세 | [j-actions.md](j-actions.md) |
| 고급 기능 | [j-advanced.md](j-advanced.md) |
| 소스 코드 | `C:/Users/MSI/.claude/jarvis/` |
| 데이터베이스 | `C:/Users/MSI/.claude/jarvis/memory/jarvis.db` |
