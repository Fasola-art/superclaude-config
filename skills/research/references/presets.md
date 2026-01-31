# Research 프리셋 정의

> 10개 프리셋의 상세 설정

---

## 프리셋 목록

### 1. market_research (시장 조사)

```yaml
name: market_research
description: 시장 규모, 트렌드, CAGR, 경쟁 구도 분석
triggers:
  - "시장"
  - "market"
  - "TAM"
  - "SAM"
  - "SOM"
  - "규모"
  - "성장률"

defaults:
  depth: deep
  format: report
  breadth: 10

queries_template:
  - "[주제] market size 2026"
  - "[주제] TAM SAM SOM"
  - "[주제] industry trends"
  - "[주제] key players market share"
  - "[주제] CAGR growth forecast"
  - "[주제] competitive landscape"
  - "[주제] market drivers challenges"
  - "[주제] regional analysis"

output_structure:
  - 핵심 요약 (Executive Summary)
  - 시장 규모 및 성장률
  - 주요 플레이어 분석
  - 트렌드 및 동인
  - 지역별 분석
  - 전망 및 예측
  - 참고문헌
```

### 2. competitor_analysis (경쟁사 분석)

```yaml
name: competitor_analysis
description: A vs B 상세 비교, 장단점, 추천
triggers:
  - "vs"
  - "비교"
  - "compare"
  - "차이"
  - "versus"

defaults:
  depth: deep
  format: comparison
  breadth: 8

queries_template:
  - "[A] vs [B] comparison"
  - "[A] [B] differences"
  - "[A] pros cons"
  - "[B] pros cons"
  - "[A] [B] pricing"
  - "[A] [B] features"
  - "[A] vs [B] review 2026"
  - "[A] [B] use cases"

output_structure:
  - 비교 요약표
  - 기능별 상세 비교
  - 가격 및 플랜 비교
  - 장단점 정리
  - 사용 사례별 추천
  - 결론 및 추천
```

### 3. tech_research (기술 조사)

```yaml
name: tech_research
description: 기술 스택, 프레임워크, 라이브러리 조사
triggers:
  - "기술"
  - "tech"
  - "framework"
  - "library"
  - "스택"
  - "stack"

defaults:
  depth: medium
  format: report
  breadth: 8

queries_template:
  - "[주제] documentation"
  - "[주제] best practices 2026"
  - "[주제] tutorial getting started"
  - "[주제] architecture patterns"
  - "[주제] performance benchmarks"
  - "[주제] ecosystem libraries"

output_structure:
  - 기술 개요
  - 핵심 개념
  - 아키텍처
  - 장단점
  - 사용 사례
  - 학습 자료
```

### 4. academic_research (학술 조사)

```yaml
name: academic_research
description: 학술 논문, 연구 결과, 이론적 배경
triggers:
  - "논문"
  - "연구"
  - "paper"
  - "research"
  - "study"
  - "학술"

defaults:
  depth: deep
  format: report
  breadth: 12

queries_template:
  - "[주제] research paper"
  - "[주제] academic study"
  - "[주제] literature review"
  - "[주제] theoretical framework"
  - "[주제] empirical evidence"
  - "[주제] methodology"
  - "[주제] recent findings 2026"

output_structure:
  - 연구 배경
  - 이론적 프레임워크
  - 주요 연구 결과
  - 방법론 비교
  - 한계점 및 향후 연구
  - 참고문헌 (학술 형식)
```

### 5. decision_support (의사결정 지원)

```yaml
name: decision_support
description: 선택지 평가, 의사결정 지원
triggers:
  - "선택"
  - "결정"
  - "어떤 것"
  - "추천"
  - "recommend"
  - "which"
  - "should I"

defaults:
  depth: medium
  format: comparison
  breadth: 6

queries_template:
  - "[주제] comparison guide"
  - "[주제] pros cons analysis"
  - "[주제] decision criteria"
  - "[주제] expert recommendations"
  - "[주제] use case scenarios"

output_structure:
  - 의사결정 기준
  - 옵션별 평가
  - 시나리오별 추천
  - 리스크 분석
  - 최종 권고사항
```

### 6. general_inquiry (일반 질문)

