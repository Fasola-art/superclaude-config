# Hooks 자동화 시스템

> 17개 Hook 상세 정의

---

## Hook 트리거 유형

| 트리거 | 시점 | Hook 수 |
|--------|------|---------|
| UserPromptSubmit | 사용자 프롬프트 제출 시 | 7개 |
| PreToolUse | 도구 실행 전 | 2개 |
| PostToolUse | 도구 실행 후 | 8개 |
| Stop | 세션 종료 시 | 1개 |

---

## UserPromptSubmit Hooks (7개)

### 1. jarvis-morning-briefing.py
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "모닝 브리핑 생성"
timeout: 5000ms
actions:
  - 일일 요약 생성
  - 미완료 태스크 알림
  - 예정 작업 표시
```

### 2. plan-mode-analyzer.py
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "PRD 감지 → 플랜 모드 진입"
timeout: 3000ms
detection:
  keywords: ["PRD", "요구사항", "프로젝트 만들어"]
  file_patterns: ["*.prd.md", "PRD.md"]
actions:
  - PRD 문서 감지
  - 플랜 모드 자동 진입
  - 분석 깊이 결정
```

### 3. context-cleaner.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "컨텍스트 자동 정리"
timeout: 2000ms
thresholds:
  warning: 75%
  critical: 90%
  emergency: 95%
actions:
  - 컨텍스트 사용량 체크
  - DCP 전략 실행
  - 정리 결과 보고
```

### 4. keyword-detector.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Vibe/Mode 키워드 감지"
timeout: 1000ms
keywords:
  vibe: 13개
  mode: 4개
actions:
  - 키워드 파싱
  - 해당 동작 트리거
  - 페르소나 활성화
```

### 5. persona-activator.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "페르소나 자동 활성화"
timeout: 1500ms
rules:
  max_concurrent: 3
  priority: [security, architect, analyzer]
  security_keywords: [auth, login, password, token]
actions:
  - 컨텍스트 분석
  - 페르소나 선택
  - 페르소나 활성화
```

### 6. todo-continuation-enforcer.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Todo 지속성 검증"
timeout: 1000ms
actions:
  - 미완료 Todo 확인
  - 연속성 보장
  - 누락 태스크 알림
```

### 7. auto-update-checker.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "업데이트 확인"
timeout: 5000ms
frequency: "1일 1회"
actions:
  - 버전 체크
  - 업데이트 알림
  - 변경 로그 표시
```

---

## PreToolUse Hooks (2개)

### 1. writer-reviewer-hook.py
```yaml
trigger: PreToolUse
matcher: "Edit|Write|MultiEdit"
purpose: "Writer-Reviewer Loop 활성화"
timeout: 30000ms
config:
  target_score: 0.85
  max_iterations: 10
actions:
  - 코드 타입 감지
  - 4-Agent 검토 실행
  - 점수 계산 및 반복
```

### 2. error-warning-hook.js
```yaml
trigger: PreToolUse
matcher: "Edit|Write|MultiEdit"
purpose: "Error KB 기반 경고"
timeout: 2000ms
actions:
  - 유사 에러 패턴 검색
  - 사전 경고 표시
  - 권장 사항 제안
```

---

## PostToolUse Hooks (8개)

### 1. jarvis-work-tracker.py
```yaml
trigger: PostToolUse
matcher: ".*"
purpose: "작업 추적"
timeout: 1000ms
actions:
  - 작업 로깅
  - 통계 업데이트
  - 진행률 계산
```

### 2. error-auto-resolver.js
```yaml
trigger: PostToolUse
matcher: "Bash|Task"
purpose: "Ralph Loop - 에러 자동 해결"
timeout: 30000ms
config:
  max_retries: 10
  similarity_threshold: 0.70
actions:
  - 에러 감지
  - Error KB 검색
  - 자동 해결 시도
```

### 3. ralph-loop-checker.js
```yaml
trigger: PostToolUse
matcher: "Bash|Task"
purpose: "무한 루프 감지"
timeout: 1000ms
config:
  max_consecutive_failures: 5
actions:
  - 실패 횟수 추적
  - 무한 루프 감지
  - 강제 중단
```

### 4. jarvis-task-completion.py
```yaml
trigger: PostToolUse
matcher: "TodoWrite|Bash|Write|Edit"
purpose: "태스크 완료 처리"
timeout: 2000ms
actions:
  - 태스크 상태 업데이트
  - 완료 알림
  - 다음 태스크 제안
```

### 5. session-snapshot.js
```yaml
trigger: PostToolUse
matcher: "TodoWrite|Bash|Write|Edit"
purpose: "세션 자동 스냅샷"
timeout: 3000ms
config:
  max_snapshots: 10
actions:
  - 상태 캡처
  - 스냅샷 저장
  - 오래된 스냅샷 정리
```

### 6. quality-gate.js
```yaml
trigger: PostToolUse
matcher: "Write|Edit|MultiEdit"
purpose: "8단계 품질 검증"
timeout: 60000ms
gates: [Syntax, Type, Lint, Security, Test, Performance, Docs, Integration]
actions:
  - 게이트 순차 실행
  - 실패 시 알림
  - 결과 리포트
```

### 7. pattern-tracker.js
```yaml
trigger: PostToolUse
matcher: "Task"
purpose: "패턴 추적/학습"
timeout: 2000ms
actions:
  - 성공 패턴 기록
  - 실패 패턴 기록
  - 패턴 분석
```

### 8. background-notification.js
```yaml
trigger: PostToolUse
matcher: "Task"
purpose: "백그라운드 작업 알림"
timeout: 1000ms
actions:
  - 백그라운드 작업 완료 감지
  - 알림 전송
  - 결과 요약
```

---

## Stop Hook (1개)

### todo-continuation-enforcer.js
```yaml
trigger: Stop
purpose: "미완료 Todo 저장"
timeout: 5000ms
actions:
  - 미완료 태스크 저장
  - 세션 상태 저장
  - 복구 정보 기록
```

---

## Hook 설정 예시

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/UserPromptSubmit/keyword-detector.py",
            "timeout": 1000
          }
        ]
      }
    ]
  }
}
```
