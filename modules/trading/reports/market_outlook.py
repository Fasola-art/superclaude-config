#!/usr/bin/env python3
"""
경제 시황 및 전망 자동 생성
- Claude Haiku API + Prompt Caching 사용
- 매일 저녁 10시 자동 생성
- 캐시 적용으로 90% 비용 절감

API 키 설정:
    export ANTHROPIC_API_KEY="your-api-key"
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

REPORTS_DIR = Path.home() / ".claude" / "modules" / "trading" / "reports" / "daily"


def generate_asset_analysis(quotes: Dict, indicators: list) -> str:
    """종목별 상세 분석 및 전망 생성"""

    analysis_sections = []
    ind_dict = {i['series_id']: i for i in indicators}

    # === 1. VIX 분석 ===
    vix = quotes.get('VIX', {})
    vix_price = vix.get('price', 0)
    vix_change = vix.get('change_pct', 0)

    if vix_price > 0:
        if vix_price < 12:
            hist_level = "역사적 저점 (과도한 낙관)"
            outlook = "변동성 반등 가능성. 풋옵션 프리미엄 저렴."
        elif vix_price < 15:
            hist_level = "안정적 낮은 수준"
            outlook = "상승 우호적 환경 지속 예상."
        elif vix_price < 20:
            hist_level = "정상 범위"
            outlook = "방향성 탐색. 이벤트 따른 변동 가능."
        elif vix_price < 25:
            hist_level = "경계 수준"
            outlook = "변동성 확대 중. 위험 관리 강화."
        else:
            hist_level = "극단적 공포"
            outlook = "패닉 구간. 추가 하락 경계."

        vix_signal = (
            "급락 → 공포 해소. 위험자산 매수 환경" if vix_change < -5 else
            "하락 → 리스크 완화. 주식 롱 우호적" if vix_change < -2 else
            "급등 → 공포 확산. 포지션 축소 및 헤지 강화" if vix_change > 5 else
            "상승 → 불확실성 증가. 신규 진입 보류" if vix_change > 2 else
            "횡보 → 방향 탐색. 이벤트 대기")
        vix_trade = (
            "변동성 매도 유효. 풋 스프레드 고려. 15 돌파 시 전략 재검토" if vix_price < 15 else
            "옵션 헤지 비용 적정. 보호적 풋 매수 타이밍" if vix_price < 20 else
            "헤지 비용 상승. 기존 포지션 방어 우선. 신규 롱 자제" if vix_price < 25 else
            "극단적 공포. 현금 비중 확대. 평균회귀 매매는 하락 확인 후")

        analysis_sections.append(f"""[VIX] {vix_price:.1f} ({vix_change:+.2f}%) - {hist_level}
• 시그널: {vix_signal}
• 전망: {outlook}
• 트레이딩: {vix_trade}""")

    # === 2. MOVE Index ===
    move = quotes.get('MOVE', {})
    move_price = move.get('price', 0)
    move_change = move.get('change_pct', 0)

    if move_price > 0:
        if move_price < 60:
            move_outlook = "채권시장 극도 안정. 캐리 전략 유리."
        elif move_price < 80:
            move_outlook = "정상 변동성. 점진적 금리 조정 환경."
        elif move_price < 100:
            move_outlook = "변동성 확대. 금리 급변 가능성."
        else:
            move_outlook = "극단적 스트레스. 금융시장 전반 위험."

        move_cross = (
            "VIX-MOVE 동반 상승 → 시스템 리스크 경고. 현금 확대"
            if move_price > 80 and quotes.get('VIX', {}).get('price', 0) > 20
            else "MOVE 안정 + VIX 높음 → 주식 변동성 일시적. 채권 안전"
            if move_price < 80 and quotes.get('VIX', {}).get('price', 0) > 20
            else "양 시장 안정적. 위험자산 선호 환경")
        move_trade = (
            "캐리/듀레이션 전략 유효. 금리 급변 리스크 낮음"
            if move_price < 80
            else "금리 트레이드 리스크 확대. 단기물/변동금리 선호")

        analysis_sections.append(f"""[MOVE] {move_price:.1f} ({move_change:+.2f}%) - {'안정' if move_price < 80 else '경계'}
