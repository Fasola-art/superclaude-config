# RL Agent (강화학습 에이전트)

> PPO/SAC via Stable-Baselines3, BaseStrategy 인터페이스 준수

---

## 알고리즘 선택

| 알고리즘 | 용도 | 특성 |
|---------|------|------|
| PPO (기본) | 안정적 학습, 초기 배포 | on-policy, 안전 |
| SAC (고급) | 연속 행동 공간 최적화 | off-policy, 샘플 효율 |

---

## State Space (~30차원)

| 카테고리 | 피처 | 차원 |
|---------|------|------|
| 가격 | 수익률, 변동성, ATR | 5 |
| 기술지표 | RSI, MACD, BB위치, EMA배열 | 8 |
| 볼륨 | 거래량 비율, OBV, CVD | 4 |
| LLM 컨피던스 | news, macro, tech, signal | 4 |
| 포지션 상태 | 보유여부, PnL, 보유시간 | 3 |
| 매크로 | VIX, DXY, 금리스프레드 | 3 |
| 시장 레짐 | 변동성 레짐, 추세 강도 | 3 |

**정규화**: 가격→z-score, 지표→0~1, 매크로→min-max

## Action Space

| 행동 | 값 | 설명 |
|------|------|------|
| BUY | 0 | 매수 (사이즈: 0.1~1.0) |
| SELL | 1 | 매도 (사이즈: 0.1~1.0) |
| HOLD | 2 | 관망 |

포지션 사이즈: `base_size * confidence` (0.1 ~ 1.0)

## Reward Function

| 구성 요소 | 계산 | 비고 |
|----------|------|------|
| 기본 보상 | PnL% × 100 | 수익률 기반 |
| Sharpe 보너스 | +0.5 (Sharpe > 1.5) | 안정적 수익 유도 |
| MDD 페널티 | -drawdown × 10 (DD > 10%) | 과도 손실 억제 |
| 과거래 페널티 | -0.3 × (trades - 20) | 일 20회 초과 시 |
| 거래 비용 | -0.1 (매매 시) | 불필요 거래 억제 |

---

## 학습 스케줄

| 항목 | 설정 |
|------|------|
| 디바이스 | 4090 노트북 (야간 00:00~06:00) |
| 추론 디바이스 | RTX 4090 Laptop |
| 학습 주기 | 주 1회 (주말 야간) |
| 에피소드 | 1000+ per training |
| 학습률 | 3e-4 (PPO), 3e-4 (SAC) |
| 배치 | 256 steps |
| 환경 | 최근 6개월 데이터 |

### BaseStrategy 인터페이스

```python
class RLStrategy(BaseStrategy):
    def __init__(self, algo: str = 'PPO', model_path: str = None):
        super().__init__(name=f'RL-{algo}')
        self.algo = algo
        self.model = self._load_model(model_path)

    def generate_signal(self, data: dict) -> TradeSignal:
        state = self.build_state(data)
        action, _states = self.model.predict(state, deterministic=True)
        confidence = self._get_action_probability(state, action)
        return TradeSignal(
            timestamp=data['timestamp'],
            symbol=data['symbol'],
            signal_type=self._map_action(action),
            side=self._map_side(action),
            price=data['price'],
            confidence=float(confidence),
            reason=f'RL-{self.algo}: action={action}, conf={confidence:.2f}'
        )
```

---

## 모델 관리

| 항목 | 경로/설정 |
|------|----------|
| 저장 경로 | `~/.claude/modules/trading/models/rl/` |
| 파일명 | `{algo}_{symbol}_{date}.zip` |
| 버전 관리 | 최근 5개 체크포인트 보존 |
| 롤백 | 성능 하락 시 이전 모델 복구 |

---

**참조**: [decision-pipeline.md](decision-pipeline.md) | [backtesting-pipeline.md](backtesting-pipeline.md)
