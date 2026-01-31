# 슬래시 명령어 치트시트

> **버전**: 1.0.0
> **갱신일**: 2026-01-30

---

## 🚀 빠른 참조

### 가장 많이 쓰는 명령어 (Top 10)

| 명령어 | 설명 | 단축키 |
|--------|------|--------|
| `/commit` | Git 커밋 생성 | - |
| `/project-status` | 프로젝트 진행 상황 | - |
| `/project-continue` | 중단된 작업 이어서 | - |
| `/recover` | 세션 복구 | - |
| `/error-search` | Error KB 검색 | - |
| `/help` | 도움말 | - |
| `/market` | 오늘의 경제 시황 | - |
| `/review-pr` | PR 코드 리뷰 | - |
| `/vibe` | 세션 Vibe 설정 | - |
| `/hookify` | 대화에서 훅 생성 | - |

---

## 📋 카테고리별 명령어

### 🔧 프로젝트 관리

| 명령어 | 설명 | 사용 예시 |
|--------|------|----------|
| `/project-plan` | 프로젝트 계획 수립 | PRD 기반 계획 생성 |
| `/project-status` | 현재 진행 상황 | 태스크 상태 확인 |
| `/project-continue` | 중단된 작업 이어서 | STATE.md 복원 |
| `/recover` | 세션/시스템 복구 | 비정상 종료 후 |

### 📝 Git 작업

| 명령어 | 설명 | 옵션 |
|--------|------|------|
| `/commit` | Git 커밋 생성 | 자동 메시지 생성 |
| `/commit-push-pr` | 커밋 → 푸시 → PR | 원스톱 |
| `/clean_gone` | gone 브랜치 정리 | 로컬 정리 |
| `/sc:git` | Git 작업 도우미 | 범용 |

### 🔍 코드 분석

| 명령어 | 설명 | 출력 |
|--------|------|------|
| `/code-review` | 풀 리퀘스트 리뷰 | 상세 리뷰 |
| `/review-pr` | 에이전트 활용 PR 리뷰 | 병렬 검토 |
| `/sc:analyze` | 코드/프로젝트 분석 | 구조 분석 |
| `/sc:explain` | 코드/개념 설명 | 상세 설명 |

### 🛠️ 개발 도구

| 명령어 | 설명 | 대상 |
|--------|------|------|
| `/sc:implement` | 기능 구현 | 코드 생성 |
| `/sc:improve` | 코드 개선 | 리팩토링 |
| `/sc:cleanup` | 코드 정리 | 미사용 코드 제거 |
| `/sc:test` | 테스트 실행 | 자동 테스트 |
| `/sc:build` | 프로젝트 빌드 | 빌드 실행 |

### 📊 경제/트레이딩

| 명령어 | 설명 | 출력 |
|--------|------|------|
| `/market` | 오늘의 경제 시황 | 보고서 |
| `/sc:calendar` | 경제 지표 발표 일정 | 캘린더 |
| `/sc:news` | 뉴스 수집 및 요약 | 요약 |
| `/sc:report` | 일일 경제 보고서 | 보고서 |
| `/telegram` | 텔레그램 모니터링 | AI 요약 |

### 🔌 플러그인/스킬 개발

| 명령어 | 설명 | 가이드 |
|--------|------|--------|
| `/create-plugin` | 플러그인 생성 | 워크플로우 |
| `/new-sdk-app` | Agent SDK 앱 생성 | TS/Python |
| `/hookify` | 훅 규칙 생성 | 대화 분석 |
| `/feature-dev` | 기능 개발 가이드 | 아키텍처 |

### 📚 문서/가이드

| 명령어 | 설명 | 참조 |
|--------|------|------|
| `/help` | 플러그인 설명 | Ralph Loop |
| `/daily` | 자주 쓰는 경로 모음 | 경로 확인 |
| `/sc:document` | 문서 생성 | 자동 문서화 |
| `/sc:index` | SC 명령어 목록 | 이 치트시트 |

### ⚙️ 설정/관리

| 명령어 | 설명 | 대상 |
|--------|------|------|
| `/vibe` | 세션 Vibe 설정 | 현재 세션 |
| `/list` | hookify 규칙 목록 | 규칙 조회 |
| `/configure` | hookify 규칙 활성화 | 활성/비활성 |
| `/revise-claude-md` | CLAUDE.md 업데이트 | 학습 반영 |