• 채권변동성: {move_outlook}
• VIX 교차분석: {move_cross}
• 트레이딩: {move_trade}""")

    # === 3. S&P 500 ===
    sp500 = quotes.get('SP500', quotes.get('SPY', {}))
    sp_price = sp500.get('price', 0)
    sp_change = sp500.get('change_pct', 0)

    if sp_price > 0:
        support = sp_price * 0.97
        resistance = sp_price * 1.03
        trend = "강세" if sp_change > 0.5 else ("약세" if sp_change < -0.5 else "보합")

        if sp_change > 1:
            sp_outlook = "강세 모멘텀. 추가 상승 여력 있으나 과열 경계."
        elif sp_change > 0:
            sp_outlook = "소폭 상승. 저항선 돌파 시 상승 가속."
        elif sp_change > -1:
            sp_outlook = "소폭 조정. 지지선 확인 후 반등 기대."
        else:
            sp_outlook = "하락 압력. 지지선 이탈 시 하락 가속."

        sp_action = (
            "강한 모멘텀. 저항선 돌파 시 추가 상승. 분할 매수 유효"
            if sp_change > 1 else
            "소폭 상승. 저항선 인근 분할 익절 고려. 돌파 확인 후 추가 롱"
            if sp_change > 0 else
            "소폭 조정. 지지선 테스트 중. 지지 확인 시 매수 기회"
            if sp_change > -1 else
            "하락 압력. 지지선 이탈 시 손절. 현금 비중 확대")

        analysis_sections.append(f"""[S&P 500] {sp_price:,.0f} ({sp_change:+.2f}%) - {trend}
• 기술적: 지지 {support:,.0f} / 저항 {resistance:,.0f} (±3%)
• 전략: {sp_action}
• 모멘텀: {'상승 추세 유지. 조정 시 매수 유효' if sp_change > 0 else '단기 약세. 반등 확인 전 신규 롱 자제'}""")

    # === 4. NASDAQ ===
    nasdaq = quotes.get('NASDAQ', quotes.get('QQQ', {}))
    nq_price = nasdaq.get('price', 0)
    nq_change = nasdaq.get('change_pct', 0)

    if nq_price > 0:
        relative = nq_change - sp_change if sp_price > 0 else 0
        trend = "강세" if nq_change > 0.5 else ("약세" if nq_change < -0.5 else "보합")

        if nq_change > 1:
            nq_outlook = "기술주 강세. AI/반도체 모멘텀 지속."
        elif nq_change < -1:
            nq_outlook = "기술주 약세. 금리 상승 부담 반영."
        else:
            nq_outlook = "중립. 실적에 따른 개별 차별화."

        nq_rotation = (
            "성장주 아웃퍼폼 → 리스크온. AI/반도체 비중 확대 유효"
            if relative > 0.3 else
            "가치주 아웃퍼폼 → 로테이션 진행. 방어주/배당주 비중 확대 고려"
            if relative < -0.3 else
            "시장 동조. 개별 종목 실적에 따른 차별화 예상")

        analysis_sections.append(f"""[NASDAQ] {nq_price:,.0f} ({nq_change:+.2f}%) - 기술주 {trend}
• S&P 대비: {relative:+.2f}%p → {nq_rotation}
• 전망: {nq_outlook}
• 핵심: {'NQ/ES 비율 상승 추세 → 성장주 강세 지속 확인' if relative > 0 else 'NQ 언더퍼폼 시 금리 민감도 재점검. 밸류에이션 부담 경계'}""")

    # === 5. Gold ===
    gold = quotes.get('GOLD', {})
    gold_price = gold.get('price', 0)
    gold_change = gold.get('change_pct', 0)

    if gold_price > 0:
        trend = "상승" if gold_change > 0.5 else ("하락" if gold_change < -0.5 else "횡보")
        if gold_change > 1:
            gold_outlook = "금 상승. 안전자산 수요 또는 인플레이션 헤지."
        elif gold_change < -1:
            gold_outlook = "금 하락. 달러 강세 또는 위험자산 선호."
        else:
            gold_outlook = "금 횡보. 연준 정책 코멘트에 민감."

        eur_chg = quotes.get('EUR_USD', {}).get('change_pct', 0)
        gold_driver = (
            "상승 + 달러 약세 → 인플레 헤지 수요. 추가 상승 여력"
            if gold_change > 0 and eur_chg > 0 else
            "상승 + 달러 강세 → 지정학/안전자산 피난. 달러 전환 시 조정 주의"
            if gold_change > 0 else
            "하락 + 달러 강세 → 실질금리 상승 압력. 하락 지속 가능"
            if gold_change < 0 and eur_chg < 0 else
            "하락 → 위험자산 선호 전환. 금 비중 축소 구간"
            if gold_change < 0 else
            "횡보 → 연준 발언/금리 데이터에 민감. 방향성 대기")

        analysis_sections.append(f"""[Gold] ${gold_price:,.0f} ({gold_change:+.2f}%) - {trend}
