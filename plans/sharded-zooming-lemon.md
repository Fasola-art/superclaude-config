# SuperClaude 시스템 최적화 계획

> **목표**: 안전하고 신중하게 시스템 효율성 개선
> **위험 관리**: 단계별 검증, 즉시 롤백 가능

---

## 핵심 발견사항 (탐색 결과)

### 실제 작동 메커니즘

| 파일 | 역할 | 실제 파싱 | 실제 실행 |
|------|------|----------|----------|
| **CLAUDE.md** | 지침 문서 | ❌ | ❌ (컨텍스트로만 주입) |
| **superclaude-config.json** | 설정 백업 | ⚠️ 부분 | ❌ (대부분 미사용) |
| **personas/index.json** | 페르소나 규칙 | ✅ | ⚠️ (loader.py에서만) |
| **settings.json** | 실제 설정 | ✅✅✅ | ✅✅✅ |

### 중요한 발견

1. **CLAUDE.md의 YAML 블록들은 실행되지 않음** - Claude가 "읽고 따르려 하는" 지침일 뿐
2. **max_concurrent 불일치는 실제 영향 없음** - 훅에서 loader.py를 호출하지 않음
3. **현재 활성 훅 3개** - jarvis-morning-briefing, jarvis-work-tracker, jarvis-task-completion
4. **17개 훅이 비활성** - settings.json에 미등록

---

## 수정 계획

### Phase 1: CLAUDE.md 경량화 (안전)

**위험도**: 🟢 매우 낮음 (문서 수정만, 기능 변경 없음)

#### 대상 파일
- `/Users/reim/.claude/CLAUDE.md`

#### 변경 내용
16KB → 5KB 목표 (70% 감소)

