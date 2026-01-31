---
description: "세션 또는 시스템 복구 (Recover session or system)"
argument-hint: "[session_id]"
---

# 세션 복구

중단된 세션을 복구하거나 시스템 상태를 복원합니다.

## 동작

1. `~/.claude/sessions/` 에서 세션 이력 검색
2. `~/.claude/shell-snapshots/` 에서 쉘 상태 복원
3. `~/.claude/file-history/` 에서 파일 변경 이력 확인
4. 마지막 안정 상태로 복원

## 복구 유형

### 세션 복구
```
/recover              # 마지막 세션 복구
/recover session_id   # 특정 세션 복구
```

### 파일 복구
```
/recover --file path/to/file   # 특정 파일 이전 버전 복원
```

### 전체 복구
```
/recover --full   # 전체 시스템 상태 복원
```

## 출력 형식

```
🔄 세션 복구

세션 ID: [session_id]
시작 시간: [timestamp]
마지막 활동: [timestamp]

복구 항목:
- 프로젝트 경로: [path]
- 태스크 상태: [N]개 복원
- 파일 이력: [N]개 확인
- 쉘 상태: 복원 완료

복구가 완료되었습니다. 이전 작업을 계속하시겠습니까?
```
