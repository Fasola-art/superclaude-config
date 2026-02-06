# Priority Level Reference

> 모든 규칙 파일에서 사용하는 공통 우선순위 정의

## Priority Levels

| Priority | 의미 | 적용 |
|----------|------|------|
| CRITICAL | 필수 적용 | 코드 리뷰 블로커 |
| HIGH | 강력 권장 | 리뷰 시 지적 |
| MEDIUM | 권장 | 상황에 따라 |
| LOW | 선택 | 최적화 단계 |

## 적용 원칙

1. **CRITICAL**: 위반 시 PR 머지 불가
2. **HIGH**: 합당한 사유 없으면 수정 요청
3. **MEDIUM**: 새 코드에 적용, 기존 코드는 점진적
4. **LOW**: 성능 이슈 발생 시 적용
