---
description: "HANDOFF.md 자동 생성 - 다음 세션 인수인계 문서"
---

현재 세션을 분석하여 프로젝트 루트에 `HANDOFF.md`를 생성하세요.

## 생성 형식

```markdown
# HANDOFF - {날짜 YYYY-MM-DD HH:MM}

## Completed (완료 작업)
- 이번 세션에서 완료한 작업 목록 (구체적으로)

## Attempted (시도한 접근)
### 성공한 방법
- 효과있던 해결책

### 실패한 방법
- 실패한 접근법과 이유 (다음 세션에서 반복 방지)

## Next Steps (우선순위 순 다음 작업)
1. [HIGH] 즉시 처리 필요한 작업
2. [MED] 이번 주 내 처리
3. [LOW] 여유 시 처리

## Watch Out (주의사항)
- 알려진 버그 또는 임시 해결책
- 건드리지 말아야 할 파일/설정
- 특이한 환경 요구사항

## Recovery (다음 세션 재개 방법)
```bash
cat HANDOFF.md && /project-continue
```
```

## 실행 규칙

1. 현재 작업 디렉토리 루트에 `HANDOFF.md` 생성
2. 기존 파일 존재 시 `HANDOFF_{timestamp}.md`로 백업 후 덮어쓰기
3. 생성 완료 후 파일 경로와 주요 내용 요약 출력
4. **인간이 읽을 수 있는 Markdown 형식** (JSON 아님)
