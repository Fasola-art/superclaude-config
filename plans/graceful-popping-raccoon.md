# 영문 Rules 파일 리팩토링 계획

> **목표**: 50-100줄 범위로 분할, 공통 모듈 추출, 정상 동작 유지

---

## 대상 파일 (영문만)

| 파일 | 현재 줄 | 상태 | 분할 수 |
|------|--------|------|--------|
| go/GO-RULES.md | 610 | 중복 제거 | 2개 추가 |
| python/PYTHON-RULES.md | 595 | 분할 필요 | 4개 |
| react/REACT-RULES.md | 721 | 분할 필요 | 6개 |
| testing/TDD-RULES.md | 730 | 분할 필요 | 4개 |
| testing/E2E-RULES.md | 673 | 분할 필요 | 6개 |

**제외**: sql/SQL-TRADING-RULES.md (한글)

---

## 목표 구조

```
rules/
├── _shared/
│   ├── ci-integration.md      # NEW (50줄)
│   └── test-fundamentals.md   # NEW (60줄)
│
├── go/
│   ├── medium.md              # NEW: FUNC+PKG (80줄)
│   ├── low.md                 # NEW: PERF+TEST (60줄)
│   └── archive/GO-RULES.md    # 원본 보관
│
├── python/
│   ├── index.md               # NEW (25줄)
│   ├── critical.md            # NEW (80줄)
│   ├── high.md                # NEW (70줄)
│   ├── medium.md              # NEW (80줄)
│   ├── low.md                 # NEW (60줄)
│   └── archive/
│
├── react/
│   ├── index.md               # NEW (25줄)
│   ├── critical.md            # NEW (80줄)
│   ├── high.md                # NEW (90줄)
│   ├── medium-cache.md        # NEW (70줄)
│   ├── medium-rerender.md     # NEW (90줄)
│   ├── low.md                 # NEW (80줄)
│   ├── low-advanced.md        # NEW (75줄)
│   └── archive/
│
└── testing/
    ├── index.md               # NEW (30줄)
    ├── QUICK-REFERENCE.md     # NEW (80줄)
    ├── tdd/
    │   ├── cycle.md           # (80줄)
    │   ├── coverage.md        # (65줄)
    │   └── mocking.md         # (80줄)
    ├── e2e/
    │   ├── user-flows.md      # (90줄)
    │   ├── selectors.md       # (80줄)
    │   ├── page-objects.md    # (90줄)
    │   ├── accessibility.md   # (85줄)
    │   ├── playwright.md      # (80줄)
    │   └── cypress.md         # (65줄)
    ├── languages/
    │   ├── typescript.md      # (60줄)
    │   ├── python.md          # (50줄)
    │   └── go.md              # (65줄)
    └── archive/
```

---

## 실행 단계

### Phase 1: 준비 (5분)
```bash
mkdir -p ~/.claude/rules/{go,python,react,testing}/archive
mkdir -p ~/.claude/rules/testing/{tdd,e2e,languages}
```

### Phase 2: 공통 모듈 (10분)
1. `_shared/ci-integration.md` 생성
2. `_shared/test-fundamentals.md` 생성

### Phase 3: Go (10분)
1. `go/medium.md` 생성 (FUNC + PKG 섹션)
2. `go/low.md` 생성 (PERF + TEST 섹션)
3. `go/GO-RULES.md` → archive 이동

### Phase 4: Python (15분)
1. critical/high/medium/low.md 생성
2. index.md 생성
3. 원본 archive 이동

### Phase 5: React (20분)
1. 6개 파일 분할 생성
2. index.md 생성
3. 원본 archive 이동

### Phase 6: Testing (30분)
1. tdd/ 폴더 3개 파일
2. e2e/ 폴더 6개 파일
3. languages/ 폴더 3개 파일
4. index.md, QUICK-REFERENCE.md
5. 원본 archive 이동

---

## 검증

```bash
# 줄 수 확인 (20-100줄 범위)
find ~/.claude/rules -name "*.md" ! -path "*/archive/*" -exec wc -l {} \;

# 20줄 미만 확인
find ~/.claude/rules -name "*.md" ! -name "index.md" ! -path "*/archive/*" \
  -exec sh -c 'lines=$(wc -l < "$1"); [ "$lines" -lt 20 ] && echo "$1: $lines"' _ {} \;
```

---

## 롤백

```bash
# archive에서 복원
cp ~/.claude/rules/*/archive/*.md ~/.claude/rules/*/
```

---

## Critical Files

- `/Users/reim/.claude/rules/testing/TDD-RULES.md` (730줄)
- `/Users/reim/.claude/rules/react/REACT-RULES.md` (721줄)
- `/Users/reim/.claude/rules/testing/E2E-RULES.md` (673줄)
- `/Users/reim/.claude/rules/go/GO-RULES.md` (610줄)
- `/Users/reim/.claude/rules/python/PYTHON-RULES.md` (595줄)

---

**예상 소요시간**: 1.5시간
**결과**: 39개 파일, 평균 67줄
