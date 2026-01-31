---
description: "코드 정리 (Cleanup code)"
argument-hint: "[target]"
---

# 정리

코드를 정리하고 불필요한 요소를 제거합니다.

## 사용

```
/sc:cleanup            # 전체 프로젝트
/sc:cleanup src/       # 특정 디렉토리
/sc:cleanup --imports  # 미사용 import만
/sc:cleanup --logs     # console.log만
```

## 정리 항목

- 미사용 import 제거
- console.log/debug 제거
- 미사용 변수 경고
- 포매팅 정리
