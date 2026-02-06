# JARVIS 시스템

> **Version**: 2026.02 | **Status**: Planning

---

## 개요

AI 개인 비서 시스템. 자연어로 작업 지시 → 자율 실행.

**핵심 특징:**
- 자연어 파싱 (NLU): 명령어 없이 의도 파악
- 로컬 메모리: SQLite 기반 프라이버시
- 브라우저 자동화: Chrome Extension 연동
- 병렬 처리: 독립 작업 동시 실행
- 학습: 패턴 분석으로 정확한 제안

---

## 문서 구조

| 문서 | 내용 |
|------|------|
| [architecture.md](architecture.md) | 시스템 아키텍처, 모듈 설계 |
| [api-reference.md](api-reference.md) | 기능별 API 명세 |
| [modules.md](modules.md) | 모듈별 상세 설명 |

---

## 빠른 시작

```bash
# 브리핑
/j

# 작업 연속성
/j 어제 뭐했더라?

# 자율 실행
/j 이력서 작성해줘

# 예약
/j 레스토랑 예약해
```

---

## 주요 기능

| 카테고리 | 기능 |
|---------|------|
| 일상 | 브리핑, 작업 연속성, 리마인더 |
| 자동화 | 자율 실행, 예약, 이벤트 계획 |
| 건강 | 운동 코칭, 식단 관리, 습관 트래킹 |
| 프로젝트 | 프로젝트 모니터링, 클라이언트 작업, GitHub 연동 |

자세한 내용은 [api-reference.md](api-reference.md) 참고.

---

**META**
- Created: 2026-02-02
- Last Updated: 2026-02-05
