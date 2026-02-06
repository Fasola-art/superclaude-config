# Rules 파일 리팩토링 계획

> **목표**: CLAUDE.md Line Limits 준수
> **현재**: 9개 파일, 4,084줄 (평균 454줄)
> **목표**: ~45개 파일, ~4,000줄 (평균 89줄)

---

## CLAUDE.md Line Limits (참조)

| Type | Range | Split Trigger |
|------|-------|---------------|
| Logic/Utils | 50~80줄 | 3+ functions or complex regex |
| **UI Components** | **100~120줄** | 4+ states or deep DOM |
| API/Server | 80~100줄 | Error handling obscures logic |
| types/constants | ≤20줄 | Type-only or const-only |
| utils/hooks | ≤50줄 | Single-purpose functions |

**Critical Rules:**
- MIN 20줄: 20줄 미만 → 병합
- **2+ usage → extract**: 공통 로직 → 공통 모듈로 추출
- Split requires: barrel export (index.md)

---

## 현황 분석

| 파일 | 현재 | 타입 | 권장 | 초과율 |
|------|------|------|------|--------|
| TDD-RULES.md | 730줄 | 복잡 문서 | 120줄 | 6.1x |
| REACT-RULES.md | 721줄 | 복잡 문서 | 120줄 | 6.0x |
| E2E-RULES.md | 673줄 | 복잡 문서 | 120줄 | 5.6x |
| GO-RULES.md | 610줄 | 규칙 문서 | 100줄 | 6.1x |
| PYTHON-RULES.md | 595줄 | 규칙 문서 | 100줄 | 6.0x |
| SQL-TRADING-RULES.md | 453줄 | 규칙 문서 | 100줄 | 4.5x |

**핵심 위반사항**:
1. 모든 파일이 Line Limits 위반
2. Barrel export (index.md) 누락
3. **공통 패턴 미추출** (2+ usage 위반)
   - Priority Summary 테이블: 9개 파일에 중복
   - BAD/GOOD 코드 예제 패턴: 모든 파일에 중복
   - Checklist 섹션: 모든 파일에 중복
   - META 섹션: 모든 파일에 중복
4. 중복 콘텐츠 (~80% RULES ↔ QUICK-REFERENCE)

---

## Phase 0: 공통 패턴 추출 (2+ usage → extract)

### 중복 분석 결과

| 패턴 | 중복 횟수 | 추출 대상 |
|------|----------|----------|
| Priority Summary 테이블 | 9회 | `_shared/priority-table.md` |
| BAD/GOOD 코드 패턴 | 전체 | `_shared/example-format.md` |
| Checklist 섹션 | 9회 | 각 언어별 `checklist.md` |
| META 섹션 | 9회 | 제거 (Git history로 대체) |
| 검증 명령어 | 5회 | `_shared/validation.md` |

### 추출 효과

- 예상 중복 제거: ~400줄 (전체의 10%)
- 유지보수: 한 곳에서 수정 → 전체 반영

---

## Phase 1: 공통 인프라 구축 (30분)

### 1.1 _shared/ 디렉토리 생성

```
rules/_shared/
├── priority-table.md      # 25줄 - Priority Summary 테이블 (공통)
├── example-format.md      # 30줄 - BAD/GOOD 예제 작성 가이드
├── rule-template.md       # 35줄 - 새 규칙 작성 템플릿
└── validation.md          # 40줄 - 공통 검증 명령어
```

### 1.2 Root 파일 생성

```
rules/
├── index.md               # 40줄 - 전체 개요 + 네비게이션
└── README.md              # 30줄 - 사용법 가이드
```

---

## Phase 2: Go 규칙 분할 (45분)

### 현재 → 목표

```
go/
├── GO-RULES.md (610줄)     →  삭제 (백업 후)
├── QUICK-REFERENCE.md (106줄)  →  유지
```

### 새 구조 (38 규칙 → 4개 파일)

