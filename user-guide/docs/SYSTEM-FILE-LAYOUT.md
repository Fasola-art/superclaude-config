# Claude 시스템 전체 구조 리스트 (최종 복원본 v2)

이 문서는 `C:\Users\looki\.claude` 경로에 위치한 AI 에이전트의 핵심 시스템 구성 요소들을 정리한 것입니다. PDF 90-91페이지의 전체 구조와 92, 97, 98, 107페이지의 상세 폴더 내용을 통합하여 복원하였습니다.

---

## 📂 1. 전체 폴더 구조 (Folders)

| 폴더명 | 설명 | 상세 포함 여부 |
| :--- | :--- | :---: |
| **agents** | 개별 에이전트의 페르소나 및 설정 데이터 관리 | - |
| **archive** | 완료된 프로젝트나 오래된 설정의 아카이브 | - |
| **backups** | 시스템 설정 및 핵심 데이터의 자동 백업본 | - |
| **cache** | 성능 향상을 위한 임시 데이터 및 검색 결과 캐시 | - |
| **cheatsheets** | 빠른 참조를 위한 명령어 및 워크플로우 요약 문서 | - |
| **chrome** | 브라우저 자동화 관련 프로필 및 설정 데이터 | - |
| **commands** | 사용자 정의 명령어 및 스크립트 실행 파일 | **[상세보기]** |
| **debug** | 시스템 오류 진단 및 디버깅을 위한 로그 데이터 | - |
| **docs** | 시스템 운영 가이드 및 상세 매뉴얼 | **[상세보기]** |
| **error-kb** | 에러 지식 베이스 (pending, resolved, patterns) | - |
| **file-history** | 파일 변경 이력 및 버전 관리 데이터 | - |
| **hooks** | 특정 이벤트 트리거 시 실행되는 자동화 훅 | - |
| **ide** | IDE(VS Code 등) 연동 관련 설정 및 플러그인 데이터 | - |
| **jarvis** | Jarvis 시스템의 핵심 로직 및 상태 관리 데이터 | - |
| **logs** | 에이전트 활동 및 시스템 실행 로그 | - |
| **mcp-router** | Model Context Protocol(MCP) 서버 연결 및 라우팅 설정 | - |
| **output-styles** | 결과물 생성을 위한 마크다운/PDF/HTML 스타일 템플릿 | - |
| **patterns** | 반복되는 코드 구조 및 해결 패턴 데이터 | - |
| **personas** | 27종 이상의 전문 페르소나 정의 데이터 | - |
| **plans** | 프로젝트 기획 및 실행 계획 데이터 | - |
| **plugins** | 시스템 기능을 확장하는 외부 플러그인 | - |
| **profiles** | 사용자별/용도별 환경 설정 프로필 | - |
| **projects** | 현재 관리 중인 프로젝트들의 메타데이터 | - |
| **prompts** | 시스템 프롬프트 및 템플릿 모음 | - |
| **references** | 리서치 및 분석 시 참조하는 외부 데이터/포맷 | **[상세보기]** |
| **scripts** | 시스템 자동화를 위한 각종 스크립트 파일 | - |
| **session-env** | 세션별 환경 변수 및 상태 값 | - |
| **sessions** | 대화 세션 이력 및 컨텍스트 데이터 | - |
| **shell-snapshots** | 쉘 실행 상태 및 환경 스냅샷 | - |
| **skills** | 에이전트의 특수 기능 정의 (research, prd-create 등) | - |
| **statsig** | 기능 플래그 및 실험적 설정 관리 | - |
| **telemetry** | 시스템 사용 통계 및 성능 모니터링 데이터 | - |
| **templates** | 문서 및 코드 생성을 위한 표준 템플릿 | - |
| **todos** | 전체 프로젝트 및 세션별 할 일 목록 관리 | - |

---

## 📂 2. 상세 폴더 내용 (Detailed View)

### 2.1 `docs` 폴더 (PDF 92페이지)
시스템 운영의 핵심 원칙과 워크플로우를 정의하는 문서들입니다.

