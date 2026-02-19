# bkit-inspired 5기능 도입 계획

## Context

bkit(Vibecoding Kit)의 PDCA 방법론, Context Engineering 패턴 분석 후 SuperClaude v2.0.9에 도입 가치가 있는 5가지 기능을 구현한다. 기존 hook/skill/jarvis 인프라를 최대한 재활용하며, 파일당 50~120줄 제한을 준수한다.

---

## Feature 1: Check-Act Auto-Retry Loop

**목표**: 코드 수정 후 lint/syntax 실패 시 자동 피드백 → Claude가 수정 반복

### 생성 파일

| 파일 | 줄 수 | 역할 |
|------|-------|------|
| `jarvis/quality/__init__.py` | ~25 | barrel export |
| `jarvis/quality/types.py` | ~25 | GateResult, CheckResult 타입 |
| `jarvis/quality/gate_runner.py` | ~100 | 파일 타입별 검증 실행 |
| `jarvis/quality/feedback.py` | ~70 | 실패 게이트 피드백 생성 |
| `hooks/PostToolUse/auto-retry-loop.py` | ~80 | 메인 Hook (Edit/Write 후 실행) |

### 수정 파일

| 파일 | 변경 |
|------|------|
| `superclaude-config.json` | `autoRetry` 섹션 추가 |
| `settings.json` | PostToolUse `Edit|Write` matcher에 hook 추가 |

### 핵심 로직

1. PostToolUse hook이 Edit/Write 감지
2. `~/.claude/cache/retry-state.json`에서 현재 반복 횟수 확인
3. gate_runner가 syntax + type check 실행 (subprocess)
4. 점수 < 0.90 → feedback 생성 → system-reminder로 출력
5. Claude가 피드백 읽고 수정 → hook 재실행 (자연 루프)
6. 점수 ≥ 0.90 또는 5회 도달 → 상태 리셋

### 설정 (superclaude-config.json)

```json
"autoRetry": {
  "enabled": true,
  "maxRetries": 5,
  "passThreshold": 0.90,
  "skipPatterns": [".json", ".md", ".env", ".yaml"]
}
```

---

## Feature 2: Agent Memory

**목표**: Task tool 에이전트가 세션 간 컨텍스트 유지

### 생성 파일

| 파일 | 줄 수 | 역할 |
|------|-------|------|
| `jarvis/memory/agent_memory.py` | ~100 | AgentMemory 클래스 (CRUD) |
| `hooks/PreToolUse/agent-memory-loader.py` | ~60 | Task 실행 전 메모리 로드 |
| `hooks/PostToolUse/agent-memory-saver.py` | ~70 | Task 실행 후 학습 저장 |

### 수정 파일

| 파일 | 변경 |
|------|------|
| `jarvis/memory/db.py` | `agent_memories` 테이블 추가 (마이그레이션) |
| `jarvis/memory/__init__.py` | AgentMemory export 추가 |
| `settings.json` | PreToolUse `Task` matcher + PostToolUse `Task` matcher에 hook 추가 |
| `superclaude-config.json` | `agentMemory` 섹션 추가 |

### DB 스키마

```sql
CREATE TABLE IF NOT EXISTS agent_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_type TEXT NOT NULL,
    project_path TEXT,
    context_key TEXT NOT NULL,
    context_value TEXT NOT NULL,
    session_id TEXT,
    access_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_type, project_path, context_key)
);
```

### 핵심 로직

- **Loader**: Task PreToolUse → agent_type + project_path로 상위 5개 메모리 조회 → 프롬프트에 `[Agent Memory] ...` 주입
- **Saver**: Task PostToolUse → 결과에서 패턴/학습 추출 → UPSERT (access_count 증가)
- **Cleanup**: 30일 미접근 메모리 자동 삭제

### 설정

```json
"agentMemory": {
  "enabled": true,
  "maxPerAgent": 50,
  "retentionDays": 30,
  "topK": 5
}
```

---

## Feature 3: Intent Detection + Ambiguity Scoring

**목표**: 모호한 프롬프트 자동 감지 → 명확화 유도

### 생성 파일

| 파일 | 줄 수 | 역할 |
|------|-------|------|
| `jarvis/nlu/ambiguity.py` | ~90 | 모호성 점수 계산 |
| `jarvis/nlu/classifier.py` | ~80 | 다중 Intent 점수 반환 |
| `hooks/UserPromptSubmit/intent-clarifier.py` | ~80 | 모호성 감지 Hook |

### 수정 파일

| 파일 | 변경 |
|------|------|
| `jarvis/nlu/__init__.py` | 새 모듈 export |
| `jarvis/nlu/types.py` | AmbiguityResult 타입 추가 |
| `settings.json` | UserPromptSubmit에 intent-clarifier hook 추가 |
| `superclaude-config.json` | `intentDetection` 섹션 추가 |

### 핵심 로직

**ambiguity.py**:
- `calculate_ambiguity(text)` → `AmbiguityResult(score, reason, suggestions)`
- 모호성 판단 기준:
  - 다중 Intent 매칭 (상위 2개 차이 < 0.15) → 높음
  - 최고 신뢰도 < 0.50 → 높음
  - 키워드 부족 (< 2개 의미어) → 중간
  - 과도한 범위 ("전부", "다", "모든") → 중간

**classifier.py**:
- `classify_multi(text)` → `list[tuple[Intent, float]]` (모든 매칭 Intent + 점수)
- 패턴 매칭 수 기반 점수: 1매칭=0.60, 2매칭=0.75, 3+매칭=0.90