```
go/
├── index.md                    # 30줄 - 개요 + Priority Summary 링크
├── critical.md                 # 120줄 - ERROR(6) + CONCUR(6) = 12 규칙
├── high.md                     # 100줄 - STRUCT(5) + IFACE(5) = 10 규칙
├── medium.md                   # 100줄 - FUNC(5) + PKG(5) = 10 규칙
├── low.md                      # 60줄 - PERF(3) + TEST(3) = 6 규칙
├── QUICK-REFERENCE.md          # 106줄 - 유지 (기존)
└── checklist.md                # 30줄 - 검증 명령어
```

**총: 546줄 (현재 716줄 대비 -24%)**

---

## Phase 3: Python 규칙 분할 (45분)

### 새 구조 (42 규칙 → 4개 파일)

```
python/
├── index.md                    # 30줄 - 개요 + Priority Summary 링크
├── critical.md                 # 110줄 - TYPE(6) + ERROR(5) = 11 규칙
├── high.md                     # 100줄 - ASYNC(5) + CLASS(5) = 10 규칙
├── medium.md                   # 110줄 - FUNC(6) + IMPORT(5) = 11 규칙
├── low.md                      # 100줄 - PERF(5) + TEST(5) = 10 규칙
├── QUICK-REFERENCE.md          # 104줄 - 유지 (기존)
└── checklist.md                # 30줄 - 검증 명령어
```

**총: 584줄 (현재 699줄 대비 -16%)**

---

## Phase 4: React 규칙 분할 (1시간)

### 새 구조 (49 규칙 → 5개 파일)

```
react/
├── index.md                    # 30줄 - 개요 + Priority Summary 링크
├── critical.md                 # 120줄 - ASYNC(5) + BUNDLE(5) = 10 규칙
├── high.md                     # 120줄 - RENDER(5) + SERVER(5) = 10 규칙
├── medium.md                   # 120줄 - CACHE(5) + IMAGE(5) + RERENDER(7) = 17 규칙
├── low.md                      # 120줄 - JS-OPT(12) = 12 규칙
├── QUICK-REFERENCE.md          # 92줄 - 유지 (기존)
└── checklist.md                # 30줄 - 검증 명령어
```

**총: 632줄 (현재 813줄 대비 -22%)**

---

## Phase 5: Testing 규칙 분할 (1.5시간)

### 핵심: TDD/E2E 공유 패턴 추출 (2+ usage)

**공유 패턴:**
- AAA 패턴 (Arrange-Act-Assert): TDD + E2E 모두 사용
- Mocking 패턴: TDD + E2E 모두 사용
- CI/CD 설정: TDD + E2E 모두 사용

### 새 구조

```
testing/
├── index.md                    # 35줄 - 개요 + TDD/E2E 링크
├── shared/
│   ├── patterns.md             # 80줄 - AAA, mocking 공통 패턴
│   └── ci-integration.md       # 60줄 - CI/CD 설정 공통
├── tdd/
│   ├── TDD-RULES.md            # 120줄 - CYCLE(4) + FIRST(3) + STRUCT(4) + COV(3) + MOCK(4)
│   ├── languages.md            # 100줄 - TS(3) + PY(3) + GO(3) 언어별 패턴
│   └── checklist.md            # 30줄 - 검증 명령어
├── e2e/
│   ├── E2E-RULES.md            # 120줄 - FLOW(4) + SEL(3) + PAT(5) + WAIT(3) + A11Y(3)
│   ├── tools.md                # 100줄 - Playwright(3) + Cypress(4)
│   └── checklist.md            # 30줄 - 검증 명령어
└── QUICK-REFERENCE.md          # 60줄 - TDD + E2E 요약
```

**총: 735줄 (현재 1,403줄 대비 -48%)**

---

## Phase 6: SQL 규칙 분할 (30분)

### 새 구조 (25 규칙 → 3개 파일)

