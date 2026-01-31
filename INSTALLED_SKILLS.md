# 설치된 스킬 목록

> SuperClaude v2.0.9 스킬 현황

---

## 핵심 스킬 (Built-in)

| 스킬 | 버전 | 상태 | 설명 |
|------|------|------|------|
| prd-create | 1.0.0 | ✅ 활성 | 아이디어 → PRD 생성 |
| project-plan | 1.0.0 | ✅ 활성 | PRD → 프로젝트 시작 |
| project-status | 1.0.0 | ✅ 활성 | 진행 상황 확인 |
| project-continue | 1.0.0 | ✅ 활성 | 이전 작업 계속 |
| ideation | 1.0.0 | ✅ 활성 | 다중 페르소나 토론 |
| research | 1.0.0 | ✅ 활성 | 범용 딥리서치 |
| error-search | 1.0.0 | ✅ 활성 | Error KB 검색 |
| recover | 1.0.0 | ✅ 활성 | 세션 복구 |

---

## 명령어 스킬 (Commands)

| 스킬 | 위치 | 설명 |
|------|------|------|
| code-with-review | commands/ | 리뷰 포함 코드 생성 |
| vibe | commands/ | Vibe 설정 확인 |
| i | commands/ | 즉각 정보 조회 |

---

## SC 서브커맨드 (commands/sc/)

| 스킬 | 설명 |
|------|------|
| analyze | 코드 분석 |
| build | 빌드 실행 |
| cleanup | 코드 정리 |
| design | 설계 문서 생성 |
| document | 문서화 |
| estimate | 작업량 추정 |
| explain | 코드 설명 |
| git | Git 작업 |
| implement | 구현 |
| improve | 개선 제안 |
| index | 인덱스 생성 |
| load | 컨텍스트 로드 |
| spawn | 에이전트 생성 |
| task | 태스크 관리 |
| test | 테스트 실행 |
| troubleshoot | 문제 해결 |
| workflow | 워크플로우 실행 |

---

## Vercel React 스킬 (49개 규칙)

| 카테고리 | 규칙 수 | 상태 |
|----------|--------|------|
| ASYNC | 5 | ✅ 활성 |
| BUNDLE | 5 | ✅ 활성 |
| SERVER | 5 | ✅ 활성 |
| RENDER | 5 | ✅ 활성 |
| RERENDER | 7 | ✅ 활성 |
| IMAGE | 5 | ✅ 활성 |
| CACHE | 5 | ✅ 활성 |
| JS-OPT | 12 | ✅ 활성 |

---

## 추가 모듈 스킬 (계획됨)

| 모듈 | 스킬 | 상태 |
|------|------|------|
| trading | /trade-analyze | 🔜 계획 |
| trading | /backtest | 🔜 계획 |
| news-collector | /news-fetch | 🔜 계획 |
| news-collector | /news-filter | 🔜 계획 |
| realtime-analysis | /stream-start | 🔜 계획 |
| realtime-analysis | /dashboard | 🔜 계획 |

---

## 스킬 통계

```yaml
total_skills: 25+
built_in: 8
commands: 3
sc_subcommands: 17
vercel_rules: 49
planned: 6
```

---

## 최근 업데이트

| 날짜 | 변경 |
|------|------|
| 2026-01-29 | 초기 설치 완료 |
