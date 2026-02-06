# Advanced Scenarios (4-6)

> 고급 사용 시나리오

## Scenario 4: Infinite Loop Prevention

```bash
> 연속 오류가 발생하는 복잡한 작업

Flow:
1. 첫 번째 실패:
   └── ralph-loop-checker: 상태 기록 (failures: 1)

2. 두 번째 실패:
   └── 상태 기록 (failures: 2)

3. 세 번째 실패:
   └── ⚠️ Loop:3/5 경고 출력
   └── 사용자 알림

4. 네 번째 실패:
   └── ⚠️ Loop:4/5 경고

5. 다섯 번째 실패:
   └── 🛑 Loop:5 → 수동 개입
   └── 자동 실행 중단
   └── 사용자 수동 개입 요청

복구:
- 오류 수정 후 성공 시 자동 리셋
- "fix" 키워드로 Error KB 기반 수정 시도
```

## Scenario 5: PRD-Based Project Start

```bash
> "start project based on this PRD document"
> [PRD.md 파일 첨부]

Flow:
1. plan-mode-analyzer:
   • PRD 파일 패턴 감지: .*PRD\.md$ → confidence: 90%
   • 기능 목록 감지: features_count: 12
   • 분석 깊이 결정: 'think-hard'

2. 자동 플랜 모드 진입:
   {
     "status": "detected",
     "type": "file",
     "confidence": 0.9,
     "features_count": 12,
     "analysis_depth": "think-hard",
     "action": "enter_plan_mode"
   }

3. 프로젝트 계획:
   • 기능 구현 순서 결정
   • 의존성 분석
   • 마일스톤 설정

4. TodoWrite로 태스크 생성:
   [ ] 프로젝트 초기화
   [ ] 기능 1 구현
   [ ] 기능 2 구현
   ...

5. 순차적 구현 시작
```

## Scenario 6: Deep Search Bug Investigation

```bash
> "ds find this memory leak cause"

Flow:
1. keyword-detector: "ds" 감지
   🎯 mode:deepsearch
   → 활성화 페르소나: explorer

2. explorer 페르소나로 딥 탐색:
   • 코드 히스토리 분석
   • 관련 이슈 검색
   • 메모리 프로파일링 제안
   • 의심 지점 식별

3. 단계별 분석 리포트:
   • Step 1: 증상 분석
   • Step 2: 관련 코드 추적
   • Step 3: 근본 원인 가설
   • Step 4: 검증 방법 제안

4. 해결책 제안
```

---

**Related**: [scenarios-basic.md](scenarios-basic.md), [orchestrator-workflow.md](orchestrator-workflow.md)