**intent-clarifier.py**:
- 모호성 ≥ 0.60 → "❓ 의도 확인: {질문}" 출력
- 모호성 < 0.60 → 무출력 (정상 진행)

### 설정

```json
"intentDetection": {
  "enabled": true,
  "ambiguityThreshold": 0.60,
  "minKeywords": 2
}
```

---

## Feature 4: PDCA Workflow Skill

**목표**: Plan→Do→Check→Act 반복 개발 워크플로우

### 생성 파일

| 파일 | 줄 수 | 역할 |
|------|-------|------|
| `skills/pdca/SKILL.md` | ~120 | /pdca 스킬 정의 |
| `skills/pdca/references/stages.md` | ~80 | 단계별 상세 가이드 |
| `skills/pdca/references/templates.md` | ~60 | .pdca/ 파일 템플릿 |

### 핵심 워크플로우

```
/pdca plan <feature>     → .pdca/plan.md 생성 + TaskCreate
/pdca do                 → 태스크 실행 + Auto-Retry 통합
/pdca check              → 테스트/린트 실행 + check-results.md
/pdca act                → 개선점 분석 + act-actions.md
/pdca iterate            → history 저장 + 다음 iteration
/pdca status             → 현재 상태 표시
/pdca report             → 완료 보고서 생성
```

### 프로젝트 내 생성 구조

```
.pdca/
├── state.json           # 현재 단계, iteration 번호
├── plan.md              # 계획 (목표, 태스크, 성공 기준)
├── do-log.md            # 실행 로그
├── check-results.md     # 검증 결과
├── act-actions.md       # 개선 액션
└── history/
    └── iteration-1.json # 과거 iteration 기록
```

### state.json 형식

```json
{
  "feature": "trading-dashboard",
  "current_stage": "plan",
  "iteration": 1,
  "max_iterations": 5,
  "pass_threshold": 0.90,
  "stages": {
    "plan": {"status": "completed", "score": null},
    "do": {"status": "in_progress", "score": null},
    "check": {"status": "pending", "score": null},
    "act": {"status": "pending", "score": null}
  }
}
```

---

## Feature 5: Project Level System

**목표**: scaffold에 Starter/Dynamic/Enterprise 레벨 추가

### 수정 파일

| 파일 | 줄 수 | 변경 |
|------|-------|------|
| `skills/project-scaffold/SKILL.md` | ~120 | 레벨 선택 + 분기 로직 추가 |

### 생성 파일

| 파일 | 줄 수 | 역할 |
|------|-------|------|
| `skills/project-scaffold/references/starter.md` | ~60 | HTML/CSS/JS 템플릿 |
| `skills/project-scaffold/references/dynamic.md` | ~80 | Next.js + Supabase 템플릿 |
| `skills/project-scaffold/references/enterprise.md` | ~100 | Microservices 템플릿 |

### 레벨 비교

| 속성 | Starter | Dynamic | Enterprise |
|------|---------|---------|------------|
| 스택 | HTML/CSS/JS | Next.js + TS + Supabase | Docker + K8s + Terraform |
| DB | 없음 | Supabase | PostgreSQL + Redis |
| 인증 | 없음 | Supabase Auth | OAuth2 + JWT |
| 배포 | Netlify/GitHub Pages | Vercel | AWS/GCP |
| 설정 시간 | ~3분 | ~10분 | ~20분 |

### 사용법

```bash
/scaffold my-blog --level starter
/scaffold saas-app --level dynamic --ai
/scaffold platform --level enterprise
```

레벨 미지정 시 AskUserQuestion으로 선택 유도.

---

## 구현 순서

| 순서 | 기능 | 의존성 | 예상 파일 수 |
|------|------|--------|-------------|
| 1 | Feature 3: Intent + Ambiguity | 없음 | 4 생성 + 3 수정 |
| 2 | Feature 2: Agent Memory | 없음 | 3 생성 + 4 수정 |
| 3 | Feature 1: Check-Act Loop | 없음 | 5 생성 + 2 수정 |
| 4 | Feature 5: Project Levels | 없음 | 3 생성 + 1 수정 |
| 5 | Feature 4: PDCA Workflow | Feature 1 (Check 단계) | 3 생성 |

**총합**: 18개 파일 생성 + 10개 파일 수정

---

## 검증 방법

### Feature 1 (Auto-Retry)
```bash
# 의도적으로 syntax error 코드 작성 → hook이 피드백 출력하는지 확인
python3 -c "from jarvis.quality.gate_runner import run_gates; print(run_gates('test.py'))"
```

### Feature 2 (Agent Memory)
```bash
# DB 테이블 생성 확인
python3 -c "from jarvis.memory.db import init_database; init_database(force=True)"
sqlite3 ~/.claude/jarvis/memory/jarvis.db ".tables" | grep agent_memories
```

### Feature 3 (Intent + Ambiguity)
```bash
python3 -c "from jarvis.nlu.ambiguity import calculate_ambiguity; print(calculate_ambiguity('해줘'))"
python3 -c "from jarvis.nlu.classifier import classify_multi; print(classify_multi('할 일 추가해줘'))"
```

### Feature 4 (PDCA)
```bash
# /pdca plan test-feature 실행 → .pdca/ 디렉토리 생성 확인
ls -la .pdca/
```

### Feature 5 (Project Levels)
```bash
# /scaffold test --level starter 실행 → 구조 확인
ls -la test/
```
