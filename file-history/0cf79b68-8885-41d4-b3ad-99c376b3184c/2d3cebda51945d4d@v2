# 세션 관리 시스템

> 자동 스냅샷 및 복구 전략

---

## 자동 스냅샷 트리거

```yaml
triggers:
  - "Todo 완료 시"
  - "Git commit 시"
  - "파일 수정 시"
  - "10분 주기 자동"
```

---

## 설정

```yaml
session_recovery:
  auto_snapshot: true
  max_snapshots: 10
  auto_resume: true
  snapshot_interval: 600  # 초 (10분)
```

---

## 스냅샷 내용

```yaml
snapshot_contents:
  - current_task: "현재 진행 중인 태스크"
  - todo_items: "TodoWrite 항목"
  - modified_files: "수정된 파일 목록"
  - context_summary: "컨텍스트 요약"
  - state_md: "STATE.md 내용"
  - timestamp: "스냅샷 시간"
```

---

## 복구 명령어

| 명령어 | 설명 |
|--------|------|
| /recover | 마지막 스냅샷 복구 |
| /recover --list | 스냅샷 목록 보기 |
| /recover --id X | 특정 스냅샷 복구 |
| 계속 | 이전 작업 계속 (Vibe 키워드) |

---

## 복구 프로세스

```
1. 스냅샷 선택
   └── 기본: 마지막 스냅샷
   └── 옵션: --id로 특정 스냅샷 선택

2. 상태 복원
   ├── STATE.md 로드
   ├── TodoWrite 항목 복원
   └── 컨텍스트 요약 로드

3. 작업 재개
   ├── 중단점 확인
   ├── 미완료 태스크 표시
   └── 사용자 확인 후 계속
```

---

## 스냅샷 저장 위치

```
~/.claude/shell-snapshots/
├── snapshot_2026-01-29_12-00-00.json
├── snapshot_2026-01-29_12-10-00.json
├── snapshot_2026-01-29_12-20-00.json
└── ...
```

---

## 스냅샷 형식

```json
{
  "id": "snap_abc123",
  "timestamp": "2026-01-29T12:00:00.000Z",
  "session_id": "session_xyz789",
  "task": {
    "current": "API 엔드포인트 구현",
    "progress": 60
  },
  "todos": [
    {
      "id": 1,
      "status": "completed",
      "subject": "User 모델 정의"
    },
    {
      "id": 2,
      "status": "in_progress",
      "subject": "Auth 미들웨어 구현"
    }
  ],
  "modified_files": [
    "src/models/user.ts",
    "src/middleware/auth.ts"
  ],
  "context_summary": "사용자 인증 시스템 구현 중...",
  "state_md_hash": "sha256:abc123..."
}
```

---

## 자동 정리

```yaml
cleanup:
  trigger: "max_snapshots 초과 시"
  strategy: "가장 오래된 스냅샷 삭제"
  preserve: "마지막 10개"
```
