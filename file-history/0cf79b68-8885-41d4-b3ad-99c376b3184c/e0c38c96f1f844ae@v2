# MCP Router

SuperClaude v2.0.9 MCP 라우터 시스템

## 개요

MCP (Model Context Protocol) 서버들을 관리하고 요청을 라우팅하는 시스템입니다.
Mac Studio Ultra M2의 24 CPU 코어를 활용한 병렬 처리를 지원합니다.

## 구성 요소

```
mcp-router/
├── server.py     # 메인 라우터 서버
├── client.py     # 클라이언트 유틸리티
└── README.md     # 이 문서
```

## 설정

`~/.claude/mcp.json` 파일에서 MCP 서버를 설정합니다:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem"],
      "priority": 10,
      "timeout": 30000
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## 사용법

### 서버 시작

```bash
python ~/.claude/mcp-router/server.py
```

### 클라이언트 사용

```bash
# 상태 확인
python ~/.claude/mcp-router/client.py status

# 기능 호출
python ~/.claude/mcp-router/client.py call filesystem '{"action": "list"}'
```

## 로드 밸런싱 전략

- **weighted_round_robin**: 우선순위 기반 라운드 로빈 (기본값)
- **least_latency**: 가장 낮은 지연시간 서버 선택

## 상태 코드

| 상태 | 설명 |
|------|------|
| HEALTHY | 정상 동작 |
| DEGRADED | 일부 기능 저하 |
| UNHEALTHY | 비정상 상태 |
| OFFLINE | 오프라인 |
| UNKNOWN | 상태 미확인 |

## Mac Studio 최적화

- 동시 서버 수: 최대 24개 (CPU 코어 수)
- 비동기 I/O 활용
- 메모리 효율적 상태 관리
