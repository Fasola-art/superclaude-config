# Vibe/Mode Keywords

> 작업 제어를 위한 키워드 시스템

## Vibe Keywords (13)

| Keyword | Alias | Action | 사용 예 |
|---------|-------|--------|---------|
| 빠르게 | qk, quick | 검증 스킵 | `qk change button color` |
| 실험 | exp | 스냅샷 후 실험 | `exp try this approach` |
| 동시에 | para | 병렬 에이전트 | `para analyze and document` |
| 고쳐 | fix | Error KB 기반 수정 | `fix this error` |
| 되돌려 | undo | 스냅샷 롤백 | `undo to previous state` |
| 계속 | cont | 이전 상태 계속 | `cont continue work` |
| 확인해 | chk | 전체 검증 | `확인해 quality check` |
| 테스트해 | tst | 테스트 실행 | `tst run all tests` |
| 배포해 | dep | 배포 체크리스트 | `dep production deploy` |
| 정리해 | clean | 코드 정리 | `clean remove unused` |
| 성능 | perf | 성능 분석 | `perf find bottleneck` |
| 계획 | plan | 계획 문서화 | `plan create plan` |
| 분석 | map | 코드베이스 분석 | `map understand structure` |

## Mode Keywords (4)

| Mode | Alias | Activated Personas | Purpose |
|------|-------|-------------------|---------|
| ultrawork | ulw | explorer, librarian, analyzer | 집중 작업 |
| deepsearch | ds | explorer | 딥 서치 |
| strategic | str | architect | 전략적 설계 |
| visual | vis | multimodal, frontend | 비주얼 작업 |

## 사용 예시

```bash
# Vibe Keywords
> "qk add API endpoint"
🎯 vibe:빠르게
→ 검증 스킵, 즉시 실행

> "para security check and performance analysis"
🎯 vibe:동시에
→ 두 작업 병렬 실행

# Mode Keywords
> "ulw implement this feature"
🎯 mode:ultrawork
→ explorer, librarian, analyzer 페르소나 활성화

> "ds find this bug cause"
🎯 mode:deepsearch
→ explorer 페르소나로 딥 탐색
```

---

**Related**: [hook-system.md](hook-system.md), [quick-reference.md](quick-reference.md)
