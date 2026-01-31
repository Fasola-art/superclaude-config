---
name: daily
description: 자주 쓰는 경로 모음. 경제 시황, 트레이딩 모듈, 페르소나, API 키 등 주요 폴더 경로를 빠르게 확인.
license: MIT
---

자주 쓰는 경로 모음을 보여줍니다.

## 주요 경로

| 용도 | 경로 |
|------|------|
| **경제 시황** | `/Users/reim/.claude/modules/trading/reports/daily/` |
| **트레이딩 모듈** | `/Users/reim/.claude/modules/trading/` |
| **뉴스 모듈** | `/Users/reim/.claude/modules/news-collector/` |
| **텔레그램 모듈** | `/Users/reim/.claude/modules/telegram/` |
| **페르소나** | `/Users/reim/.claude/personas/` |
| **스킬** | `/Users/reim/.claude/skills/` |
| **API 키** | `/Users/reim/.claude/credentials/api-keys.json` |
| **설정** | `/Users/reim/.claude/settings.json` |

## 빠른 열기

```bash
# 경제 시황 폴더
open /Users/reim/.claude/modules/trading/reports/daily/

# 트레이딩 모듈
open /Users/reim/.claude/modules/trading/

# 페르소나 폴더
open /Users/reim/.claude/personas/

# 스킬 폴더
open /Users/reim/.claude/skills/

# API 키 파일
open /Users/reim/.claude/credentials/api-keys.json
```

## 오늘 시황 파일

```bash
# 오늘 날짜 시황
cat /Users/reim/.claude/modules/trading/reports/daily/outlook_$(date +%Y-%m-%d).json

# 최신 시황
ls -t /Users/reim/.claude/modules/trading/reports/daily/outlook_*.json | head -1
```
