# Writer-Reviewer Loop

> 코드 생성 시 4-agent 품질 보증 시스템

## Overview

Writer-Reviewer는 코드 생성 시 4개의 병렬 리뷰어 에이전트를 통해 품질을 보장합니다.

## 4-Agent Structure

```
┌─────────────────────────────────────────────────────────────┐
│                      Writer (Code Generation)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   4 Reviewers (Parallel)                     │
├─────────────────┬─────────────────┬─────────────────┬───────┤
│ Quality (30%)   │ Security (30%)  │ Performance(20%)│A11y   │
│                 │                 │                 │(20%)  │
│ • 코드 품질     │ • 취약점        │ • 병목          │• 접근성│
│ • 가독성       │ • 인증/인가      │ • 메모리 누수   │• ARIA │
│ • 유지보수성   │ • 인젝션         │ • 알고리즘 효율 │• 키보드│
└─────────────────┴─────────────────┴─────────────────┴───────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Score Aggregation (targetScore: 0.85)           │
│                                                              │
│   현재 점수 < 0.85 → 피드백과 함께 재작성 (최대 10회)       │
│   현재 점수 ≥ 0.85 → ✅ 완료                                 │
│   수렴 임계값: 0.015 (미만 시 조기 종료)                     │
└─────────────────────────────────────────────────────────────┘
```

## 코드 타입별 가중치 자동 조정

```python
CODE_TYPE_PATTERNS = {
    'frontend': {
        'keywords': ['component', 'tsx', 'jsx', 'ui', 'form'],
        'weights': {
            'quality': 0.25,
            'security': 0.25,
            'performance': 0.20,
            'accessibility': 0.30  # 프론트엔드: 접근성 우선
        }
    },
    'backend': {
        'keywords': ['api', 'route', 'endpoint', 'controller'],
        'weights': {
            'quality': 0.25,
            'security': 0.40,       # 백엔드: 보안 우선
            'performance': 0.25,
            'accessibility': 0.10
        }
    },
    'database': {
        'keywords': ['query', 'sql', 'database', 'migration'],
        'weights': {
            'quality': 0.20,
            'security': 0.40,       # DB: 보안 매우 중요
            'performance': 0.35,    # 쿼리 성능 중요
            'accessibility': 0.05
        }
    },
    'utility': {
        'keywords': ['util', 'helper', 'lib', 'function'],
        'weights': {
            'quality': 0.35,        # 유틸리티: 품질 우선
            'security': 0.25,
            'performance': 0.30,
            'accessibility': 0.10
        }
    }
}
```

## Skip Conditions

W-R 루프가 건너뛰는 파일:
- Config: `.json`, `.env`, `tsconfig`, `eslint`, `prettier`
- Documentation: `.md`
- Lock files: `.lock`
- Git related: `git`, `config`

## Configuration

```json
{
  "writerReviewer": {
    "enabled": true,
    "targetScore": 0.85,
    "maxIterations": 10,
    "convergenceThreshold": 0.015,
    "agents": {
      "quality": 0.30,
      "security": 0.30,
      "performance": 0.20,
      "accessibility": 0.20
    }
  }
}
```

---

**Related**: [system-architecture.md](system-architecture.md), [scenarios-basic.md](scenarios-basic.md)
