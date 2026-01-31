# MCP 에러 패턴

> **카테고리**: mcp-protocol
> **갱신일**: 2026-01-30

---

## 🔴 Critical 에러

### 서버 시작 실패

**메시지**: `MCP 서버 시작 실패 [서버명]`

**원인**:
1. 패키지 미설치
2. 잘못된 설정
3. 권한 문제

**해결책**:
```bash
# 1. 패키지 확인
npm list -g | grep mcp

# 2. 수동 실행 테스트
npx @서버명/mcp --debug

# 3. 설정 확인
cat ~/.claude/mcp.json

# 4. 로그 확인
tail -f ~/.claude/logs/mcp.log
```

**예시 해결**:
```json
// 문제: gdrive 서버 실패
// 해결: @isaacphi/mcp-gdrive로 대체

// mcp-router/servers.json
{
  "gdrive": {
    "command": "npx",
    "args": ["@isaacphi/mcp-gdrive"]
  }
}
```

---

### 요청 타임아웃

**메시지**: `요청 타임아웃: initialize`

**원인**:
1. 네트워크 문제
2. 서버 과부하
3. 잘못된 설정

**해결책**:
```bash
# 1. 네트워크 확인
ping registry.npmjs.org

# 2. 서버 재시작
# Claude Code 재시작

# 3. 타임아웃 설정 조정
# mcp-router/config.json
{
  "timeout": 60000,  # 60초로 증가
  "retries": 3
}
```

---

### 연결 거부

**메시지**: `연결 거부됨: ECONNREFUSED`

**원인**:
1. 서버 미실행
2. 포트 충돌
3. 방화벽

**해결책**:
```bash
# 1. 프로세스 확인
ps aux | grep mcp

# 2. 포트 확인
lsof -i :포트번호

# 3. 방화벽 확인 (macOS)
sudo pfctl -s rules
```

---

## 🟠 Common 에러

### 도구 호출 실패

**메시지**: `도구 호출 실패: [도구명]`

**원인**:
1. 잘못된 매개변수
2. 인증 만료
3. 서버 에러

**해결책**:
```typescript
// 매개변수 확인
{
  "tool": "context7.get-library-docs",
  "params": {
    "libraryId": "올바른-ID",  // 필수
    "query": "검색어"         // 선택
  }
}

// 인증 갱신
// 해당 서버의 인증 토큰 재설정
```

---

### 직렬화 오류

**메시지**: `JSON 직렬화 실패`

**원인**: 응답 데이터 파싱 실패

**해결책**:
```bash
# 원본 응답 확인
npx @서버명/mcp --debug

# 서버 버전 업데이트
npm update -g @서버명/mcp
```

---

## 🟡 설정 에러

### mcp.json 파싱 에러

**원인**: JSON 문법 오류

**해결책**:
```bash
# 문법 검사
cat ~/.claude/mcp.json | jq .

# 올바른 형식
{
  "mcpServers": {
    "mcp-router": {
      "command": "python",
      "args": ["~/.claude/mcp-router/server.py"]
    }
  }
}
```

---

### 서버 중복 등록

**원인**: 같은 서버 여러 번 등록

**해결책**:
```json
// ❌ 잘못된 설정
{
  "mcpServers": {
    "context7": { ... },    // 직접 등록
    "mcp-router": { ... }   // 라우터도 context7 포함
  }
}

// ✅ 올바른 설정 (라우터만)
{
  "mcpServers": {
    "mcp-router": {
      "command": "python",
      "args": ["~/.claude/mcp-router/server.py"]
    }
  }
}
```

---

## 📊 에러 빈도

| 에러 | 빈도 | 심각도 |
|------|------|--------|
| 서버 시작 실패 | 높음 | 높음 |
| 타임아웃 | 중간 | 중간 |
| 도구 호출 실패 | 중간 | 중간 |
| 설정 오류 | 낮음 | 낮음 |

---

## 🔧 디버깅

```bash
# 전체 로그
tail -f ~/.claude/logs/mcp.log

# 특정 서버 상태
cat ~/.claude/mcp-router/status.json

# 수동 테스트
echo '{"method":"tools/list"}' | npx @서버명/mcp
```

---

## 🔄 복구 절차

### 전체 MCP 재설정

```bash
# 1. 캐시 정리
rm -rf ~/.claude/mcp-router/cache/*

# 2. 상태 초기화
rm ~/.claude/mcp-router/status.json

# 3. Claude Code 재시작
# 터미널에서 claude 재실행
```

### 개별 서버 재설정

```bash
# 1. 서버 제거
# mcp-router/servers.json에서 해당 서버 삭제

# 2. 캐시 정리
rm ~/.claude/mcp-router/cache/서버명.*

# 3. 다시 추가
# mcp-router/servers.json에 재등록
```

---

**META**
- Category: mcp-protocol
- Last Updated: 2026-01-30
