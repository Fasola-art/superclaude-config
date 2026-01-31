# Dynamic Context Pruning (DCP) Rules

> SuperClaude v4.1 - 자동 컨텍스트 관리 시스템

---

## 개요

DCP (Dynamic Context Pruning)는 Claude Code 세션의 컨텍스트 창을 효율적으로 관리합니다.
컨텍스트 사용량에 따라 불필요한 정보를 자동으로 정리하여 세션 연속성을 보장합니다.

---

## 임계값 (Mac Studio Ultra M2 최적화)

| 레벨 | 임계값 | 동작 | 알림 |
|------|--------|------|------|
| 🟢 Normal | < 75% | 모니터링만 | 없음 |
| 🟡 Warning | 75% | 경고 표시 | `⚠️ 컨텍스트 75%` |
| 🔴 Critical | 90% | 자동 DCP 제안 | `🔴 컨텍스트 90% - 압축 권장` |
| ❌ Emergency | 95% | 강제 압축 | `🚨 컨텍스트 95% - 강제 압축` |

---

## DCP 전략

### 1. 중복 제거 (Deduplication)

```yaml
deduplication:
  file_reads:
    rule: "동일 파일 반복 읽기 → 최신 결과만 유지"
    action: "이전 Read 결과 제거"
  bash_outputs:
    rule: "동일 명령어 반복 → 마지막 결과만 유지"
    action: "이전 Bash 출력 제거"
  grep_results:
    rule: "동일 패턴 검색 → 최신 결과만 유지"
    action: "이전 Grep 결과 제거"
```

### 2. 에러 정리 (Error Cleanup)

```yaml
error_cleanup:
  resolved_errors:
    rule: "해결된 에러 메시지 → 삭제"
    condition: "동일 명령어 성공 시"
  duplicate_errors:
    rule: "동일 에러 반복 → 첫 번째 + 횟수만 유지"
    format: "[에러 메시지] (N회 발생)"
  stack_traces:
    rule: "3회 이상 반복 스택 트레이스 → 요약으로 대체"
    action: "핵심 라인만 유지"
```

### 3. 파일 요약 (File Summarize)

```yaml
file_summarize:
  large_files:
    threshold: 2000  # 라인
    rule: "2000+ 라인 파일 → 관련 부분만 유지"
    action: "요청된 섹션만 보존"
  log_outputs:
    threshold: 50  # 라인
    rule: "로그 출력 → 마지막 50줄만 유지"
    action: "이전 로그 제거"
  config_files:
    rule: "설정 파일 → 변경된 부분만 유지"
    action: "diff 형식으로 압축"
```

---

## 보존 항목 (절대 삭제 금지)

```yaml
preserve_always:
  - "현재 태스크 컨텍스트"
  - "활성 TodoWrite 항목"
  - "최근 수정 파일 목록"
  - "CLAUDE.md 핵심 규칙"
  - "현재 에러 및 수정 시도"
  - "사용자 명시적 요청 내용"
```

---

## 자동 실행 조건

### 90% 자동 DCP

```yaml
auto_dcp_at_90:
  trigger: "컨텍스트 사용량 >= 90%"
  actions:
    1: "중복 제거 전략 실행"
    2: "에러 정리 전략 실행"
    3: "파일 요약 전략 실행"
  report:
    format: "DCP 실행: [X] 토큰 확보. 현재 사용량: [Y]%"
```

### 95% 긴급 압축

```yaml
emergency_at_95:
  trigger: "컨텍스트 사용량 >= 95%"
  actions:
    1: "모든 DCP 전략 강제 실행"
    2: "오래된 파일 내용 제거"
    3: "세션 아카이브 생성"
  warning: "세션 연속성 위험 - 즉시 정리 필요"
```
