# Trading Module Rules

> 이 폴더에서 작업하는 에이전트는 반드시 준수

## 필수 규칙

| 규칙 | 설명 |
|------|------|
| 파일 제한 | 50~120줄 범위 유지 |
| 타입 힌트 | Python 타입 힌트 필수 |
| 기존 패턴 | 기존 코드 스타일 유지 |

## 폴더 구조

```
trading/
├── trading_module.py      # 메인 모듈
├── config.py / config.json # 설정
├── strategies/            # 전략 파일
│   ├── base_strategy.py   # 기본 클래스 (상속 필수)
│   ├── momentum_strategy.py
│   └── mean_reversion_strategy.py
├── indicators/            # 기술 지표
│   └── technical_indicators.py
├── data_sources/          # 데이터 소스
│   ├── fred_monitor.py    # FRED API
│   ├── cot_report.py      # COT 리포트
│   └── economic_calendar.py
├── backtesting/           # 백테스팅
│   └── backtest_engine.py
└── reports/               # 리포트 생성
    └── daily_economic_report.py
```

## 새 전략 추가

```python
from strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    """전략 설명 (필수)"""

    def generate_signal(self, data: pd.DataFrame) -> str:
        # 완전한 구현 필수 (No stub)
        ...
```

## 참조 파일

- 메인: `trading_module.py`
- 설정: `config.py`, `config.json`
- DB 스키마: `../sql-trading/schema.sql`