• 배경: {gold_driver}
• 레벨: 지지 ${gold_price * 0.97:,.0f} / 저항 ${gold_price * 1.03:,.0f} (±3%)
• 트레이딩: {'실질금리 하락 추세면 금 롱 유지. 신고가 돌파 시 모멘텀 추종' if gold_change > 0 else '실질금리 상승 환경이면 금 숏 또는 비중 축소. 지지선 확인 후 재진입'}""")

    # === 6. EUR/USD ===
    eurusd = quotes.get('EUR_USD', {})
    eur_price = eurusd.get('price', 0)
    eur_change = eurusd.get('change_pct', 0)

    if eur_price > 0:
        dollar = "약세" if eur_change > 0.2 else ("강세" if eur_change < -0.2 else "보합")
        if eur_price > 1.10:
            eur_level = "유로 강세 구간"
        elif eur_price > 1.00:
            eur_level = "중립~약세 구간"
        else:
            eur_level = "패리티 이하"

        eur_strategy = (
            "유로 강세 모멘텀. 달러 약세 트레이드 유효. 1.20 저항 주시"
            if eur_change > 0.5 else
            "유로 약세. 달러 강세 포지션 유지. 지지선 이탈 시 추가 숏"
            if eur_change < -0.5 else
            "횡보. 레인지 내 역추세 매매 또는 브레이크아웃 대기")

        analysis_sections.append(f"""[EUR/USD] {eur_price:.4f} ({eur_change:+.2f}%) - 달러 {dollar}
• 수준: {eur_level}. 미-유 금리차 동향이 핵심 드라이버
• 전략: {eur_strategy}
• 주의: {'1.20 돌파 시 달러 약세 가속. 원자재/신흥국 자산 동반 강세 기대' if eur_price > 1.15 else '패리티 접근 시 달러 강세 피크아웃 가능. 반전 시그널 주시' if eur_price < 1.02 else '레인지 지속 시 옵션 매도(스트래들) 전략 고려'}""")

    # === 7. USD/JPY ===
    usdjpy = quotes.get('USD_JPY', {})
    jpy_price = usdjpy.get('price', 0)
    jpy_change = usdjpy.get('change_pct', 0)

    if jpy_price > 0:
        if jpy_price > 150:
            jpy_level = "엔화 약세 극단 (BOJ 개입 경계)"
        elif jpy_price > 145:
            jpy_level = "엔화 약세 (개입 가능성)"
        else:
            jpy_level = "안정 구간"

        jpy_carry = (
            "155+ 구간. BOJ 구두/실제 개입 리스크 고조. 신규 엔숏 위험"
            if jpy_price > 155 else
            "150-155 구간. 개입 경계. 롱 포지션 스탑 타이트하게 관리"
            if jpy_price > 150 else
            "145-150 구간. 캐리 트레이드 유효. 엔숏 포지션 유지 가능"
            if jpy_price > 145 else
            "145 이하. 엔화 강세 전환 신호. 캐리 트레이드 청산 주의")

        analysis_sections.append(f"""[USD/JPY] {jpy_price:.2f} ({jpy_change:+.2f}%) - {jpy_level}
• 캐리: 미-일 금리차 기반 캐리 {'과열 구간' if jpy_price > 155 else '유효 구간' if jpy_price > 145 else '약화 구간'}
• 리스크: {jpy_carry}
• 핵심: BOJ 정책 변화(금리인상/YCC 조정) 시 5-10엔 급격한 엔화 강세 가능. 이벤트 전 포지션 경량화""")

    # === 8. Bitcoin ===
    btc = quotes.get('BTC', {})
    btc_price = btc.get('price', 0)
    btc_change = btc.get('change_pct', 0)

    if btc_price > 0:
        if btc_change > 5:
            btc_outlook = "강한 상승. 기관 매수 또는 FOMO. 과열 주의."
        elif btc_change > 2:
            btc_outlook = "소폭 상승. 위험자산 선호 지속."
        elif btc_change > -2:
            btc_outlook = "횡보. 방향성 탐색 중."
        elif btc_change > -5:
            btc_outlook = "소폭 하락. 차익실현 또는 위험회피."
        else:
            btc_outlook = "급락. 레버리지 청산 또는 매크로 악재."

        support_btc = btc_price * 0.90
        resistance_btc = btc_price * 1.10

        nq_chg = quotes.get('NASDAQ', quotes.get('QQQ', {})).get('change_pct', 0)
        btc_corr = (
            "나스닥 동반 강세 → 추세 신뢰도 높음. 모멘텀 추종"
            if btc_change > 0 and nq_chg > 0 else
            "나스닥 괴리 → BTC 단독 강세. 지속성 검증 필요"
            if btc_change > 0 and nq_chg <= 0 else
            "나스닥 동반 약세 → 매크로 리스크오프. 추가 하락 경계"
            if btc_change < 0 and nq_chg < 0 else
            "나스닥 강세에 BTC 약세 → 크립토 고유 악재 가능성")

        analysis_sections.append(f"""[Bitcoin] ${btc_price:,.0f} ({btc_change:+.2f}%)
