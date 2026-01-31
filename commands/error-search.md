---
description: "Error KB에서 유사 에러 검색 (Search similar errors in Error KB)"
argument-hint: "[error_message]"
---

# Error KB 검색

에러 메시지를 받아 Error KB에서 유사한 해결 사례를 검색합니다.

## 동작

1. 인자로 받은 에러 메시지 또는 최근 에러를 분석
2. `~/.claude/error-kb/resolved/` 에서 Jaccard 유사도 검색 (임계값: 70%)
3. `~/.claude/patterns/error-success-map.json` 에서 Quick Fix 패턴 매칭
4. 유사한 해결 사례가 있으면 솔루션 제시
5. 없으면 새 에러로 등록 제안

## 사용 예시

```
/error-search "Cannot find module 'react'"
/error-search "TS2304: Cannot find name 'useState'"
```

## 출력 형식

```
🔍 Error KB 검색 결과

에러: [에러 메시지 요약]
유형: [module_not_found | typescript_error | ...]

📌 유사 해결 사례 발견 (유사도: 85%)
- 원인: [원인 설명]
- 해결: [해결 방법]
- 명령어: [성공한 명령어]

💡 Quick Fix: [즉시 실행 가능한 수정]
```
