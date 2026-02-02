# 문서 템플릿 (Document Template)

> 표준 문서 작성을 위한 템플릿

---

## 문서 헤더

```markdown
# [문서 제목]

> [한 줄 설명]
> 버전: [X.Y.Z]
> 최종 수정: [YYYY-MM-DD]

---
```

## 표준 구조

### 1. 개요 (Overview)
- 문서 목적
- 대상 독자
- 관련 문서 링크

### 2. 핵심 내용 (Core Content)
- 주요 개념 설명
- 구조/다이어그램
- 코드 예시

### 3. 사용법 (Usage)
- 단계별 가이드
- 예시 코드
- 주의사항

### 4. 참조 (Reference)
- 관련 문서
- 외부 링크
- API 문서

---

## 마크다운 규칙

### 제목
```markdown
# H1: 문서 제목
## H2: 주요 섹션
### H3: 하위 섹션
#### H4: 세부 항목
```

### 코드 블록
````markdown
```typescript
// 언어 명시
const example = 'code';
```
````

### 테이블
```markdown
| 열1 | 열2 | 열3 |
|-----|-----|-----|
| A   | B   | C   |
```

### 체크리스트
```markdown
- [ ] 미완료 항목
- [x] 완료 항목
```

---

## 파일 명명 규칙

- 대문자 + 하이픈: `DOCUMENT-NAME.md`
- 소문자 + 언더스코어: `document_name.md`
- 버전 포함: `DOCUMENT-v2.0.md`
