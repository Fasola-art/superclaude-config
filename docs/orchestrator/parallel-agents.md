# Parallel Agent Execution

> 병렬 에이전트 실행 설정 및 동작

## superclaude-config.json 설정

```json
{
  "parallelExecution": {
    "enabled": true,
    "adaptive": true,
    "initial": 10,
    "minimum": 3,
    "maximum": 24,
    "scaleUp": {
      "increment": 5,
      "condition": "3 consecutive successes"
    },
    "scaleDown": {
      "decrement": 3,
      "condition": "1 failure"
    },
    "optimization": "M2 Ultra CPU cores (24 cores)"
  },
  "personas": {
    "maxConcurrent": 8,
    "priority": ["security", "architect", "analyzer"],
    "autoActivate": true
  }
}
```

## Adaptive Scaling 동작

```
시작: 10개 동시 실행
       │
       ├── 3회 연속 성공 → 15개로 증가 (+5)
       │                    │
       │                    ├── 3회 연속 성공 → 20개로 증가
       │                    │
       │                    └── 1회 실패 → 17개로 감소 (-3)
       │
       └── 1회 실패 → 7개로 감소 (-3)
```

## Available Agents (79)

| Category | Agent | Purpose |
|----------|-------|---------|
| Code Review | code-reviewer | 버그, 보안, 품질 리뷰 |
| Code Exploration | code-explorer | 코드베이스 분석 |
| Testing | pr-test-analyzer | PR 테스트 커버리지 분석 |
| Design | code-architect | 피처 아키텍처 설계 |
| Types | type-design-analyzer | 타입 설계 분석 |
| Simplification | code-simplifier | 코드 단순화 |
| Comments | comment-analyzer | 주석 분석 |
| Failure Detection | silent-failure-hunter | 사일런트 실패 탐지 |

## 병렬 실행 트리거

```bash
# 방법 1: "동시에" 또는 "para" 키워드
> "para analyze this code and generate tests"
🎯 vibe:동시에

# 방법 2: Task 도구로 여러 에이전트
# (내부적으로 자동 병렬 처리)
```

---

**Related**: [system-architecture.md](system-architecture.md), [scenarios-basic.md](scenarios-basic.md)
