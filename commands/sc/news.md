---
description: 뉴스 수집 및 요약 실행
---

# /news 명령어

뉴스 및 시장 데이터를 수집하고 요약합니다.

## 실행 내용

1. **Bloomberg 뉴스** - 시장, 경제, 기술 카테고리 속보
2. **Finviz 뉴스** - 주식 시장 뉴스 및 가격
3. **FRED 지표** - 주요 경제 지표 체크

## 사용법

```
/news           # 전체 뉴스 수집
/news market    # 시장 뉴스만
/news breaking  # 속보만
```

## 실행 스크립트

아래 명령을 실행하여 뉴스를 수집합니다:

```bash
python3 ~/.claude/scripts/scheduled_collectors.py all
```

## 출력 형식

### 속보 (있는 경우)
- 🚨 [카테고리] 헤드라인

### 시장 요약
- 📈/📉 주요 지수 변동
- 섹터별 동향

### 뉴스 하이라이트
- 긍정/부정/중립 분류
- 중요도별 정렬

## 데이터 저장 위치
- Bloomberg: `~/.claude/modules/news-collector/archive/bloomberg/`
- Finviz: `~/.claude/modules/news-collector/archive/finviz/`
