# Sessions 폴더

> **목적**: 대화 세션 이력 및 컨텍스트 데이터 저장소
> **갱신일**: 2026-01-30

---

## 📁 폴더 구조

```
sessions/
├── README.md           # 이 파일
├── active/             # 현재 활성 세션
│   └── {session-id}.json
├── completed/          # 완료된 세션
│   └── {YYYYMMDD}/
│       └── {session-id}.json
├── snapshots/          # 세션 스냅샷 (중요 지점)
│   └── {session-id}_{label}.json
└── exports/            # 내보낸 세션
    └── {session-id}.md
```

---

## 🎯 세션 유형

| 유형 | 설명 | 보관 기간 |
|------|------|----------|
| **active** | 현재 진행 중인 세션 | 세션 종료까지 |
| **completed** | 정상 완료된 세션 | 7일 |
| **snapshot** | 중요 지점 스냅샷 | 30일 |
| **exported** | 명시적으로 내보낸 세션 | 무기한 |

---

## 📋 세션 데이터 구조

```json
{
  "id": "session_abc123",
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T12:30:00Z",
  "status": "active",
  "project": {
    "path": "/Users/reim/projects/my-app",
    "name": "my-app"
  },
  "context": {
    "files_read": ["src/index.ts", "package.json"],
    "files_modified": ["src/components/Button.tsx"],
    "tasks_completed": 5,
    "tasks_pending": 2
  },
  "state": {
    "vibe": "focused",
    "personas_active": ["architect", "coder"],
    "mode": "implementation"
  },
  "metrics": {
    "tokens_used": 45000,
    "duration_minutes": 150,
    "tools_called": 78
  }
}
```

---

## 🔧 세션 관리 명령어

### 세션 저장
```bash
# 현재 세션 스냅샷
/recover --snapshot "before-refactor"

# 세션 내보내기 (마크다운)
/recover --export markdown
```

### 세션 복구
```bash
# 마지막 세션 이어가기
/project-continue

# 특정 스냅샷에서 복구
/recover --from snapshot_abc123_before-refactor
```

### 세션 조회
```bash
# 최근 세션 목록
/project-status --sessions

# 특정 세션 상세
/project-status --session abc123
```

---

## 🔄 자동 저장 정책

| 이벤트 | 동작 | 저장 위치 |
|--------|------|----------|
| **태스크 완료** | 자동 스냅샷 | snapshots/ |
| **Git 커밋** | 자동 스냅샷 | snapshots/ |
| **세션 종료** | 전체 저장 | completed/ |
| **컨텍스트 70%** | 자동 압축 | active/ |
| **에러 발생** | 상태 저장 | active/ |

---

## 📊 세션 메트릭

### 추적 항목
- 토큰 사용량 (입력/출력)
- 세션 지속 시간
- 도구 호출 횟수
- 파일 읽기/수정 횟수
- 태스크 완료율

### 보고서 생성
```bash
# 세션 요약 보고서
/project-status --report session

# 주간 활동 보고서
/project-status --report weekly
```

---

## ⚠️ 주의사항

- 민감한 정보는 세션 데이터에서 자동 마스킹
- 7일 이상 된 completed 세션은 자동 삭제
- 중요 세션은 archive/로 이동 권장

---

**META**
- Category: sessions
- Last Updated: 2026-01-30
- Version: 1.0.0
