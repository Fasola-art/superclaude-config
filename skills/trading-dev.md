---
name: trading-dev
description: Trading module development guide and rules
version: "1.0.0"
triggers:
  - /trading-dev
  - trading 모듈 개발
  - 새 전략 추가
---

# Trading Development Skill

## 내장 규칙

에이전트는 다음 규칙을 반드시 준수:

1. **파일 제한**: 50~120줄 범위 유지
2. **타입 힌트**: Python 타입 힌트 필수
3. **기존 패턴**: `~/.claude/modules/trading/` 구조 유지
4. **No stub**: 완전한 구현만 (placeholder 금지)

## 사용법

```bash
/trading-dev [action] [target]

# 예시
/trading-dev add strategy momentum_breakout
/trading-dev add indicator rsi_divergence
/trading-dev analyze AAPL
```

## 작업 가이드

### 새 전략 추가

1. `strategies/base_strategy.py` 확인
2. `strategies/` 폴더에 새 파일 생성
3. BaseStrategy 상속
4. `generate_signal()` 구현

### 새 지표 추가

1. `indicators/technical_indicators.py` 확인
2. 기존 패턴 따라 함수 추가
3. 타입 힌트 + docstring 필수

### 데이터 소스 추가

1. `data_sources/` 폴더 확인
2. 기존 패턴 따라 클래스 생성
3. `fetch()`, `parse()` 메서드 구현

## 참조

- 모듈: `~/.claude/modules/trading/`
- 설정: `config.py`, `config.json`
- DB: `~/.claude/modules/sql-trading/schema.sql`
