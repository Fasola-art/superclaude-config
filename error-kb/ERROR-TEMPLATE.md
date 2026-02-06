# Error KB 추가 가이드

> 에러 발생 시 유형별 자동 분류 저장

## 폴더 구조

```
error-kb/categories/{technology}/
├── index.md        # 빠른 참조 + 통계
├── critical.md     # 🔴 치명적 에러
├── build.md        # 🟠 빌드 에러
├── runtime.md      # 🟡 런타임 에러
├── config.md       # 🔧 설정 에러
└── archive/        # 원본 백업
```

## 에러 추가 방법

새 에러 발생 시 아래 형식으로 해당 파일에 추가:

```markdown
## [에러 메시지 요약]

**Message**: `정확한 에러 메시지`

**Cause**: 원인 설명

**Solution**:
\`\`\`typescript
// ❌ 문제 코드
...

// ✅ 해결 코드
...
\`\`\`

---
```

## 유형 분류 기준

| 유형 | 파일 | 기준 |
|------|------|------|
| 🔴 Critical | critical.md | 앱 크래시, 보안 이슈 |
| 🟠 Build | build.md | 빌드 실패, 컴파일 에러 |
| 🟡 Runtime | runtime.md | 런타임 예외, API 에러 |
| 🔧 Config | config.md | 설정 오류, 환경 문제 |

## 지원 기술

- nextjs/
- react/
- typescript/
- git/
- mcp/