• 기술적: 지지 ${support_btc:,.0f} / 저항 ${resistance_btc:,.0f} (±10%)
• 상관관계: 나스닥 상관 0.6-0.8. {btc_corr}
• 트레이딩: {btc_outlook}""")

    return "\n\n".join(analysis_sections) if analysis_sections else "종목 데이터 없음"

# 캐시할 시스템 프롬프트 (경제 분석 컨텍스트 - 최소 1024 토큰 이상)
SYSTEM_PROMPT = """당신은 전문 경제 애널리스트입니다. 매일 저녁 시장 데이터를 분석하여 투자자를 위한 시황 보고서를 작성합니다.

## 분석 대상 지표

### 1. VIX (CBOE Volatility Index)
- 정의: S&P 500 옵션의 내재변동성을 측정하는 "공포지수"
- 해석 기준:
  - 12 미만: 극단적 낙관 (과열 주의)
  - 12-15: 낮은 변동성 (안정적)
  - 15-20: 보통 수준
  - 20-25: 높은 변동성 (경계)
  - 25 이상: 극단적 공포 (위기 신호)

### 2. MOVE Index (ICE BofAML MOVE)
- 정의: 미국 국채 옵션의 내재변동성 지수 (채권시장 VIX)
- 해석 기준:
  - 60 미만: 매우 낮은 변동성 (채권시장 안정)
  - 60-80: 정상 범위
  - 80-100: 높은 변동성
  - 100-120: 매우 높은 변동성
  - 120 이상: 극단적 스트레스 (2008년, 2020년 수준)

### 3. SOFR (Secured Overnight Financing Rate)
- 정의: 미국 담보부 익일물 금리 (LIBOR 대체)
- 의미: 단기 자금시장 상황 반영
- 연준 기준금리와의 관계: 보통 연방기금금리 범위 내에서 움직임
- 급등 시: 단기 유동성 경색 신호
- 급락 시: 과잉 유동성 또는 안전자산 선호

### 4. 수익률 곡선 (10Y-2Y Spread)
- 정상: 양수 (장기 > 단기)
- 역전: 음수 (경기 침체 선행지표)
- 스티프닝: 스프레드 확대 (경기 회복 기대)
- 플래트닝: 스프레드 축소 (성장 둔화 우려)

### 5. 비트코인 (BTC/USD)
- 위험자산 선호도 지표
- 전통 시장과의 상관관계 증가 추세
- 기관 투자자 참여로 매크로 영향 확대

## 주요 경제 지표 해석

### 연방기금금리 (Federal Funds Rate)
- 연준의 통화정책 핵심 도구
- 인상: 인플레이션 억제, 달러 강세, 주식 하락 압력
- 인하: 경기 부양, 달러 약세, 주식 상승 지지

### CPI/PCE (물가지수)
- 연준 목표: 2%
- 예상 상회: 금리 인상 압력, 주식/채권 하락
- 예상 하회: 금리 인하 기대, 주식/채권 상승

### GDP (국내총생산)
- 분기별 발표 (속보치 → 수정치 → 확정치)
- 예상 상회: 경기 낙관, 주식 상승
- 예상 하회: 경기 우려, 안전자산 선호

### NFP (비농업 고용)
- 매월 첫째 금요일 발표
- 예상 상회: 경기 강세, 금리 인상 압력
- 예상 하회: 경기 우려, 금리 인하 기대

### 실업률
- 연준 목표: 완전고용 (약 4% 수준)
- 상승: 경기 침체 우려
- 하락: 임금 인플레이션 압력

## 보고서 작성 가이드라인

1. **객관성**: 데이터 기반 분석만
2. **간결성**: 핵심만 전달, 군더더기 제거
3. **실용성**: 즉시 활용 가능한 정보
4. **중립성**: 투자 추천 금지
5. **정확성**: 수치/날짜 정확히

## 문체 규칙 (매우 중요)

- "~입니다", "~있습니다", "~됩니다" 사용 금지
- 체언 종결 사용: "유지", "상승", "하락", "주의 필요"
- 예시:
  - ❌ "안정적인 흐름을 유지하고 있습니다"
  - ✅ "안정적 흐름 유지"
  - ❌ "변동성이 확대되고 있습니다"
  - ✅ "변동성 확대"
  - ❌ "주의가 필요합니다"
  - ✅ "주의 필요"