```
sql/
├── index.md                    # 30줄 - 개요 + Priority Summary 링크
├── critical.md                 # 100줄 - PERF(5) + SAFETY(4) = 9 규칙
├── patterns.md                 # 120줄 - TS(5) + AGG(4) + STYLE(4) + MAINT(3) = 16 규칙
├── QUICK-REFERENCE.md          # 50줄 - 신규 생성
└── checklist.md                # 25줄 - 검증 명령어
```

**총: 325줄 (현재 453줄 대비 -28%)**

---

## Phase 7: CLAUDE.md Pre-Task Checklist 개선 (15분)

### 현재 문제

Pre-Task Checklist가 "**Before ANY code modification**"로 되어 있어 문서 파일에는 적용되지 않음.

### 개선안

**수정 전:**
```markdown
## Pre-Task Checklist (MANDATORY)

**Before ANY code modification:**
1. Run `wc -l <file>` - verify within limits
2. If exceeds limit → split first, then modify

**Line Limits (STRICT):**
| Type | Range | Split Trigger |
|------|-------|---------------|
| Logic/Utils | 50~80 | 3+ functions or complex regex |
| UI Components | 100~120 | 4+ states or deep DOM |
| API/Server | 80~100 | Error handling obscures logic |
| types/constants | ≤20 | Type-only or const-only |
| utils/hooks | ≤50 | Single-purpose functions |
```

**수정 후:**
```markdown
## Pre-Task Checklist (MANDATORY)

**Before ANY file creation/modification:**
1. Run `wc -l <file>` - verify within limits
2. If exceeds limit → split first, then modify

**Line Limits (STRICT):**
| Type | Range | Split Trigger |
|------|-------|---------------|
| Logic/Utils | 50~80 | 3+ functions or complex regex |
| UI Components | 100~120 | 4+ states or deep DOM |
| API/Server | 80~100 | Error handling obscures logic |
| types/constants | ≤20 | Type-only or const-only |
| utils/hooks | ≤50 | Single-purpose functions |
| **Documentation** | **80~120** | **5+ sections or long examples** |
| **Rules/Guidelines** | **100~120** | **10+ rules per priority** |

**Document-Specific Rules:**
- README.md: ≤150줄 (overview + quick start)
- API docs: ≤100줄 per endpoint group
- Rule files: ≤120줄 per priority level
- Quick Reference: ≤100줄 (snippets only)
```

### 수정 파일

`/Users/reim/.claude/CLAUDE.md` - Pre-Task Checklist 섹션 확장

---

## 실행 순서

| Phase | 작업 | 예상 시간 | 파일 수 |
|-------|------|----------|--------|
| 0 | 공통 패턴 추출 분석 | 15분 | - |
| 1 | 공통 인프라 (_shared/) | 30분 | 6개 |
| 2 | Go 분할 | 30분 | 7개 |
| 3 | Python 분할 | 30분 | 7개 |
| 4 | React 분할 | 45분 | 7개 |
| 5 | Testing 분할 | 1시간 | 11개 |
| 6 | SQL 분할 | 20분 | 5개 |
| 7 | CLAUDE.md 개선 | 15분 | 1개 |
| **총계** | | **~3.5시간** | **44개** |

---

## 검증 방법

### 1. 줄 수 검증
```bash
wc -l ~/.claude/rules/**/*.md | sort -n
# 모든 파일 ≤120줄, ≥20줄 확인
```

### 2. 구조 검증
```bash
# 모든 디렉토리에 index.md 존재 확인
find ~/.claude/rules -type d -exec sh -c 'ls "$1"/index.md 2>/dev/null || echo "Missing: $1"' _ {} \;
```

### 3. 링크 검증
```bash
# 깨진 링크 확인
grep -r "\](\./" ~/.claude/rules --include="*.md" | head -20
```

---

## 롤백 계획

