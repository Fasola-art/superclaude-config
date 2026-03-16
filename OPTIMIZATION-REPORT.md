# Claude 성능 최적화 보고서

> 생성: 2026-02-16
> 대상: 코덱스-Claude 간 오류 패턴 분석

## 문제 진단

### 1. 근본 원인

| 원인 | 심각도 | 영향 |
|------|--------|------|
| 훅 실행 오버헤드 (34개) | CRITICAL | 매 도구 호출마다 최대 17개 Python 스크립트 실행 |
| MCP 서버 타임아웃 미설정 | CRITICAL | 네트워크 지연 시 전체 요청 블로킹 |
| 병렬 실행 설정 충돌 | HIGH | 설정값 불일치로 성능 저하 |
| 파일 I/O 경쟁 조건 | MEDIUM | 간헐적 오류 발생 |

---

## 적용된 수정 사항 (2026-02-16)

### ✅ 완료: MCP 서버 타임아웃 설정

```json
// servers.json 업데이트
"mysql": { "timeout": 30000 }
"postgresql": { "timeout": 30000 }
"github": { "timeout": 45000 }
"local-llm": { "timeout": 90000 }
"ollama": { "timeout": 60000 }
"playwright": { "timeout": 45000 }
"slack": { "timeout": 30000 }
"brave-search": { "timeout": 45000 }
"gdrive": { "timeout": 45000 }
"sentry": { "timeout": 30000 }
"linear": { "timeout": 30000 }
```

**효과**: 네트워크 지연 시 무한 대기 방지

### ✅ 완료: 동시성 설정 조정

```json
// settings.json 업데이트
"performance": {
  "maxConcurrentTasks": 8  // 4 → 8
}
```

**효과**: superclaude-config.json의 `personas.maxConcurrent: 8`과 일치

---

## 권장 사항 (단계적 적용)

### 🟡 PHASE 1: 훅 최적화 (즉시)

#### 비활성화 권장 훅 (성능 영향 큰 순)

**PostToolUse 그룹 (17개 → 10개)**:

```json
// 비활성화 권장 (7개)
// - format-python.py (린터가 대체 가능)
// - format-js-ts.py (린터가 대체 가능)
// - run-tests.py (명시적 실행 권장)
// - quality-gate.py (코드 리뷰 단계로 이동)
// - pattern-tracker.py (수동 분석으로 대체)
// - session-snapshot.py (session-saver.py와 중복)
// - background-notification.py (필수 아님)
```

**UserPromptSubmit 그룹 (9개 → 5개)**:

```json
// 비활성화 권장 (4개)
// - jarvis-morning-briefing.py (/j 명령어로 대체)
// - context-cleaner.py (자동화 불필요)
// - plan-mode-analyzer.py (필요 시에만 실행)
// - persona-activator.py (명시적 활성화 권장)
```

**기대 효과**:
- PostToolUse: 17개 → 10개 (41% 감소)
- UserPromptSubmit: 9개 → 5개 (44% 감소)
- 전체 훅: 34개 → 21개 (38% 감소)

### 🟡 PHASE 2: 훅 병렬화 (1주 이내)

현재 순차 실행되는 훅을 병렬 실행으로 변경:

```python
# 기존 (순차)
for hook in hooks:
    hook.run()

# 개선 (병렬)
import asyncio
await asyncio.gather(*[hook.run() for hook in hooks])
```

**대상 훅**:
- PostToolUse의 포매터 그룹 (format-python, format-js-ts)
- PreToolUse의 메모리 로더/주입기

**기대 효과**: 훅 실행 시간 60% 단축

### 🟡 PHASE 3: 파일 I/O 잠금 메커니즘 (2주 이내)

경쟁 조건 방지를 위한 잠금 구현:

```python
import filelock

lock = filelock.FileLock("~/.claude/.locks/session.lock")
with lock:
    # 파일 읽기/쓰기
```

**대상 파일**:
- session.json
- context-state.json
- agent-memory/*.json

---

## 모니터링 체크리스트

### 즉시 확인 (오늘)

- [ ] MCP 서버 연결 안정성 개선 확인
- [ ] 타임아웃 오류 발생 빈도 감소 확인
- [ ] Claude 응답 속도 체감 개선 확인

### 1주 후 확인

- [ ] 훅 비활성화 후 기능 정상 동작 확인
- [ ] 오류 발생 빈도 50% 이상 감소 확인
- [ ] 평균 응답 시간 측정 및 비교

### 2주 후 확인

- [ ] 파일 잠금 구현 후 경쟁 조건 해소 확인
- [ ] 장기 안정성 테스트 (24시간 연속 사용)

---

## 롤백 방안

모든 변경 사항은 Git으로 관리되며, 문제 발생 시 즉시 롤백 가능:

```bash
# MCP 타임아웃 롤백
git checkout HEAD~1 -- C:/Users/MSI/.claude/mcp-router/servers.json

# 성능 설정 롤백
git checkout HEAD~1 -- C:/Users/MSI/.claude/settings.json
```

---

## 예상 성능 개선

| 지표 | 현재 | 목표 | 개선율 |
|------|------|------|--------|
| MCP 타임아웃 오류 | 간헐적 | 0% | -100% |
| 평균 응답 시간 | ? | -30% | +30% |
| 훅 실행 시간 | 높음 | 낮음 | -60% |
| 오류 발생 빈도 | 가끔 | 드물게 | -70% |

---

## 추가 제안

### 장기 개선 과제

1. **훅 통합**: 유사 기능 훅들을 하나로 병합
   - `format-python` + `format-js-ts` → `format-all`
   - `session-snapshot` + `session-saver` → `session-manager`

2. **조건부 훅 실행**: 파일 타입/크기에 따라 선택적 실행
   ```json
   {
     "matcher": "Edit|Write",
     "condition": "file.size < 1MB && file.ext in ['.py', '.ts']",
     "hooks": ["format-code"]
   }
   ```

3. **훅 성능 프로파일링**: 각 훅의 실행 시간 측정 및 최적화
   ```python
   import time
   start = time.time()
   # 훅 로직
   print(f"Hook execution: {time.time() - start:.2f}s")
   ```

---

**작성자**: Claude Sonnet 4.5
**검토 필요**: 사용자 확인 후 PHASE 1 적용 여부 결정