## 출력 형식 (상세)

1. **시장 현황 요약** (5-6문장)
   - 주요 지수 등락률 + 절대값
   - 전일/전주 대비 변화
   - 글로벌 매크로 컨텍스트

2. **변동성 분석** (4-5문장)
   - VIX 수치 + 추세 + 역사적 위치
   - MOVE Index + 채권시장 의미
   - 주식-채권 변동성 괴리 여부

3. **금리 환경** (4-5문장)
   - SOFR 수치 + 주간 변화
   - 연준 기준금리와 관계
   - 수익률 곡선 (10Y-2Y) 상태
   - 단기 자금시장 신호

4. **섹터별 동향** (6-8문장)
   - 주식: S&P 500, 나스닥, 다우
   - 채권: 10년물, 2년물
   - 원자재: 금, 원유
   - 암호화폐: BTC 동향 + 위험선호 지표
   - 각 섹터별 등락 수치 필수

5. **핵심 경제지표 해석** (4-5문장)
   - 최근 발표 지표 분석
   - 예상치 대비 결과
   - 시장 영향 평가

6. **내일 전망 및 주의사항** (5-6문장)
   - 예정 이벤트 상세 (시간, 중요도)
   - 시나리오별 영향 분석
   - 변동성 예상
   - 주의해야 할 레벨/지지저항

## 주의사항

- 모든 섹션에 실제 수치 필수 기재
- 변화율은 % 단위로 소수점 2자리까지
- 추측 표현 최소화
- 매수/매도 추천 금지
- 미확인 정보 제외
"""


def _inject_asset_analysis(text: str, analysis: str) -> str:
    """종목별 상세 분석 섹션을 rule-based 분석으로 교체"""
    import re
    pattern = r'## 종목별 상세 분석.*?(?=\n## |\Z)'
    replacement = f'## 종목별 상세 분석\n\n{analysis}'
    result = re.sub(pattern, replacement, text, flags=re.DOTALL)
    if '## 종목별 상세 분석' not in result:
        if '## 내일 전망' in result:
            result = result.replace(
                '## 내일 전망',
                f'## 종목별 상세 분석\n\n{analysis}\n\n## 내일 전망')
        else:
            result += f'\n\n## 종목별 상세 분석\n\n{analysis}'
    return result


def generate_market_outlook(report_data: Dict) -> Dict:
    """
    Ollama (Qwen2.5-7B)를 사용하여 경제 시황 생성

    Args:
        report_data: 시세, 지표 등 보고서 데이터

    Returns:
        시황 및 전망 딕셔너리
    """
    import requests
    import time

    # rule-based 분석이 7B 모델보다 일관적이고 빠름 → 기본값으로 사용
    # Ollama는 USE_OLLAMA=1 환경변수 설정 시에만 사용
    if not os.environ.get('USE_OLLAMA'):
        print("[모드] rule-based (즉시 생성)")
        return generate_default_outlook(report_data)

    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL = "qwen2.5:7b"

    # Ollama 서버 연결 체크
    try:
        health_check = requests.get("http://localhost:11434/api/tags", timeout=5)
        if health_check.status_code != 200:
            print("[경고] Ollama 서버 응답 없음 - 기본 시황 사용")
            return generate_default_outlook(report_data)
    except requests.exceptions.RequestException:
        print("[경고] Ollama 서버 연결 실패 - 기본 시황 사용")
        return generate_default_outlook(report_data)

    try:
        # 데이터 요약 (매일 변하는 부분)
        indicators_summary = "\n".join([
            f"- {i['name']}: {i['value']:.2f}% ({i['date']})"
            for i in report_data.get('economic_indicators', [])
        ])

        tomorrow_events = "\n".join([
            f"- {e['time']}: {e['name']} ({e['importance']})"
            for e in report_data.get('tomorrow_events', [])
        ])

        # 전일 대비 변화 계산
        quotes_detail = []
        for q in report_data.get('quotes', []):
            price = q.get('price', 0)
            change = q.get('change_pct', 0)
            prev_close = price / (1 + change/100) if change != 0 else price
            quotes_detail.append(
                f"- {q['name']} ({q['symbol']}): {price:,.2f} (전일비 {change:+.2f}%, 전일종가 {prev_close:,.2f})"
            )
        quotes_detail_str = "\n".join(quotes_detail)

        # 시스템 프롬프트 + 유저 프롬프트 결합
        system_instruction = """당신은 전문 경제 애널리스트입니다. 매일 저녁 시장 데이터를 분석하여 투자자를 위한 시황 보고서를 작성합니다.

