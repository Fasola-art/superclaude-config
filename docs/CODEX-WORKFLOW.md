# Codex-Claude 협업 워크플로우

> 클로드(설계/검증) + 코덱스/에이전트(구현) 분업 시스템

---

## 역할 정의

| 역할 | 담당자 | 핵심 책임 |
|------|--------|----------|
| 아키텍트 | Claude | 설계 결정, 명세서 작성, 최종 검증 |
| 구현자 | Codex/Agent | 명세서 기반 코드 생성, 테스트 실행 |
| 조율자 | Claude | 핸드오프, 상태 추적, 품질 게이트 |

---

## RACI 요약

| 작업 | Claude | Codex/Agent |
|------|--------|-------------|
| 요구사항 분석 | **R** | I |
| 아키텍처 설계 | **R** | C |
| 코드 구현 (반복) | I | **R** |
| 코드 구현 (복잡) | **R** | C |
| 검증/리뷰 | **R** | I |

전체 RACI → `~/.claude/modules/codex/roles/RACI.md`

---

## 핸드오프 다이어그램

```
사용자 요청
     │
     ▼
[Claude] 작업 분석
     │
     ├─ 클로드 전담 ──────────────────► 직접 처리
     │   (설계/아키텍처/판단)
     │
     └─ 코덱스 적합 ──► [Claude] 명세서 생성
                              │
                              ▼
                         10섹션 명세서
                         + agent-role.md
                              │
                              ▼
                    [Codex/Agent] 구현 실행
                              │
                              ▼
                         완료 보고
                              │
                              ▼
                    [Claude] 5개 품질 게이트
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                통과 → 완료          실패 → 재위임
                    │
                    ▼
             TASKS.md 업데이트
```

---

## WSL2 설정 (Platform Rules v2.1.0)

```bash
# 필수: Codex CLI는 WSL2에서 실행
wsl --install  # Ubuntu 설치

# 프로젝트 파일은 WSL2 filesystem에 위치
~/project/    # ✅ 올바른 경로
/mnt/c/       # ❌ 성능 저하 + I/O 느림

# Codex CLI 실행
codex --model sonnet --file ~/project/.planning/codex-task.md
```

---

## 모델 선택 가이드

| 작업 | 모델 | 이유 |
|------|------|------|
| 복잡 알고리즘/보안 | `opus` | 깊은 추론 필요 |
| 표준 기능 구현 | `sonnet` | 균형 잡힌 성능/비용 |
| 단순 수정/포맷 | `haiku` | 빠르고 저렴 |

---

## 품질 게이트 (5개)

```
1. 기능 완성도  → 명세서 FR/NFR 100% 충족
2. 코드 품질   → 줄 제한 준수 + 린트 통과
3. 타입 안전성 → 타입 힌트/정의 완성
4. 테스트 존재 → 핵심 로직 테스트 포함
5. 의존성 정합 → import/require 실제 존재
```

---

## Context Loss Prevention

```bash
# 핸드오프 전 (클로드)
/compact            # 컨텍스트 압축

# TASKS.md 업데이트 형식
## Status: CODEX_DELEGATED | COMPLETED | BLOCKED
## Done: [완료 목록]
## Next: [다음 단계]
## Blockers: [블로커]
```

---

## 관련 파일

| 파일 | 역할 |
|------|------|
| `modules/codex/task-template.md` | 명세서 템플릿 |
| `modules/codex/roles/agent-role.md` | 에이전트 역할 지침 |
| `modules/codex/roles/RACI.md` | 상세 RACI |
| `skills/codex-workflow/SKILL.md` | 스킬 진입점 |

---

**Version**: 1.0.0
**Platform**: Windows + WSL2 (RTX 4090 Laptop)
