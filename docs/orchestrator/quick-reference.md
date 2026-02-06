# Quick Reference

> 자주 사용하는 키워드, 명령어, 설정 파일

## 자주 사용하는 키워드

| Situation | Keyword | Effect |
|-----------|---------|--------|
| 빠른 수정 | `qk` | 검증 스킵 |
| 병렬 작업 | `para` | 병렬 에이전트 실행 |
| 오류 수정 | `fix` | Error KB 기반 수정 |
| 품질 확인 | `확인해` | 전체 검증 실행 |
| 테스팅 | `tst` | 테스트 실행 |
| 성능 분석 | `perf` | 성능 병목 분석 |
| 딥 서치 | `ds` | 딥 서치 모드 |

## 자주 사용하는 명령어

| Command | Purpose |
|---------|---------|
| `/orchestrator [topic]` | 종합 리서치 |
| `/generate-tests [file]` | 테스트 생성 |
| `/project-plan` | 프로젝트 계획 |
| `/commit` | Git 커밋 |
| `/review-pr` | PR 리뷰 |
| `/sc:analyze` | 코드 분석 |

## 주요 설정 파일

| File | Location | Purpose |
|------|----------|---------|
| CLAUDE.md | `~/.claude/CLAUDE.md` | 전역 지시사항 |
| settings.json | `~/.claude/settings.json` | 권한/훅 설정 |
| superclaude-config.json | `~/.claude/superclaude-config.json` | 병렬/W-R 설정 |
| servers.json | `~/.claude/mcp-router/servers.json` | MCP 서버 |

## 훅 출력 해석

| Output | Meaning |
|--------|---------|
| `🎯 vibe:빠르게` | 빠른 모드 활성화 |
| `🎯 mode:deepsearch` | 딥 서치 모드 활성화 |
| `🔍 QG:python → '확인해' for verify` | 품질 게이트 대기 |
| `⚠️ Loop:3/5` | 연속 실패 경고 |
| `🛑 Loop:5 → Manual intervention` | 무한 루프 감지 |

---

## Troubleshooting

### Q: W-R 루프가 계속 반복됨

```bash
# 해결: 수렴 임계값 확인
convergenceThreshold: 0.015
# 개선 < 1.5%면 자동 종료

# 또는 maxIterations 조정
maxIterations: 10 → 5로 감소
```

### Q: 병렬 에이전트가 느림

```bash
# 해결: 동시 실행 수 조정
# superclaude-config.json:
"initial": 10 → 5로 감소
"maximum": 24 → 12로 감소
```

### Q: 특정 파일에 훅이 작동 안 함

```bash
# 해결: 스킵 조건 확인
SKIP_CONDITIONS = ['git', 'config', '.md', '.json', ...]
# 패턴 매치 시 훅 스킵
```

---

**Related**: [index.md](index.md), [vibe-mode-keywords.md](vibe-mode-keywords.md)