""" + SYSTEM_PROMPT

        user_prompt = f"""오늘 날짜: {report_data.get('date', datetime.now().strftime('%Y-%m-%d'))}

## 현재 시세 (상세)
{quotes_detail_str}

## 변동성 지표
- VIX (공포지수): {report_data.get('quotes', [{}])[0].get('price', 0) if report_data.get('quotes') and report_data['quotes'][0].get('symbol') == 'VIX' else 'N/A'}
- MOVE Index (채권 변동성): {report_data.get('move_current', 0):.1f}
  - 분석: {report_data.get('move_analysis', '')}

## 금리 환경
- SOFR (담보부 익일물 금리): {report_data.get('sofr_current', 0):.2f}%
  - 주간 변화: {report_data.get('sofr_analysis', '')}
- 연준 기준금리 범위: 4.25% - 4.50% (참고)

## 주요 경제 지표 (최근 발표)
{indicators_summary if indicators_summary else "- 오늘 발표된 주요 지표 없음"}

## 내일 예정 이벤트
{tomorrow_events if tomorrow_events else "- 내일 예정된 주요 이벤트 없음"}

위 데이터를 바탕으로 시장 시황 보고서를 한국어로 작성하세요.

[필수 형식 - 위반 시 무효]
- 100% 한국어로만 작성. 중국어(简体/繁體) 절대 금지. 영어는 종목명/수치만 허용
- ## 헤더만 사용 (### 사용 금지)
- 간결체 필수 (종결어미 "-다", "-했다", "-입니다" 금지)

[문체 변환 예시 - 반드시 따를 것]
❌ "S&P 500은 +0.12% 상승했다" → ✅ "S&P 500: +0.12% 상승"
❌ "VIX가 17.72로 상승하였다" → ✅ "VIX 17.72 (+1.61%) - 소폭 상승"
❌ "시장은 안정적인 흐름을 보이고 있다" → ✅ "시장 안정적 흐름 유지"
❌ "내일 발표될 예정이다" → ✅ "내일 발표 예정"
❌ "주의가 필요합니다" → ✅ "주의 필요"

[필수 섹션 5개 - 순서대로 작성]
## 시장 현황 요약
## 변동성 분석
## 금리 환경
## 섹터별 동향
## 내일 전망

⚠️ "종목별 상세 분석" 섹션은 자동 생성되므로 작성하지 마세요.

[내용 요구 - 상세하게 작성]
- 모든 섹션에 실제 수치 포함

[변동성 분석] 각 지표별:
• 현재 수치 + 전일비
• 수준 평가 (예: "정상 범위", "경계 수준")
• 의미 해석 1줄

[섹터별 동향] 주식/채권/원자재/암호화폐 각각:
• 현재 상황 + 방향성
• 주요 이슈나 특이점 1줄

