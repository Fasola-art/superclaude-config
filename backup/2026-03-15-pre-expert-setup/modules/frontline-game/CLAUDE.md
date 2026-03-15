# Frontline Game - WW2 Bid/Ask War

> Next.js 15 + React 19 + Canvas 2D + Zustand

## 구조

```
src/
├── app/          # Next.js App Router
├── components/   # UI 컴포넌트 (6개)
├── hooks/        # useBattle 훅
├── lib/          # 엔진, 물리, 렌더러
└── types/        # 타입 정의
```

## 키 매핑

| 키 | ForceType | 진영 | 역할 |
|----|-----------|------|------|
| Space | marketBuy | germany | drill |
| → | limitBuy | germany | shield |
| ← | marketSell | soviet | drill |
| Ctrl/Shift | limitSell | soviet | shield |

## 규칙

- 파일 50~150줄 유지
- 한국어 주석
- data-testid 필수 (E2E용)
- Canvas 렌더링은 renderer.ts에 집중
- 상태관리: Zustand (Phase 2)

## 명령어

```bash
pnpm dev          # 개발 서버
pnpm build        # 빌드
pnpm test:e2e     # E2E 테스트
```
