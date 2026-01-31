# MCP 도구 치트시트

> **버전**: 1.0.0
> **갱신일**: 2026-01-30

---

## 🚀 빠른 참조

### MCP Router 아키텍처

```
Claude Code
    ↓
mcp-router (단일 진입점)
    ↓
필요한 서버만 동적 로딩
    ├── context7
    ├── serena
    └── playwright
```

### 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **단일 진입점** | mcp-router만 mcp.json에 등록 |
| **동적 로딩** | 필요할 때만 서버 실행 |
| **컨텍스트 절약** | 시스템 프롬프트 최소화 |

---

## 📋 사용 가능한 MCP 서버

### Context7 - 라이브러리 문서 검색

| 도구 | 설명 | 사용 예시 |
|------|------|----------|
| `resolve` | 라이브러리 ID 조회 | Next.js 문서 ID 확인 |
| `get-library-docs` | 문서 검색 | Next.js 라우팅 문서 |

#### 사용 예시

```
"Next.js App Router 문서 찾아줘"
→ context7.resolve("next.js")
→ context7.get-library-docs(id, "app router")
```

#### 지원 라이브러리

| 라이브러리 | 용도 |
|-----------|------|
| Next.js | React 프레임워크 |
| React | UI 라이브러리 |
| Supabase | 백엔드 서비스 |
| Tailwind | CSS 프레임워크 |
| Prisma | ORM |

---

### Serena - 코드 분석

| 도구 | 설명 | 사용 예시 |
|------|------|----------|
| `find-symbol` | 심볼 검색 | 함수/클래스 위치 찾기 |
| `get-definition` | 정의 조회 | 함수 구현 확인 |
| `find-references` | 참조 검색 | 사용처 찾기 |
| `analyze-file` | 파일 분석 | 구조 파악 |

#### 사용 예시

```
"UserService 클래스 정의 찾아줘"
→ serena.find-symbol("UserService")
→ serena.get-definition(location)

"이 함수 어디서 사용되는지 찾아줘"
→ serena.find-references(symbol)
```

---

### Playwright - 브라우저 자동화

| 도구 | 설명 | 사용 예시 |
|------|------|----------|
| `navigate` | 페이지 이동 | URL 방문 |
| `click` | 클릭 | 버튼 클릭 |
| `fill` | 입력 | 폼 작성 |
| `screenshot` | 스크린샷 | 화면 캡처 |
| `evaluate` | JS 실행 | 커스텀 스크립트 |

#### 사용 예시

```
"이 페이지 스크린샷 찍어줘"
→ playwright.navigate(url)
→ playwright.screenshot()

"로그인 폼 테스트해줘"
→ playwright.fill("#email", "test@example.com")
→ playwright.fill("#password", "password")
→ playwright.click("button[type=submit]")
```

---

## 🔧 MCP Router 설정

### mcp.json 설정 (올바른 방법)

```json
{
  "mcpServers": {
    "mcp-router": {
      "command": "python",
      "args": ["~/.claude/mcp-router/server.py"]
    }
  }
}
```

### ❌ 잘못된 설정 (절대 금지)

```json
{
  "mcpServers": {
    "context7": { ... },    // ❌ 직접 등록 금지
    "sequential": { ... },  // ❌ 컨텍스트 폭발
    "playwright": { ... }   // ❌ 시스템 프롬프트 비대화
  }
}
```

---

## 📊 서버 목록 (mcp-router/servers.json)

### 현재 등록된 서버

| 서버 | 명령어 | 용도 |
|------|--------|------|
| `context7` | `npx @context7/mcp` | 문서 검색 |
| `serena` | `npx @serena/mcp` | 코드 분석 |
| `playwright` | `npx @playwright/mcp` | 브라우저 자동화 |

### 서버 추가 방법

```json
// ~/.claude/mcp-router/servers.json
{
  "servers": {
    "new-server": {
      "command": "npx",
      "args": ["@new-server/mcp"],
      "description": "새 서버 설명"
    }
  }
}
```

---

## 🎯 사용 시나리오

### 문서 검색 플로우

```
1. 라이브러리 식별
   → context7.resolve("라이브러리명")

2. 문서 검색
   → context7.get-library-docs(id, "검색어")

3. 결과 활용
   → 코드 생성에 반영
```

### 코드 분석 플로우

```
1. 심볼 검색
   → serena.find-symbol("클래스/함수명")

2. 정의 확인
   → serena.get-definition(location)

3. 참조 찾기
   → serena.find-references(symbol)

4. 영향도 분석
   → 리팩토링 계획 수립
```

### 브라우저 테스트 플로우

```
1. 페이지 이동
   → playwright.navigate(url)

2. 인터랙션
   → playwright.fill / click

3. 검증
   → playwright.screenshot / evaluate

4. 결과 확인
   → 테스트 결과 분석
```

---

## ⚠️ 주의사항

### 컨텍스트 관리

| 상황 | 주의사항 |
|------|----------|
| 다중 서버 호출 | 순차적으로 호출, 병렬 금지 |
| 대용량 응답 | 필요한 부분만 요청 |
| 캐시 활용 | 동일 요청 반복 방지 |

### 성능 고려

| 서버 | 응답 시간 | 리소스 |
|------|----------|--------|
| context7 | 빠름 | 낮음 |
| serena | 중간 | 중간 |
| playwright | 느림 | 높음 |

---

## 🔍 트러블슈팅

### 일반적인 문제

| 문제 | 원인 | 해결책 |
|------|------|--------|
| 서버 응답 없음 | 서버 미실행 | mcp-router 재시작 |
| 타임아웃 | 네트워크 문제 | 재시도 |
| 권한 오류 | 인증 문제 | 토큰 확인 |

### 디버깅

```bash
# MCP 로그 확인
tail -f ~/.claude/logs/mcp.log

# 서버 상태 확인
cat ~/.claude/mcp-router/status.json

# 수동 서버 실행
npx @context7/mcp --debug
```

---

## 📚 참조

| 문서 | 경로 |
|------|------|
| MCP 통합 가이드 | `~/.claude/skills/mcp-integration/` |
| MCP Router 설정 | `~/.claude/mcp-router/` |
| 설정 가이드 | `~/.claude/docs/SETTINGS-GUIDE.md` |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
