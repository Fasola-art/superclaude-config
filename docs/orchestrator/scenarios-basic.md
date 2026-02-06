# Basic Scenarios (1-3)

> 일반적인 사용 시나리오

## Scenario 1: Quick Code Fix

```bash
> "qk change login button color to blue"

Flow:
1. keyword-detector: "qk" 감지
   🎯 vibe:빠르게 → action: skip_validation
2. W-R 루프 스킵
3. Edit 즉시 실행
4. 최소 PostToolUse 훅
5. ✅ 완료

예상 시간: 5초
```

## Scenario 2: Security-Focused API Development

```bash
> "create user payment API endpoint"

Flow:
1. writer-reviewer-hook: 'api' 키워드 감지
   → 코드 타입: backend
   → 가중치: security 40%, quality 25%, perf 25%, a11y 10%

2. Writer가 코드 생성

3. 4-Agent 병렬 리뷰:
   - Quality Agent: 코드 품질 검사
   - Security Agent: 인증, SQL 인젝션, XSS 검사 (가중치 40%)
   - Performance Agent: 응답 시간, 메모리 사용
   - Accessibility Agent: API 응답 형식

4. 점수 계산:
   1차: 0.72 < 0.85 → 재작성
   2차: 0.81 < 0.85 → 재작성
   3차: 0.88 ≥ 0.85 → ✅ 완료

5. PostToolUse:
   - quality-gate.py 실행
   - run-tests.py 실행

예상 시간: 2-3분
```

## Scenario 3: Parallel Analysis Work

```bash
> "para analyze this codebase, document it, and generate tests"

Flow:
1. keyword-detector: "para" 감지
   🎯 vibe:동시에 → action: parallel_agents

2. 3개 Task 동시 실행:
   ┌────────────────────────────────────────────┐
   │ Task 1: code-explorer                      │
   │ • 코드베이스 구조 분석                     │
   │ • 의존성 매핑                              │
   │ • 아키텍처 문서화                          │
   ├────────────────────────────────────────────┤
   │ Task 2: sc:document                        │
   │ • README 생성                              │
   │ • API 문서화                               │
   │ • 사용 가이드                              │
   ├────────────────────────────────────────────┤
   │ Task 3: generate-tests                     │
   │ • 함수별 테스트 케이스                     │
   │ • 엣지 케이스                              │
   │ • 통합 테스트                              │
   └────────────────────────────────────────────┘

3. 결과 병합 후 반환

예상 시간: 순차 대비 60% 감소
```

---

**Related**: [scenarios-advanced.md](scenarios-advanced.md), [vibe-mode-keywords.md](vibe-mode-keywords.md)