```yaml
name: general_inquiry
description: 일반적인 질문에 대한 간결한 답변
triggers:
  - "뭐야"
  - "무엇"
  - "what is"
  - "explain"
  - "설명"

defaults:
  depth: quick
  format: summary
  breadth: 5

queries_template:
  - "[주제] explained"
  - "[주제] definition"
  - "[주제] overview"
  - "[주제] basics"

output_structure:
  - 정의
  - 핵심 개념
  - 주요 특징
  - 관련 자료
```

### 7. product_review (제품 리뷰)

```yaml
name: product_review
description: 제품/서비스 리뷰, 사용기
triggers:
  - "리뷰"
  - "review"
  - "사용기"
  - "후기"
  - "평가"

defaults:
  depth: medium
  format: comparison
  breadth: 8

queries_template:
  - "[제품] review 2026"
  - "[제품] user experience"
  - "[제품] pros cons"
  - "[제품] alternatives"
  - "[제품] pricing plans"
  - "[제품] customer feedback"

output_structure:
  - 제품 개요
  - 주요 기능
  - 장단점
  - 사용자 피드백 요약
  - 대안 제품
  - 총평
```

### 8. how_to (방법론)

```yaml
name: how_to
description: 튜토리얼, 가이드, 방법론
triggers:
  - "방법"
  - "어떻게"
  - "how to"
  - "가이드"
  - "guide"
  - "tutorial"

defaults:
  depth: quick
  format: summary
  breadth: 5

queries_template:
  - "how to [주제]"
  - "[주제] tutorial"
  - "[주제] step by step guide"
  - "[주제] best practices"

output_structure:
  - 개요
  - 단계별 가이드
  - 팁 및 주의사항
  - 참고 자료
```

### 9. news_analysis (뉴스 분석)

```yaml
name: news_analysis
description: 최신 뉴스, 시사 분석
triggers:
  - "뉴스"
  - "news"
  - "최신"
  - "latest"
  - "recent"
  - "today"

defaults:
  depth: medium
  format: report
  breadth: 10

queries_template:
  - "[주제] news today"
  - "[주제] latest developments"
  - "[주제] breaking news"
  - "[주제] analysis"
  - "[주제] impact implications"

output_structure:
  - 핵심 뉴스 요약
  - 배경 설명
  - 영향 분석
  - 전문가 의견
  - 전망
```

### 10. troubleshooting (문제 해결)

```yaml
name: troubleshooting
description: 오류 해결, 디버깅, 문제 진단
triggers:
  - "에러"
  - "오류"
  - "error"
  - "문제"
  - "안됨"
  - "doesn't work"
  - "fix"
  - "해결"

defaults:
  depth: quick
  format: summary
  breadth: 5

queries_template:
  - "[오류 메시지] solution"
  - "[오류 메시지] fix"
  - "[주제] common issues"
  - "[주제] troubleshooting guide"

output_structure:
  - 문제 요약
  - 원인 분석
  - 해결 방법 (단계별)
  - 예방 조치
```

---

## 프리셋 자동 감지 로직

```typescript
function detectPreset(input: string): PresetType {
  const lowercaseInput = input.toLowerCase();

  // 우선순위 순서대로 검사
  const presetOrder = [
    'competitor_analysis',  // "vs", "비교" 먼저 검사
    'troubleshooting',      // "error", "오류"
    'how_to',               // "how to", "방법"
    'news_analysis',        // "news", "뉴스"
    'product_review',       // "review", "리뷰"
    'market_research',      // "market", "시장"
    'tech_research',        // "tech", "기술"
    'academic_research',    // "paper", "논문"
    'decision_support',     // "which", "어떤"
    'general_inquiry'       // 기본값
  ];

  for (const preset of presetOrder) {
    if (matchesTriggers(lowercaseInput, PRESETS[preset].triggers)) {
      return preset;
    }
  }

  return 'general_inquiry';
}
```

---

## 프리셋 오버라이드

사용자가 명시적으로 설정을 변경할 수 있습니다:

```
/research AI 시장 --depth=exhaustive --format=comparison
```

| 옵션 | 설명 | 값 |
|------|------|-----|
| --depth | 깊이 수준 | quick, medium, deep, exhaustive |
| --format | 출력 형식 | summary, report, comparison |
| --breadth | 소스 수 | 숫자 |
| --no-verify | 교차검증 스킵 | - |