**삭제할 섹션** (중복, docs/ 문서 참조로 대체):
- [ ] 핵심 시스템 YAML 블록 4개 → 1줄 참조
- [ ] Vibe/Mode Keywords 상세 테이블 → KEYWORD-TRIGGERS.md 참조
- [ ] 적응형 사고 모드 상세 → docs/THINKING-MODES.md 참조
- [ ] Project Planning 상세 → docs/PROJECT-PLANNING.md 참조
- [ ] Language Profiles 상세 설명 → profiles/*.md 참조
- [ ] 참조 문서 중복 테이블 → 1개로 통합
- [ ] Hooks System Summary → docs/HOOKS-SYSTEM.md 참조

**유지할 섹션** (필수):
- ✅ 최우선 규칙: 한국어 응답
- ✅ 효율성 원칙
- ✅ 필수 규칙 (5개)
- ✅ 스킬 명령어
- ✅ 파일 구조 (간략화)
- ✅ Safety Rules
- ✅ MCP Router 기본 원칙 (간략화)

#### 검증
```bash
# 크기 확인
wc -c ~/.claude/CLAUDE.md  # 목표: 5KB 이하

# Claude Code 동작 테스트
claude "안녕, 한국어로 응답해줘"
```

#### 롤백
```bash
cp ~/.claude/CLAUDE.md.backup ~/.claude/CLAUDE.md
```

---

### Phase 2: 설정 파일 정리 (저위험)

**위험도**: 🟡 낮음

#### 2.1 index.json finance 카테고리 추가

**대상**: `/Users/reim/.claude/personas/index.json`

```json
// 추가할 내용
"finance": {
  "count": 12,
  "personas": [
    "macro_economist", "fx_trader", "us_stock_analyst",
    "kr_stock_analyst", "onchain_analyst", "chart_analyst",
    "quant_strategist", "risk_manager", "derivatives_specialist",
    "bond_analyst", "commodity_specialist", "sentiment_analyst"
  ]
}
```

**참고**: 이 변경은 실제 동작에 영향 없음 (loader.py가 훅에서 호출되지 않으므로)

#### 2.2 superclaude-config.json maxConcurrent 통일

**대상**: `/Users/reim/.claude/superclaude-config.json`

```json
// 변경: 3 → 8
"personas": {
  "maxConcurrent": 8
}
```

**참고**: 이 변경도 실제 동작에 영향 없음 (문서 일관성 목적)

#### 검증
```bash
# JSON 문법 검증
python3 -c "import json; json.load(open('/Users/reim/.claude/personas/index.json'))"
python3 -c "import json; json.load(open('/Users/reim/.claude/superclaude-config.json'))"
```

---

### Phase 3: 훅 점진적 활성화 (신중하게)

**위험도**: 🟠 중간 (단계별 진행 필수)

#### 현재 활성 훅 (절대 수정 금지 ⚠️)
```json
// settings.json - 이 부분 유지
"UserPromptSubmit": jarvis-morning-briefing.py
"PostToolUse": jarvis-work-tracker.py, jarvis-task-completion.py
```

#### 추가 후보 (우선순위 순)

| 순위 | 훅 | 기능 | 위험도 |
|------|-----|------|--------|
| 1 | keyword-detector.py | Vibe/Mode 키워드 감지 | 낮음 |
| 2 | context-cleaner.py | 컨텍스트 70%+ 경고 | 낮음 |
| 3 | session-snapshot.py | 세션 자동 저장 | 낮음 |

#### 3.1 keyword-detector.py 추가 (1순위)

**대상**: `/Users/reim/.claude/settings.json`

```json
// UserPromptSubmit에 추가
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "python3 /Users/reim/.claude/hooks/UserPromptSubmit/keyword-detector.py"
    }
  ]
}
```

**검증**:
```bash
# 수동 테스트
CLAUDE_USER_PROMPT="빠르게 테스트" python3 ~/.claude/hooks/UserPromptSubmit/keyword-detector.py

# Claude Code 테스트
claude "빠르게 hello world 만들어줘"
# 예상 출력: 🎯 vibe:빠르게
```

**관찰 기간**: 3일

#### 3.2 이후 단계

- **3.2**: context-cleaner.py (3일 관찰 후)
- **3.3**: session-snapshot.py (3일 관찰 후)

---

## 실행 순서

| # | 작업 | 예상 시간 | 검증 기간 |
|---|------|----------|----------|
| 1 | CLAUDE.md 백업 | 1분 | - |
| 2 | CLAUDE.md 경량화 | 30분 | 즉시 확인 |
| 3 | index.json finance 추가 | 5분 | 즉시 확인 |
| 4 | superclaude-config.json 통일 | 5분 | 즉시 확인 |
| 5 | (선택) keyword-detector 활성화 | 5분 | **3일 관찰** |

---

## 수정 대상 파일 목록

### 필수 수정
1. `/Users/reim/.claude/CLAUDE.md` - 경량화
2. `/Users/reim/.claude/personas/index.json` - finance 추가
3. `/Users/reim/.claude/superclaude-config.json` - maxConcurrent 통일

### 선택 수정 (Phase 3)
4. `/Users/reim/.claude/settings.json` - 훅 추가 (신중하게)

### 절대 수정 금지
- settings.json의 기존 3개 훅 설정
- settings.json의 permissions 섹션

---

## 롤백 계획

### 백업 생성 (실행 전 필수)
```bash
# 전체 백업
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup.$(date +%Y%m%d)
cp ~/.claude/personas/index.json ~/.claude/personas/index.json.backup
cp ~/.claude/superclaude-config.json ~/.claude/superclaude-config.json.backup
cp ~/.claude/settings.json ~/.claude/settings.json.backup
```

### 문제 발생 시 롤백
```bash
# 개별 롤백
cp ~/.claude/CLAUDE.md.backup.* ~/.claude/CLAUDE.md
cp ~/.claude/settings.json.backup ~/.claude/settings.json
```

---

## 검증 체크리스트

### Phase 1 완료 후
- [ ] CLAUDE.md 크기 5KB 이하
- [ ] Claude Code 정상 시작
- [ ] 한국어 응답 정상
- [ ] 기존 기능 모두 동작

### Phase 2 완료 후
- [ ] JSON 파일 문법 오류 없음
- [ ] Claude Code 정상 시작

### Phase 3 완료 후 (선택 시)
- [ ] 키워드 감지 출력 확인 ("빠르게" 입력 시)
- [ ] 기존 Jarvis 훅 정상 동작
- [ ] 에러 없음

---

## 주의사항

1. **Phase 1, 2는 안전** - 문서/설정 정리만, 실제 동작 변경 없음
2. **Phase 3는 신중하게** - 하나씩 추가, 3일 관찰
3. **settings.json 수정 시 극도로 주의** - 기존 훅 설정 절대 건드리지 않음
4. **문제 발생 시 즉시 롤백** - 백업 파일 복원