[내일 전망]
• 예정 이벤트 목록
• 시나리오별 전망 (긍정/부정/중립)
• 주의해야 할 가격 레벨"""

        full_prompt = f"{system_instruction}\n\n---\n\n{user_prompt}"

        start_time = time.time()
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "num_predict": 2500,
                    "temperature": 0.7
                }
            },
            timeout=120
        )

        if response.status_code != 200:
            print(f"[에러] Ollama API 오류: {response.status_code}")
            return generate_default_outlook(report_data)

        result = response.json()
        outlook_text = result.get('response', '')
        elapsed = time.time() - start_time

        # 로깅
        eval_count = result.get('eval_count', 0)
        print(f"[API] Ollama ({MODEL})")
        print(f"      생성: {eval_count} tokens, 소요: {elapsed:.1f}초")
        print(f"      비용: $0.00 (로컬 모델)")

        # 종목별 상세 분석: rule-based로 대체 (일관된 품질 보장)
        quotes_dict = {q['symbol']: q for q in report_data.get('quotes', [])}
        asset_detail = generate_asset_analysis(
            quotes_dict, report_data.get('economic_indicators', []))
        outlook_text = _inject_asset_analysis(outlook_text, asset_detail)

        return {
            'generated': True,
            'model': f'ollama-{MODEL}',
            'text': outlook_text,
            'tokens': {
                'input': result.get('prompt_eval_count', 0),
                'output': eval_count,
                'cache_creation': 0,
                'cache_read': 0
            },
            'cost': 0.0,
            'cache_status': 'LOCAL',
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        print(f"[에러] Ollama 호출 실패: {e}")
        import traceback
        traceback.print_exc()
        return generate_default_outlook(report_data)


def generate_default_outlook(report_data: Dict) -> Dict:
    """API 없이 상세 시황 생성 (데이터 기반 - 확장 버전)"""

    quotes = {q['symbol']: q for q in report_data.get('quotes', [])}
    date = report_data.get('date', datetime.now().strftime('%Y-%m-%d'))

    # === 1. 시장 현황 요약 ===
    # VIX 분석
    vix_data = quotes.get('VIX', {})
    vix = vix_data.get('price', 0)
    vix_change = vix_data.get('change_pct', 0)

    if vix < 12:
        vix_level = "극단적 낙관 (과열 주의)"
        vix_risk = "높음"
    elif vix < 15:
        vix_level = "낮은 변동성 (안정적)"
        vix_risk = "낮음"
    elif vix < 20:
        vix_level = "보통 수준"
        vix_risk = "보통"
    elif vix < 25:
        vix_level = "높은 변동성 (경계)"
        vix_risk = "경계"
    else:
        vix_level = "극단적 공포 (위기 신호)"
        vix_risk = "매우 높음"

    # MOVE Index 분석
    move = report_data.get('move_current', 0)
    move_analysis = report_data.get('move_analysis', '')

    if move < 60:
        move_level = "매우 낮은 변동성 (채권시장 안정)"
    elif move < 80:
        move_level = "정상 범위"
    elif move < 100:
        move_level = "높은 변동성"
    elif move < 120:
        move_level = "매우 높은 변동성"
    else:
        move_level = "극단적 스트레스 (위기 수준)"

    # === 2. 섹터별 분석 ===
    # 주식 지수 (SP500/NASDAQ 또는 SPY/QQQ)
    spy = quotes.get('SP500', quotes.get('SPY', {}))
    qqq = quotes.get('NASDAQ', quotes.get('QQQ', {}))
    spy_price = spy.get('price', 0)
    spy_change = spy.get('change_pct', 0)
    qqq_price = qqq.get('price', 0)
    qqq_change = qqq.get('change_pct', 0)

    if spy_change > 1:
        stock_trend = "강세"
    elif spy_change < -1:
        stock_trend = "약세"
    else:
        stock_trend = "보합"

    # 채권
    tlt = quotes.get('TLT', {})
    tlt_price = tlt.get('price', 0)
    tlt_change = tlt.get('change_pct', 0)

    if tlt_change > 0.5:
        bond_trend = "상승 (금리 하락)"
    elif tlt_change < -0.5:
        bond_trend = "하락 (금리 상승)"
    else:
        bond_trend = "보합"

    # 원자재
    gold = quotes.get('GOLD', {})
    oil = quotes.get('OIL', {})
    gold_price = gold.get('price', 0)
    gold_change = gold.get('change_pct', 0)
    oil_price = oil.get('price', 0)
    oil_change = oil.get('change_pct', 0)

    # 암호화폐
    btc = quotes.get('BTC', {})
    btc_price = btc.get('price', 0)
    btc_change = btc.get('change_pct', 0)

    if btc_change > 5:
        btc_trend = "강세 (위험선호 확대)"
    elif btc_change > 2:
        btc_trend = "소폭 상승"
    elif btc_change < -5:
        btc_trend = "급락 (위험회피 신호)"
    elif btc_change < -2:
        btc_trend = "소폭 하락"
    else:
        btc_trend = "횡보"

    # === 3. 금리 환경 ===
    sofr = report_data.get('sofr_current', 0)
    sofr_analysis = report_data.get('sofr_analysis', '')

    # === 4. 경제 지표 ===
    indicators = report_data.get('economic_indicators', [])
    indicators_text = ""
    if indicators:
        for ind in indicators[:5]:
            indicators_text += f"- {ind['name']}: {ind['value']:.2f}% ({ind['date']})\n"
    else:
        indicators_text = "- 오늘 발표된 주요 지표 없음\n"

    # === 5. 내일 이벤트 ===
    tomorrow = report_data.get('tomorrow_events', [])
    critical_events = [e for e in tomorrow if e.get('importance') == 'critical']
    high_events = [e for e in tomorrow if e.get('importance') == 'high']

    tomorrow_text = ""
    if critical_events:
        tomorrow_text += f"⚠️ 중요 이벤트 {len(critical_events)}개:\n"
        for e in critical_events:
            tomorrow_text += f"  - {e['time']}: {e['name']}\n"
    if high_events:
        tomorrow_text += f"📌 주요 이벤트 {len(high_events)}개:\n"
        for e in high_events[:3]:
            tomorrow_text += f"  - {e['time']}: {e['name']}\n"
    if not critical_events and not high_events:
        tomorrow_text = "- 내일 예정된 주요 이벤트 없음"

    # === 보고서 생성 ===
    text = f"""## 시장 현황 요약 ({date})

