# Writer-Reviewer 시스템 상세 (Writer-Reviewer System)

> 4-Agent 병렬 코드 검토 시스템 상세 문서

---

## 시스템 개요

Writer-Reviewer는 코드 생성 시 자동으로 4개의 에이전트가 병렬로 검토하는 품질 보장 시스템입니다.

---

## 아키텍처

```
[코드 요청]
    │
    ▼
[Writer] ──────────────────────────────┐
    │                                  │
    ▼                                  ▼
[4-Agent 병렬 검토]              [코드 생성]
    │
    ├── Quality Agent (30%)
    ├── Security Agent (30%)
    ├── Performance Agent (20%)
    └── Accessibility Agent (20%)
    │
    ▼
[점수 통합] ─── < 0.85 ──► [재검토/수정]
    │                           │
    ▼                           │
[수렴 확인] ◄──────────────────┘
    │
    ▼
[완료]
```

---

## 설정

### 기본 설정
```yaml
# ~/.claude/WRITER-REVIEWER.md
target_score: 0.85
max_iterations: 10
convergence_threshold: 0.015
```

### 코드 타입별 가중치
| 타입 | Quality | Security | Performance | Accessibility |
|------|---------|----------|-------------|---------------|
| frontend | 0.25 | 0.25 | 0.20 | **0.30** |
| backend | 0.25 | **0.40** | 0.25 | 0.10 |
| utility | **0.35** | 0.25 | 0.30 | 0.10 |
| database | 0.20 | **0.40** | **0.35** | 0.05 |

---

## 에이전트 상세

### Quality Agent
**검사 항목:**
- 코드 가독성 (네이밍, 구조)
- 타입 안전성
- 에러 처리
- SOLID 원칙
- DRY 원칙

### Security Agent
**검사 항목:**
- XSS 취약점
- SQL Injection
- 인증/권한
- 민감 정보 노출
- 입력 검증

### Performance Agent
**검사 항목:**
- 알고리즘 효율성
- 메모리 관리
- 불필요한 렌더링
- N+1 쿼리
- 번들 크기

### Accessibility Agent
**검사 항목:**
- 시맨틱 HTML
- ARIA 레이블
- 키보드 네비게이션
- 색상 대비
- 포커스 관리

---

## 수렴 조건

### 조기 종료
- 목표 점수 (0.85) 달성
- 모든 카테고리 0.80 이상
- 2회 연속 변화 < 0.015

### 보안 최소 점수
```yaml
security_minimum:
  score: 0.85
  block_early_exit_if:
    security_score < 0.85
    has_critical_issues: true
    any_category < 0.70
```

---

## 플래그

| 플래그 | 효과 |
|--------|------|
| `--no-review` | 비활성화 (보안 코드 제외) |
| `--review-strict` | 목표 0.90 |
| `--review-quick` | 최대 3회 |
| `--review-verbose` | 상세 출력 |

---

## 참조

- `~/.claude/WRITER-REVIEWER.md` - 메인 설정
- `~/.claude/hooks/PreToolUse/writer-reviewer-hook.py` - 훅 구현
