# TODO 우선순위 작업 진행 계획

> 생성일: 2026-02-06
> 목표: High 우선순위 작업 완료

---

## 탐색 결과 요약

### ✅ 이미 구현된 작업 (TODO 업데이트 필요)

| ID | 작업 | 구현 파일 | 라인 수 |
|----|------|----------|--------|
| J-01 | MemoryManager | memory/manager.py | 197줄 |
| JF-02 | Remember | actions/remember.py | 77줄 |
| JF-03 | Do (자율 실행) | actions/do.py | 100줄 |
| JT-01 | NLU 파싱 | nlu/*.py | 7개 파일 |
| JT-02 | SQLite 메모리 | memory/db.py + 스키마 | 10개 테이블 |

### 🟡 부분 구현 (보완 필요)

| ID | 작업 | 현재 상태 | 필요 작업 |
|----|------|---------|---------|
| J-05 | ProjectMonitor | modules/project/ 존재 | 통합 테스트 |
| J-07 | GitHubMonitor | modules/github/ 존재 | API 연동 확인 |

### 🔴 미구현 (실제 작업 대상)

| ID | 작업 | 우선순위 |
|----|------|---------|
| D-01 | 자동화 수정 에이전트 | High |
| D-05 | 자율자동/랄프 시스템 | High |
| T-01 | 실시간 가격 데이터 | High |
| T-02 | WebSocket 연결 | High |

---

## 권장 진행 순서

### Phase 1: TODO 업데이트 (즉시)
- J-01, JF-02, JF-03, JT-01, JT-02 → 완료 처리
- 실제 남은 High 작업: 4개

### Phase 2: Trading 모듈 (T-01, T-02)
**이유**: 실용적 가치 높음, 독립적 구현 가능

1. Yahoo Finance API 연동 (실시간 가격)
2. Binance WebSocket 연결 (암호화폐)
3. 기존 trading 모듈과 통합

**파일 구조**:
```
modules/trading/
├── realtime/
│   ├── __init__.py
│   ├── yahoo_client.py   # ~60줄
│   ├── binance_ws.py     # ~80줄
│   └── price_cache.py    # ~40줄
```

### Phase 3: 자동화 에이전트 (D-01, D-05)
**이유**: 복잡도 높음, Phase 2 완료 후 진행

1. 에러 감지 → 자동 수정 플로우
2. Ralph Loop 통합
3. 기존 agents/ 폴더 활용

---

## 병렬 에이전트 지침 테스트 결과

### 테스트 항목

| 항목 | 결과 |
|------|------|
| 한국어 응답 | ✅ 준수 |
| 라인 수 분석 | ✅ 포함 |
| 기존 코드 참조 | ✅ 완료 |
| 50~120줄 범위 언급 | ✅ 확인 |

### 결론
MANDATORY RULES가 에이전트에 잘 전달됨

---

## 실행 계획 (D → C → B → A 순서)

### Step 1: ProjectMonitor 보완 (J-05, J-07)
1. modules/project/ 통합 테스트
2. modules/github/ API 연동 확인
3. 기존 코드 검증 후 필요시 보완

### Step 2: TODO 정리
1. J-01, JF-02, JF-03, JT-01, JT-02 → 완료 처리
2. J-05, J-07 → 완료 처리 (Step 1 후)

### Step 3: 자동화 에이전트 (D-01, D-05)
1. D-01: 에러 감지/수정 에이전트
2. D-05: Ralph 시스템 개선
3. agents/ 폴더 확장

### Step 4: Trading 모듈 (T-01, T-02)
1. Yahoo Finance 클라이언트 구현
2. Binance WebSocket 구현
3. 통합 테스트

---

## 검증 방법

```bash
# 1. Trading 모듈 테스트
python3 -c "from modules.trading.realtime import get_price; print(get_price('AAPL'))"

# 2. WebSocket 연결 테스트
python3 modules/trading/realtime/binance_ws.py --test

# 3. 통합 테스트
pytest ~/.claude/jarvis/tests/test_trading.py
```

---

## 수정할 파일

| 파일 | 작업 |
|------|------|
| ~/.claude/todo.md | 완료 항목 업데이트 |
| modules/trading/realtime/*.py | 신규 생성 (3개) |
| modules/trading/__init__.py | export 추가 |
