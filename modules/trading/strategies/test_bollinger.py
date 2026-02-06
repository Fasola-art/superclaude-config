#!/usr/bin/env python3
"""볼린저 밴드 전략 테스트"""

from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from strategies.bollinger_breakout_strategy import BollingerBreakoutStrategy


def test_strategy():
    """전략 테스트 실행"""
    strategy = BollingerBreakoutStrategy({
        'period': 20,
        'std_dev': 2.0,
        'use_volume_confirmation': True
    })

    print("=== 볼린저 밴드 돌파 전략 테스트 ===\n")

    # 시나리오 1: 하단밴드 이탈
    print("1. 하단밴드 이탈")
    signal1 = strategy.generate_signal({
        'symbol': 'BTC/USD',
        'close': 48000,
        'bb_upper': 52000,
        'bb_middle': 50000,
        'bb_lower': 48500,
        'volume': 1500,
        'avg_volume': 1000,
        'timestamp': datetime.now().isoformat()
    })
    print(f"시그널: {signal1.signal_type.value} / 신뢰도: {signal1.confidence * 100:.1f}%\n")

    # 시나리오 2: 하단밴드 복귀 (매수)
    print("2. 하단밴드 복귀 (매수 시그널)")
    signal2 = strategy.generate_signal({
        'symbol': 'BTC/USD',
        'close': 49000,
        'bb_upper': 52000,
        'bb_middle': 50000,
        'bb_lower': 48500,
        'volume': 1800,
        'avg_volume': 1000,
        'timestamp': datetime.now().isoformat()
    })
    print(f"시그널: {signal2.signal_type.value}")
    print(f"신뢰도: {signal2.confidence * 100:.1f}%")
    print(f"이유: {signal2.reason}")
    print(f"손절가: {signal2.stop_loss:.2f}")
    print(f"목표가: {signal2.target_price:.2f}\n")

    # 시나리오 3: 상단밴드 돌파 후 복귀 (매도)
    strategy.reset()
    print("3. 상단밴드 돌파")
    signal3 = strategy.generate_signal({
        'symbol': 'BTC/USD',
        'close': 52500,
        'bb_upper': 52000,
        'bb_middle': 50000,
        'bb_lower': 48000,
        'volume': 1200,
        'avg_volume': 1000,
        'timestamp': datetime.now().isoformat()
    })
    print(f"시그널: {signal3.signal_type.value}\n")

    print("4. 상단밴드 복귀 (매도 시그널)")
    signal4 = strategy.generate_signal({
        'symbol': 'BTC/USD',
        'close': 51500,
        'bb_upper': 52000,
        'bb_middle': 50000,
        'bb_lower': 48000,
        'volume': 1600,
        'avg_volume': 1000,
        'timestamp': datetime.now().isoformat()
    })
    print(f"시그널: {signal4.signal_type.value}")
    print(f"신뢰도: {signal4.confidence * 100:.1f}%")
    print(f"이유: {signal4.reason}")
    print(f"손절가: {signal4.stop_loss:.2f}")
    print(f"목표가: {signal4.target_price:.2f}")


if __name__ == '__main__':
    test_strategy()
