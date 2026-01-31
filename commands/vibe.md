---
description: "현재 세션 Vibe 설정 확인 및 변경 (Check and set session vibe)"
argument-hint: "[vibe_name]"
---

# Vibe 설정

현재 세션의 Vibe(작업 모드/톤앤매너)를 확인하거나 변경합니다.

## 사용 가능한 Vibe

| Vibe | 설명 | 활성화 페르소나 |
|------|------|----------------|
| `default` | 기본 모드 | - |
| `ultrawork` | 최대 성능 | explorer, librarian, analyzer |
| `deepsearch` | 딥리서치 | explorer |
| `strategic` | 전략적 분석 | architect |
| `visual` | 시각 분석 | multimodal, frontend |

## 사용 예시

```
/vibe              # 현재 Vibe 확인
/vibe ultrawork    # Ultrawork 모드 설정
/vibe strategic    # Strategic 모드 설정
```

## 동작

1. 인자 없이 실행: 현재 Vibe 상태 표시
2. Vibe 이름 지정: 해당 모드로 전환
3. 관련 페르소나 자동 활성화
4. 세션 설정 업데이트

## 출력 형식

```
🎨 Vibe 설정

현재 Vibe: [vibe_name]
활성 페르소나: [persona_list]

설정:
- 병렬 실행: [활성/비활성]
- 검토 수준: [strict/normal/quick]
- 출력 스타일: [상세/간결]

변경하려면: /vibe [vibe_name]
```