### 🔄 루프/자동화

| 명령어 | 설명 | 동작 |
|--------|------|------|
| `/ralph-loop` | Ralph Loop 시작 | 자동 작업 |
| `/cancel-ralph` | Ralph Loop 취소 | 중단 |
| `/sc:workflow` | 워크플로우 실행 | 자동화 |
| `/sc:spawn` | 에이전트 생성 | 병렬 처리 |

### 💳 Stripe 관련

| 명령어 | 설명 | 출력 |
|--------|------|------|
| `/test-cards` | Stripe 테스트 카드 | 카드 번호 |
| `/explain-error` | Stripe 에러 설명 | 해결책 |
| `/stripe-best-practices` | Stripe 모범 사례 | 가이드 |

### 🔧 트러블슈팅

| 명령어 | 설명 | 동작 |
|--------|------|------|
| `/error-search` | Error KB 검색 | 유사 에러 |
| `/sc:troubleshoot` | 문제 해결 | 자동 진단 |
| `/recover` | 세션 복구 | 상태 복원 |

---

## 📊 SC (SuperClaude) 명령어 전체

### 개발

| 명령어 | 설명 |
|--------|------|
| `/sc:implement` | 기능 구현 |
| `/sc:improve` | 코드 개선 |
| `/sc:cleanup` | 코드 정리 |
| `/sc:test` | 테스트 실행 |
| `/sc:build` | 프로젝트 빌드 |

### 분석

| 명령어 | 설명 |
|--------|------|
| `/sc:analyze` | 코드/프로젝트 분석 |
| `/sc:explain` | 코드/개념 설명 |
| `/sc:design` | 시스템/컴포넌트 설계 |
| `/sc:estimate` | 작업 규모 추정 |

### 문서

| 명령어 | 설명 |
|--------|------|
| `/sc:document` | 문서 생성 |
| `/sc:index` | SC 명령어 목록 |
| `/sc:load` | 컨텍스트 로드 |

### 자동화

| 명령어 | 설명 |
|--------|------|
| `/sc:workflow` | 워크플로우 실행 |
| `/sc:spawn` | 에이전트 생성 |
| `/sc:task` | 태스크 관리 |
| `/sc:git` | Git 작업 도우미 |

### 경제

| 명령어 | 설명 |
|--------|------|
| `/sc:calendar` | 경제 지표 발표 일정 |
| `/sc:news` | 뉴스 수집 및 요약 |
| `/sc:report` | 일일 경제 보고서 |

---

## 🎯 사용 시나리오

### 새 프로젝트 시작

```
1. /project-plan     → 계획 수립
2. /sc:design        → 아키텍처 설계
3. /sc:implement     → 기능 구현
4. /sc:test          → 테스트 실행
5. /commit           → 커밋
```

### 코드 리뷰 플로우

```
1. /review-pr        → PR 리뷰 (에이전트 활용)
2. /sc:improve       → 개선 사항 적용
3. /sc:test          → 테스트 확인
4. /commit-push-pr   → 머지
```

### 트러블슈팅 플로우

```
1. /error-search     → Error KB 검색
2. /sc:troubleshoot  → 자동 진단
3. /sc:improve       → 수정 적용
4. /sc:test          → 확인
```

### 경제 분석 플로우

```
1. /market           → 오늘의 시황
2. /sc:calendar      → 발표 일정
3. /sc:news          → 뉴스 수집
4. /sc:report        → 보고서 생성
```

---

## ⚠️ 주의사항

| 명령어 | 주의사항 |
|--------|----------|
| `/commit-push-pr` | 리모트 푸시 포함 |
| `/ralph-loop` | 장시간 실행 가능 |
| `/clean_gone` | 로컬 브랜치 삭제 |
| `/hookify` | 훅 파일 생성 |

---

## 📚 참조

| 문서 | 경로 |
|------|------|
| 스킬 가이드 | `~/.claude/CLAUDE_SKILLS_GUIDE.md` |
| 설치된 스킬 | `~/.claude/INSTALLED_SKILLS.md` |
| 훅 시스템 | `~/.claude/docs/HOOKS-SYSTEM.md` |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
