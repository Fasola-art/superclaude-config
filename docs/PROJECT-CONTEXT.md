# 프로젝트 컨텍스트 관리 (Project Context)

> 프로젝트 컨텍스트 유지 및 복원 전략

---

## 개요

프로젝트 컨텍스트는 작업의 연속성을 보장하고 효율적인 개발을 위해 필수적입니다.

---

## 컨텍스트 구성 요소

### 1. 프로젝트 메타데이터
```yaml
project:
  name: [프로젝트명]
  path: [경로]
  type: [nextjs | react | node | ...]
  created: [생성일]
  last_active: [마지막 활동일]
```

### 2. 작업 상태
```yaml
state:
  current_task: [현재 태스크]
  milestone: [현재 마일스톤]
  progress: [진행률]
  blockers: [차단 요소]
```

### 3. 파일 컨텍스트
```yaml
files:
  recently_modified:
    - path: [파일경로]
      modified: [수정일]
  frequently_accessed:
    - path: [파일경로]
      count: [접근횟수]
```

---

## 컨텍스트 저장 위치

```
~/.claude/
├── session-env/
│   ├── current-project.json
│   └── session-state.json
├── projects/
│   └── [project-hash]/
│       ├── context.json
│       └── history.json
└── file-history/
    └── [date]/
        └── changes.json
```

---

## 컨텍스트 복원

### 자동 복원
세션 시작 시 마지막 프로젝트 컨텍스트 자동 로드

### 수동 복원
```
/project-continue    # 마지막 프로젝트 계속
/recover            # 세션 복구
/sc:load --project  # 프로젝트 컨텍스트 로드
```

---

## 컨텍스트 정리

### DCP (Dynamic Context Pruning)
- 75%: 경고
- 90%: 자동 압축
- 95%: 강제 압축

### 보존 항목
- 현재 태스크
- 활성 TodoWrite
- 최근 수정 파일
- CLAUDE.md 규칙