1. 원본 파일을 `*.BACKUP.md`로 보관
2. 2주 검증 기간 후 백업 삭제
3. 문제 발생 시 백업에서 복원

---

## 예상 효과

| 지표 | 현재 | 개선 후 | 개선율 |
|------|------|---------|--------|
| 총 파일 수 | 9개 | 44개 | +389% |
| 총 줄 수 | 4,084줄 | ~2,980줄 | **-27%** |
| 평균 파일 크기 | 454줄 | 68줄 | **-85%** |
| 최대 파일 크기 | 730줄 | 120줄 | **-84%** |
| CLAUDE.md 준수 | 0% | 100% | ✅ |
| 중복 제거 | - | ~400줄 | - |

### 줄 수 감소 상세

| 디렉토리 | 현재 | 개선 후 | 감소율 |
|----------|------|---------|--------|
| go/ | 716줄 | 546줄 | -24% |
| python/ | 699줄 | 584줄 | -16% |
| react/ | 813줄 | 632줄 | -22% |
| testing/ | 1,403줄 | 735줄 | **-48%** |
| sql/ | 453줄 | 325줄 | -28% |
| _shared/ + root | - | 160줄 | - |

---

## 수정 대상 파일

### 삭제 (백업 후)
- `/Users/reim/.claude/rules/go/GO-RULES.md` → `GO-RULES.md.bak`
- `/Users/reim/.claude/rules/python/PYTHON-RULES.md` → `PYTHON-RULES.md.bak`
- `/Users/reim/.claude/rules/react/REACT-RULES.md` → `REACT-RULES.md.bak`
- `/Users/reim/.claude/rules/testing/TDD-RULES.md` → `tdd/TDD-RULES.md` (재구조화)
- `/Users/reim/.claude/rules/testing/E2E-RULES.md` → `e2e/E2E-RULES.md` (재구조화)
- `/Users/reim/.claude/rules/sql/SQL-TRADING-RULES.md` → 분할

### 유지 (그대로)
- `/Users/reim/.claude/rules/go/QUICK-REFERENCE.md` (106줄)
- `/Users/reim/.claude/rules/python/QUICK-REFERENCE.md` (104줄)
- `/Users/reim/.claude/rules/react/QUICK-REFERENCE.md` (92줄)

### 수정
- `/Users/reim/.claude/CLAUDE.md` - Pre-Task Checklist 확장

### 신규 생성
```
rules/
├── index.md                         # Root 네비게이션
├── README.md                        # 사용법 가이드
├── _shared/
│   ├── priority-table.md
│   ├── example-format.md
│   ├── rule-template.md
│   └── validation.md
├── go/
│   ├── index.md
│   ├── critical.md
│   ├── high.md
│   ├── medium.md
│   ├── low.md
│   └── checklist.md
├── python/
│   ├── index.md
│   ├── critical.md
│   ├── high.md
│   ├── medium.md
│   ├── low.md
│   └── checklist.md
├── react/
│   ├── index.md
│   ├── critical.md
│   ├── high.md
│   ├── medium.md
│   ├── low.md
│   └── checklist.md
├── testing/
│   ├── index.md
│   ├── shared/
│   │   ├── patterns.md
│   │   └── ci-integration.md
│   ├── tdd/
│   │   ├── TDD-RULES.md
│   │   ├── languages.md
│   │   └── checklist.md
│   ├── e2e/
│   │   ├── E2E-RULES.md
│   │   ├── tools.md
│   │   └── checklist.md
│   └── QUICK-REFERENCE.md
└── sql/
    ├── index.md
    ├── critical.md
    ├── patterns.md
    ├── QUICK-REFERENCE.md
    └── checklist.md
```

**신규 파일: 38개**

---

**META**
- Plan Version: 2.0
- Created: 2026-02-04
- Estimated Effort: ~3.5시간
- Key Changes: 공통 패턴 추출, CLAUDE.md 개선, 줄 수 제한 현실화