*   **ARCH-PRINCIPLES.md**: 시스템 아키텍처 설계 원칙
*   **DOC-TEMPLATE.md**: 표준 문서 작성을 위한 템플릿
*   **HOOKS-SYSTEM.md**: 자동화 훅 시스템 작동 원리 및 설정
*   **PERSONAS.md**: 페르소나 시스템 정의 및 활용 가이드
*   **PLAN-MODE.md**: 전략적 계획 모드(Plan Mode) 상세 가이드
*   **PRD-WORKFLOW.md**: 제품 요구사항 문서(PRD) 작성 워크플로우
*   **PROJECT-CONTEXT.md**: 프로젝트 컨텍스트 관리 및 유지 전략
*   **PROJECT-PLANNING.md**: 프로젝트 기획 및 단계별 분석 가이드
*   **QUALITY-GATES.md**: 코드 및 산출물 품질 검증 기준
*   **SETTINGS-GUIDE.md**: 시스템 환경 설정 상세 매뉴얼
*   **VERSION-POLICY.md**: 버전 관리 및 릴리즈 정책
*   **VIBE-WORKFLOW.md**: Vibe(감성/톤앤매너) 관리 워크플로우
*   **WRITER-REVIEWER-SYSTEM.md**: 작가-검토자 루프 시스템 상세 정의

### 2.2 `commands` 폴더 (PDF 97페이지)
에이전트의 동작을 제어하는 실행 명령어 및 스크립트입니다.

*   **sc/**: 하위 상세 명령어 폴더 (아래 2.3 참조)
*   **code-with-review.md**: 리뷰를 포함한 코드 생성 명령어
*   **error-search.md**: 에러 원인 분석 및 해결책 검색 명령어
*   **i.md**: 즉각적인 정보 조회 또는 인터랙션 명령어
*   **project-continue.md**: 중단된 프로젝트 이어서 진행하기
*   **project-plan.md**: 프로젝트 계획 수립 명령어
*   **project-status.md**: 현재 프로젝트 진행 상태 확인
*   **recover.md**: 시스템 또는 세션 복구 명령어
*   **vibe.md**: 현재 세션의 Vibe 설정 및 확인

### 2.3 `commands/sc` 폴더 (PDF 98페이지)
특정 작업(Task) 수행을 위한 세부 실행 유닛들입니다.

*   **analyze.md**, **build.md**, **cleanup.md**, **design.md**, **document.md**, **estimate.md**, **explain.md**, **git.md**, **implement.md**, **improve.md**, **index.md**, **load.md**, **spawn.md**, **task.md**, **test.md**, **troubleshoot.md**, **workflow.md**

### 2.4 `references` 폴더 (PDF 107페이지)
리서치, 분석 및 개발 시 참조하는 외부 라이브러리, SDK 및 가이드 모음입니다.

*   **claude-agent-sdk-typescript**: TypeScript용 Claude 에이전트 SDK 참조
*   **claude-code-action**: Claude 코드 액션 관련 정의 및 예시
*   **claude-code-security-review**: 코드 보안 검토 가이드 및 체크리스트
*   **claude-cookbooks**: 다양한 구현 사례를 담은 쿡북 레시피
*   **claude-quickstarts**: 빠른 시작을 위한 튜토리얼 및 샘플 프로젝트
*   **devcontainer-features**: 개발 컨테이너 환경 설정 및 기능 참조
*   **rhi-rhf**: RHI/RHF 관련 기술 참조 데이터

---

## 📄 3. 핵심 파일 목록 (Root Files)

| 파일명 | 설명 |
| :--- | :--- |
| **.credentials.json** | 외부 API 및 서비스 인증 정보 (암호화 관리) |
| **superclaude-metadata.json** | 시스템 전체 메타데이터 및 버전 정보 |
| **AGENTS.md** | 활성화된 에이전트 목록 및 역할 정의 문서 |
| **CLAUDE.md** | 프로젝트별 핵심 지침 및 워크플로우 가이드 |
| **CLAUDE_SKILLS_GUIDE.md** | 스킬 사용법 및 확장 가이드 문서 |
| **CONTEXT-MANAGER.md** | 컨텍스트 창 관리 및 DCP 전략 정의 문서 |
| **history.json** | 전체 실행 이력 및 타임라인 데이터 |
| **INSTALLED_SKILLS.md** | 현재 설치된 스킬 목록 및 상태 보고서 |
| **KEYWORD-TRIGGERS.md** | 자동화 트리거 키워드 및 액션 정의 문서 |
| **mcp.json** | MCP 서버 구성 및 연결 상세 설정 |
| **SESSION-MANAGER.md** | 세션 유지 및 복구 전략 정의 문서 |
| **settings.json** | 전역 시스템 환경 설정 파일 |
| **settings.local.json** | 로컬 환경 전용 오버라이드 설정 파일 |
| **stats-cache.json** | 통계 데이터 캐시 파일 |
| **WRITER-REVIEWER.md** | 코드 품질 검토 루프 및 가중치 설정 문서 |
| **todo.md** | 시스템 수준의 통합 할 일 관리 파일 |
| **VERSION** | 현재 시스템 버전 정보 파일 |
