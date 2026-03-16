---
description: "실험적 방향 분기점 문서화 - FORK_CONTEXT.md 생성 + Git 브랜치 안내"
---

현재 세션 상태를 스냅샷으로 저장하고 실험적 방향을 시도할 분기점을 만드세요.

$ARGUMENTS

## 실행 순서

### 1. FORK_CONTEXT.md 생성

현재 디렉토리에 `FORK_CONTEXT.md` 생성:

```markdown
# FORK CONTEXT - {타임스탬프}

## 분기 이유
{사용자 제공 이유 또는 "실험적 접근 시도"}

## 현재 상태 스냅샷
- 작업 중인 파일 목록
- 현재까지 완료된 작업
- 미해결 문제

## 실험 목표
{이 분기에서 검증하려는 가설}

## 복귀 방법 (실패 시)
```bash
git checkout {현재 브랜치}
cat FORK_CONTEXT.md  # 원래 상태 확인
```
```

### 2. Git 브랜치 생성 안내

```bash
# 실험 브랜치 생성 (사용자가 직접 실행)
git checkout -b experiment/$(date +%Y%m%d-%H%M)
```

### 3. 완료 메시지 출력

- FORK_CONTEXT.md 경로
- 실험 브랜치 명령어 (복사 가능)
- 복귀 방법 안내

## 사용 예시

```
/fork "새로운 API 구조 실험"
/fork "성능 최적화 접근법 A 테스트"
```
