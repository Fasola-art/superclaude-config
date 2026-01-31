---
description: 일일 경제 보고서 생성
---

# /report 명령어

일일 경제 보고서를 생성합니다. 매일 저녁 10시 자동 실행됩니다.

## 보고서 구성

### 1️⃣ 오늘 발표 경제 지표
| 항목 | 설명 |
|------|------|
| 예상치 | 시장 컨센서스 |
| 실제 | 발표된 실제 값 |
| 이전 | 전기 발표 값 |
| 서프라이즈 | 실제 - 예상 |
| 영향 | 시장 영향 평가 |

### 2️⃣ 전문가 의견 (3-5인)
- 연준 (FOMC) - 통화정책
- 주요 IB (Goldman, JP Morgan) - 시장 전망
- 저명 투자자 (달리오, 버핏 등) - 매크로 뷰

### 3️⃣ 향후 경제 전망
- 주식 (미국): 지지/저항 레벨, 리스크
- 채권: 금리 전망
- 외환: 달러 방향성
- 원자재: 유가, 금 전망

### 4️⃣ 투자자 참고사항
- 포지션 관리 팁
- 시즌성 고려사항
- 기술적 분석 포인트
- 자금 흐름 모니터링

### 5️⃣ 내일 예정 이벤트
- 경제 지표 발표 일정
- 중요도별 분류 (🔴 critical, 🟠 high)

### 6️⃣ 오늘의 주요 뉴스
- Bloomberg/Finviz 주요 헤드라인
- 감성 분석 (📈 긍정/📉 부정)

## 사용법

```
/report          # 보고서 생성
/report today    # 오늘 보고서 보기
/report preview  # 미리보기
```

## 실행 스크립트

```bash
python3 ~/.claude/scripts/scheduled_collectors.py report
```

## 보고서 저장 위치
`~/.claude/modules/trading/reports/daily/daily_report_YYYY-MM-DD.md`

## 자동 실행
- **매일 22:00** (저녁 10시)
- 서비스: `com.superclaude.evening-report`
