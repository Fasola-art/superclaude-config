---
description: "에이전트 생성 (Spawn agent)"
argument-hint: "[agent_type]"
---

# 에이전트 생성

특정 작업을 위한 에이전트를 생성합니다.

## 사용

```
/sc:spawn explorer         # Explorer 에이전트
/sc:spawn analyzer         # Analyzer 에이전트
/sc:spawn --parallel 3     # 병렬 에이전트
```

## 에이전트 유형

- explorer: 코드 탐색
- analyzer: 분석
- reviewer: 리뷰
- implementer: 구현