{date} 기준, 미국 주식시장은 {stock_trend} 흐름. S&P 500은 {spy_price:,.0f}로 전일비 {spy_change:+.2f}% 변동. NASDAQ은 {qqq_price:,.0f}로 {qqq_change:+.2f}% 기록. VIX {vix:.1f}로 {vix_level} 평가.

## 변동성 분석

[VIX - 주식 변동성]
• 현재: {vix:.1f} (전일비 {vix_change:+.2f}%)
• 수준: {vix_level} | 위험도: {vix_risk}
• 해석: VIX {vix:.1f}은 {'20 이하로 안정적 환경 지속' if vix < 20 else '변동성 확대 구간'}

[MOVE - 채권 변동성]
• 현재: {move:.1f}
• 수준: {move_level}
• 주간: {move_analysis}
• 해석: {'MOVE 80 미만으로 금리 급변 리스크 낮음' if move < 80 else 'MOVE 상승으로 금리 변동성 확대'}

## 금리 환경

[SOFR]
• 현재: {sofr:.2f}%
• 동향: {sofr_analysis}
• 연준 기준금리: 4.25% - 4.50%
• 해석: {'기준금리 범위 내 정상' if 4.25 <= sofr <= 4.60 else '기준금리 대비 이탈 - 유동성 변화 주시'}

## 섹터별 동향

[주식]
• S&P 500: {spy_price:,.0f} ({spy_change:+.2f}%)
• NASDAQ: {qqq_price:,.0f} ({qqq_change:+.2f}%)
• 방향: {stock_trend} | {'기술주가 S&P 대비 강세' if qqq_change > spy_change else '기술주가 S&P 대비 약세'}

[원자재/통화]
• Gold: ${gold_price:,.0f} ({gold_change:+.2f}%) - {'안전자산 수요' if gold_change > 0 else '위험자산 선호'}
• EUR/USD: {quotes.get('EUR_USD', {}).get('price', 0):.4f} - 달러 {'약세' if quotes.get('EUR_USD', {}).get('change_pct', 0) > 0 else '강세'}
• USD/JPY: {quotes.get('USD_JPY', {}).get('price', 0):.2f} {'(BOJ 개입 경계)' if quotes.get('USD_JPY', {}).get('price', 0) > 150 else ''}

[암호화폐]
• Bitcoin: ${btc_price:,.0f} ({btc_change:+.2f}%)
• 해석: {btc_trend}

## 종목별 상세 분석

{generate_asset_analysis(quotes, report_data.get('economic_indicators', []))}

## 핵심 경제지표

{indicators_text}

## 내일 전망

{tomorrow_text}

[시나리오]
• 긍정: VIX 15 이하 유지 → 안정적 상승 지속
• 부정: VIX 25 돌파 → 급락 가능성, 현금 비중 확대
• 중립: 현 수준 유지 → 박스권 등락

[S&P 500 지지/저항]
• 지지선: {spy_price * 0.98:,.0f} (-2%)
• 저항선: {spy_price * 1.02:,.0f} (+2%)

---
자동 생성 보고서 (rule-based) | 투자 조언 아님"""

    return {
        'generated': False,
        'model': 'rule-based-v2',
        'text': text,
        'tokens': {'input': 0, 'output': 0, 'cache_creation': 0, 'cache_read': 0},
        'cost': 0,
        'cache_status': 'N/A',
        'timestamp': datetime.now().isoformat()
    }


def save_outlook(outlook: Dict, date: str = None):
    """시황 저장"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    outlook_file = REPORTS_DIR / f"outlook_{date}.json"
    with open(outlook_file, 'w', encoding='utf-8') as f:
        json.dump(outlook, f, ensure_ascii=False, indent=2)

    print(f"[저장] 시황: {outlook_file}")
    return str(outlook_file)


def load_outlook(date: str = None) -> Optional[Dict]:
    """시황 로드"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    outlook_file = REPORTS_DIR / f"outlook_{date}.json"
    if outlook_file.exists():
        with open(outlook_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


# CLI
if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path.home() / ".claude" / "modules" / "trading"))

    from reports.export_report import load_report_json

    date = sys.argv[1] if len(sys.argv) > 1 else None
    report = load_report_json(date)

    if report:
        outlook = generate_market_outlook(report)
        print("\n" + "="*50)
        print(outlook['text'])
        print("="*50)
        print(f"\n모델: {outlook['model']}")
        print(f"캐시: {outlook.get('cache_status', 'N/A')}")
        print(f"비용: ${outlook['cost']:.4f}")
        save_outlook(outlook, report.get('date'))
    else:
        print("보고서 데이터 없음")
