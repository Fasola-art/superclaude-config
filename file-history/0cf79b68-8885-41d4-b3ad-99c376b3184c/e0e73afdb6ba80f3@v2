# SuperClaude 키워드 트리거 시스템

> Vibe Keywords (13개) + Mode Keywords (4개) 상세 정의

---

## Vibe Keywords (13개)

### 1. 빠르게 (qk, quick)
```yaml
trigger: ["빠르게", "qk", "quick", "급하게", "바로"]
action:
  - 검증 단계 생략
  - Writer-Reviewer 최소 모드 (3회 반복)
  - 즉시 실행
use_case: "빠르게 로그인 폼 만들어줘"
```

### 2. 실험 (exp)
```yaml
trigger: ["실험", "exp", "시험", "테스트해볼게"]
action:
  - 현재 상태 스냅샷 생성
  - 실험 코드 실행
  - 롤백 옵션 제공
use_case: "실험 모드로 새 알고리즘 적용해봐"
```

### 3. 동시에 (para)
```yaml
trigger: ["동시에", "para", "병렬로", "한꺼번에"]
action:
  - 적응형 병렬 실행 활성화
  - 독립 태스크 동시 처리
  - 의존성 자동 감지
use_case: "동시에 3개 컴포넌트 만들어줘"
```

### 4. 고쳐 (fix)
```yaml
trigger: ["고쳐", "fix", "수정해", "버그"]
action:
  - Error KB 검색 (Jaccard 70%+)
  - Ralph Loop 활성화 (최대 10회)
  - 자동 수정 시도
use_case: "이 에러 고쳐줘"
```

### 5. 되돌려 (undo)
```yaml
trigger: ["되돌려", "undo", "롤백", "취소해"]
action:
  - 마지막 스냅샷 조회
  - 롤백 실행
  - 변경 사항 보존 옵션
use_case: "방금 변경 되돌려줘"
```

### 6. 계속 (cont)
```yaml
trigger: ["계속", "cont", "이어서", "계속해"]
action:
  - STATE.md 복원
  - 이전 컨텍스트 로드
  - 중단점부터 재개
use_case: "어제 작업 계속해줘"
```

### 7. 확인해 (chk)
```yaml
trigger: ["확인해", "chk", "검증해", "체크해"]
action:
  - TypeScript 타입 검사
  - ESLint 검사
  - Build 검사
  - Bundle 크기 분석
use_case: "전체 코드 확인해줘"
```

### 8. 테스트해 (tst)
```yaml
trigger: ["테스트해", "tst", "테스트 실행", "test"]
action:
  - 관련 테스트 파일 탐색
  - 테스트 실행
  - 커버리지 리포트
use_case: "auth 모듈 테스트해줘"
```

### 9. 배포해 (dep)
```yaml
trigger: ["배포해", "dep", "deploy", "릴리즈"]
action:
  - 배포 체크리스트 실행
  - Performance 검사
  - ROADMAP.md 업데이트
use_case: "스테이징에 배포해줘"
```

### 10. 정리해 (clean)
```yaml
trigger: ["정리해", "clean", "클린업", "청소해"]
action:
  - 미사용 import 제거
  - console.log 제거
  - 데드 코드 제거
  - 포맷팅
use_case: "이 파일 정리해줘"
```

### 11. 성능 (perf)
```yaml
trigger: ["성능", "perf", "performance", "최적화"]
action:
  - 전체 프로젝트 성능 분석
  - 병목 지점 식별
  - 자동 수정 제안
use_case: "성능 분석해줘"
```

### 12. 계획 (plan)
```yaml
trigger: ["계획", "plan", "플랜", "설계"]
action:
  - .planning/ 디렉토리 생성
  - PROJECT.md 생성
  - ROADMAP.md 생성
  - STATE.md 생성
use_case: "프로젝트 계획 세워줘"
```

### 13. 분석 (map)
```yaml
trigger: ["분석", "map", "매핑", "구조 파악"]
action:
  - 코드베이스 전체 분석
  - 7개 문서 자동 생성
  - 의존성 그래프
use_case: "이 프로젝트 분석해줘"
```

---

## Mode Keywords (4개)

### 1. ultrawork (ulw)
```yaml
trigger: ["ultrawork", "ulw", "울트라워크", "최대성능"]
activated_personas: [explorer, librarian, analyzer]
behavior:
  - 병렬 실행 최대화
  - 모든 분석 도구 활성화
  - 깊은 검색 모드
use_case: "ultrawork 모드로 전체 리팩토링해줘"
```

### 2. deepsearch (ds)
```yaml
trigger: ["deepsearch", "ds", "딥서치", "깊은검색"]
activated_personas: [explorer]
behavior:
  - /research 스킬 활성화
  - 웹 검색 포함
  - 문서 크롤링
use_case: "deepsearch로 최신 React 패턴 조사해줘"
```

### 3. strategic (str)
```yaml
trigger: ["strategic", "str", "전략", "전략적"]
activated_personas: [architect]
behavior:
  - 트레이드오프 분석
  - 장기 영향 고려
  - Red Team / Blue Team 분석
use_case: "strategic 모드로 아키텍처 검토해줘"
```

### 4. visual (vis)
```yaml
trigger: ["visual", "vis", "시각", "이미지"]
activated_personas: [multimodal, frontend]
behavior:
  - 스크린샷 분석
  - 이미지 처리
  - UI 시각적 검토
use_case: "visual 모드로 이 스크린샷 분석해줘"
```

---

## 키워드 감지 우선순위

1. Mode Keywords (전역 모드 변경)
2. Vibe Keywords (작업 방식 변경)
3. 보안 키워드 (페르소나 강제 활성화)
4. 일반 키워드 (기본 처리)

---

## 조합 사용 예시

```bash
# 병렬 + 빠르게
"동시에 빠르게 3개 API 만들어줘"

# 전략 + 분석
"strategic 모드로 현재 아키텍처 분석해줘"

# 실험 + 테스트
"실험 모드로 새 알고리즘 적용하고 테스트해줘"
```
