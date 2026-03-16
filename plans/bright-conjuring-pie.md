# 코덱스-클로드 협업 워크플로우 구축 플랜

## 배경

CLAUDE.md v2.1.0 반영 사항:
- Platform Rules: WSL2 Required for Codex CLI 명시됨
- WSL2 filesystem `~/` 사용 (not `/mnt/c/`)
- Cost Strategy: Opus/Sonnet/Haiku 모델 분류
- Context Loss Prevention: `/compact` + TASKS.md 실시간 업데이트
- 코덱스용 파일은 120줄 제한 없음 (사용자 요청)

---

## 생성할 파일 목록

| 파일 | 줄 제한 | 역할 |
|------|---------|------|
| `skills/codex-workflow/SKILL.md` | 없음 (코덱스용) | 스킬 진입점 + 4단계 워크플로우 |
| `docs/CODEX-WORKFLOW.md` | 80~120줄 | 참조 가이드 (RACI + 다이어그램) |
| `modules/codex/task-template.md` | 없음 (코덱스용) | 명세서 템플릿 (10섹션) |
| `modules/codex/index.md` | 20~50줄 | 폴더 인덱스 |
| `hooks/UserPromptSubmit/codex-router.py` | Python 스크립트 | 자동 감지 훅 |

---

## 적용할 기존 지침

### CLAUDE.md v2.1.0 반영

1. **WSL2 경로**: 코덱스 실행 시 `~/project` (WSL2 filesystem)
2. **Cost Strategy**: 코덱스 위임 시 모델 선택 가이드 포함
   - 복잡 로직/아키텍처 → Max plan (Opus)
   - 표준 구현/리팩토링 → Sonnet (default)
   - 단순 수정/포맷 → Haiku
3. **Context Loss Prevention**: 핸드오프 전후 `/compact` + TASKS.md 업데이트
4. **TASKS.md 포맷**: `## Status | ## Done | ## Next | ## Blockers`

### 기존 스킬 패턴 적용

- YAML Frontmatter: `name`, `description`, `version`, `triggers`
- 트리거: 슬래시 커맨드 + 한국어 키워드
- 4단계 Phase 구조 (prd-create/SKILL.md 패턴)

### 기존 훅 패턴 적용

- stdin JSON 파싱 (`keyword-detector.py` 패턴)
- Windows UTF-8 처리
- 1줄 출력 (Efficiency Rules)
- `cache/` 디렉토리 상태 파일

---

## 파일별 세부 내용

### 1. `skills/codex-workflow/SKILL.md`
```
줄 제한: 없음 (코덱스 호환 명세서 포함)
트리거: /codex, 코덱스 위임, codex delegate, codex로 넘겨, 코덱스한테 맡겨
내용:
  - 작업 분류 매트릭스 (클로드 vs 코덱스)
  - Phase 1: 작업 분석 + 코덱스 적합성 판단
  - Phase 2: 명세서(Spec) 자동 생성 (task-template.md 기반)
  - Phase 3: WSL2 실행 명령 생성 (Cost Strategy 포함)
  - Phase 4: 클로드 검증 + TASKS.md 업데이트
  - 3-파일 시스템 연계 (plan.md, context.md, TASKS.md)
  - 사용 예시
```

### 2. `docs/CODEX-WORKFLOW.md`
```
줄 제한: 80~120줄
내용:
  - 역할 정의 표
  - RACI 매트릭스
  - 핸드오프 다이어그램 (ASCII)
  - WSL2 설정 (v2.1.0 Platform Rules 기반)
  - 품질 게이트 5개 기준
  - 관련 파일 링크
```

### 3. `modules/codex/task-template.md`
```
줄 제한: 없음 (코덱스 호환)
내용: 10섹션 명세서 템플릿
  1. 작업 목표 (단일 문장)
  2. 환경 정보 (WSL2 경로 포함, v2.1.0 반영)
  3. 모델 선택 (Cost Strategy 기반)
  4. 입력 파일 (WSL2 절대경로)
  5. 출력 파일 (WSL2 절대경로)
  6. 기술 스택 및 패턴
  7. 세부 요구사항
  8. 금지 사항 (PROHIBITED)
  9. 검증 방법
  10. 성공 기준 + 클로드 검증 체크포인트
```

### 4. `modules/codex/index.md`
```
줄 제한: 20~50줄
내용: 모듈 구조 + 파일 역할 설명
```

### 5. `hooks/UserPromptSubmit/codex-router.py`
```
패턴: keyword-detector.py 기반
입력: stdin JSON (prompt 키)
감지: 코덱스 적합 작업 키워드 (최적화/리팩토링/버그/알고리즘/보안/반복코드)
제외: /codex 이미 명시된 경우, 클로드 전담 패턴 (설계/기획/아키텍처)
출력: 1줄 안내 "[CODEX] {카테고리} 감지 → /codex 로 위임하거나 계속 진행"
상태: cache/codex-router-state.json
```

---

## settings.json 훅 등록 (구현 시 추가)

`settings.json`의 `UserPromptSubmit` 배열에 추가:
```json
{
  "type": "command",
  "command": "python C:/Users/MSI/.claude/hooks/UserPromptSubmit/codex-router.py"
}
```

기존 훅 순서 (keyword-detector → plan-mode-analyzer → language-enforcer → intent-clarifier → **codex-router**) 맨 끝에 추가.

---

## 검증 방법

1. `codex-router.py` 직접 실행 테스트
   ```bash
   echo '{"prompt": "정렬 알고리즘 최적화해줘"}' | python codex-router.py
   # 예상: [CODEX] 최적화/알고리즘 감지 → /codex 로 위임하거나 계속 진행
   ```

2. 스킬 트리거 확인
   ```
   /codex 입력 시 codex-workflow/SKILL.md 실행 확인
   ```

3. settings.json 훅 등록 확인
   - UserPromptSubmit에 codex-router.py 추가 필요 여부 확인

---

## 구현 순서

1. `modules/codex/index.md` (인덱스 먼저)
2. `modules/codex/task-template.md` (템플릿)
3. `skills/codex-workflow/SKILL.md` (스킬)
4. `docs/CODEX-WORKFLOW.md` (문서)
5. `hooks/UserPromptSubmit/codex-router.py` (훅)
6. `settings.json` 훅 등록 확인
