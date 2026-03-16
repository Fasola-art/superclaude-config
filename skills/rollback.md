---
name: rollback
description: 자동 스냅샷 롤백 - 최근 안전 포인트로 복구
version: "1.0.0"
triggers:
  - /rollback
  - 롤백해줘
  - 이전 상태로 되돌려줘
  - 되돌려줘
---
# Rollback 시스템

## 사용법

```bash
# 스냅샷 목록 확인
python ~/.claude/scripts/rollback.py list

# 마지막 스냅샷으로 복구
python ~/.claude/scripts/rollback.py undo

# 특정 스냅샷으로 복구 (해시 앞 8자리)
python ~/.claude/scripts/rollback.py undo abc12345

# 현재 git 롤백 포인트 확인
python ~/.claude/scripts/rollback.py status
```

## 자동 스냅샷 트리거

| 조건 | 동작 |
|------|------|
| `rm -rf`, `git reset --hard` 등 위험 명령어 | 즉시 스냅샷 |
| Write/Edit/MultiEdit (파일 수정) | 5분 쓰로틀링 적용 스냅샷 |
| git repo 외부 작업 | 스냅샷 건너뜀 |

## 실행 지침

1. `python ~/.claude/scripts/rollback.py list` 실행
2. 복구할 시점의 해시 확인
3. `undo [hash]` 로 복구
4. 복구 후 `git status` 로 상태 확인
