# 로컬 LLM 서브에이전트 트레이딩 시스템

> **목표**: 최소 사양 모델로 최대 효율, 저전력/저비용 운영
> **환경**: Mac Studio Ultra M2 (192GB), MLX 런타임

---

## 아키텍처 개요

```
Claude Code (Main) ─────────────────────────────────────────────────
       │
       ├──▶ MCP local-llm 서버 ──▶ MLX 모델 풀
       │         │
       │         ├─ Qwen2.5-3B (상주) ─ 뉴스 분류
       │         └─ Qwen2.5-7B (온디맨드) ─ 지표 해석, 시그널 검증
       │
       └──▶ 기존 모듈 (trading, news-collector, sql-trading)
```

---

## 서브에이전트 구성 (4개)

| 에이전트 | 모델 | 양자화 | VRAM | 역할 |
|----------|------|--------|------|------|
| NewsClassifier | Qwen2.5-3B | Q4_K_M | ~2GB | 뉴스 분류/감성 분석 |
| IndicatorInterpreter | Qwen2.5-7B | Q5_K_M | ~6GB | 경제 지표 해석 |
| SignalValidator | Qwen2.5-7B | Q5_K_M | ~6GB | 시그널 검증/신뢰도 평가 |
| ReportDrafter | Qwen2.5-7B | Q5_K_M | ~6GB | 리포트 초안 작성 |

**역할 분담 원칙**:
- **로컬 LLM**: 대량 처리, 반복 작업, 정형 분석
- **Claude API**: 복잡한 추론, 전략 수립, 신규 패턴 발견

---

## 구현 로드맵

### Phase 1: 기반 인프라 (1주)

**작업**:
1. MLX 설치 및 모델 다운로드
2. MCP 서버 래퍼 구현
3. 모델 로딩/언로딩 관리자

**생성 파일**:
```
~/.claude/modules/local-llm/
├── __init__.py
├── index.py              # barrel export
├── types.py              # 타입 정의 (≤20 lines)
├── constants.py          # 상수 (≤20 lines)
├── mlx_server.py         # MLX 모델 서버 (≤80 lines)
├── mcp_wrapper.py        # MCP stdio 래퍼 (≤80 lines)
├── model_manager.py      # 모델 관리 (≤50 lines)
├── cache.py              # 결과 캐싱 (≤50 lines)
└── config.json
```

**수정 파일**:
- `~/.claude/mcp-router/servers.json` - local-llm 서버 등록

### Phase 2: 핵심 에이전트 (2주)

**작업**:
1. NewsClassifier 구현 + news_module.py 통합
2. IndicatorInterpreter 구현 + sql-trading 연동
3. 프롬프트 템플릿 작성

**생성 파일**:
```
~/.claude/modules/local-llm/agents/
├── __init__.py
├── base_agent.py           # 기본 클래스 (≤50 lines)
├── news_classifier.py      # 뉴스 분류 (≤80 lines)
├── indicator_interpreter.py # 지표 해석 (≤80 lines)
└── prompts/
    ├── news_classification.md
    └── indicator_interpretation.md
```

### Phase 3: 시그널 및 리포트 (1주)

**작업**:
1. SignalValidator 구현 + trading_module.py 통합
2. ReportDrafter 구현

**생성 파일**:
```
~/.claude/modules/local-llm/agents/
├── signal_validator.py     # 시그널 검증 (≤80 lines)
├── report_drafter.py       # 리포트 작성 (≤80 lines)
└── prompts/
    ├── signal_validation.md
    └── report_draft.md
```

### Phase 4: 파이프라인 통합 (1주)

**작업**:
1. Hook 시스템 연동
2. 자동화 파이프라인 구성
3. 스케줄러 설정

**생성 파일**:
```
~/.claude/modules/local-llm/
├── orchestrator.py         # 작업 조율 (≤80 lines)
└── pipelines/
    ├── __init__.py
    ├── morning_briefing.py # 아침 브리핑
    └── signal_pipeline.py  # 시그널 파이프라인

~/.claude/hooks/PostToolUse/
└── local_llm_trigger.py    # Hook 트리거
```

---

## 모델 로딩 전략

```python
MODEL_STRATEGY = {
    "always_loaded": ["qwen2.5-3b-instruct-q4"],  # ~2GB
    "on_demand": ["qwen2.5-7b-instruct-q5"],      # ~6GB
    "cache_timeout_minutes": 30,
    "max_concurrent_models": 2,
}
```

**전력 최적화**:
- 유휴 5분 후 7B 모델 언로드
- 배치 작업은 야간 (22:00~06:00)
- 실시간 작업만 주간 처리

---

## 통합 포인트

### 1. NewsClassifier ↔ news_module.py
```python
# news_module.py의 NewsArticle.sentiment 필드 활용
# NewsClassifier 출력 → sentiment, priority 자동 설정
```

### 2. SignalValidator ↔ trading_module.py
```python
# TradingSignal.confidence, TradingSignal.reason 필드 활용
# SignalValidator 출력 → confidence 조정, reason 상세화
```

### 3. IndicatorInterpreter ↔ sql-trading
```python
# economic_indicators 테이블에서 데이터 조회
# 해석 결과 → indicator_interpretations 테이블 저장
```

---

## MCP 서버 등록

```json
{
  "local-llm": {
    "command": "python3",
    "args": ["-m", "local_llm.mcp_wrapper"],
    "env": {
      "MLX_MODEL_PATH": "~/.claude/modules/local-llm/models/",
      "DEFAULT_MODEL": "qwen2.5-7b-instruct-q5"
    },
    "description": "로컬 LLM 서브에이전트",
    "enabled": true
  }
}
```

---

## 예상 비용 절감

| 항목 | 기존 (API Only) | 하이브리드 | 절감 |
|------|-----------------|-----------|------|
| 뉴스 분류 (10K/일) | ~$15/일 | $0 | 100% |
| 지표 해석 (100/일) | ~$3/일 | $0 | 100% |
| 시그널 검증 (50/일) | ~$2/일 | $0 | 100% |
| **월간 합계** | ~$600 | ~$100 | **83%** |

---

## 검증 방법

### Phase 1 검증
```bash
# MLX 서버 테스트
python3 -m local_llm.mlx_server --test

# MCP 연결 테스트
claude mcp test local-llm
```

### Phase 2-3 검증
```bash
# 에이전트 단위 테스트
pytest ~/.claude/modules/local-llm/tests/

# 통합 테스트
python3 -m local_llm.agents.news_classifier --test-batch
```

### Phase 4 검증
```bash
# 파이프라인 E2E 테스트
python3 -m local_llm.pipelines.signal_pipeline --dry-run

# 24시간 모니터링
python3 -m local_llm.monitor --duration 24h
```

---

## 주요 수정 파일

1. `~/.claude/mcp-router/servers.json` - local-llm 서버 추가
2. `~/.claude/modules/news-collector/news_module.py` - NewsClassifier 통합
3. `~/.claude/modules/trading/trading_module.py` - SignalValidator 통합
4. `~/.claude/modules/sql-trading/config.json` - IndicatorInterpreter 연동

---

## 위험 및 대응

| 위험 | 대응 |
|------|------|
| 모델 품질 부족 | confidence 임계값 설정, 낮으면 Claude API 에스컬레이션 |
| 메모리 부족 | 동시 로딩 2개 제한, 7B 모델 온디맨드 로드 |
| 응답 지연 | 배치/실시간 분리, 타임아웃 설정 |

---

**META**
- 계획 버전: 1.0
- 생성일: 2026-02-03
- 예상 기간: 5주
