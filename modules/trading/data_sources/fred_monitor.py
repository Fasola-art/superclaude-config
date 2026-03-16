#!/usr/bin/env python3
"""
FRED (Federal Reserve Economic Data) 경제 지표 모니터링
- 주요 경제 지표 실시간 추적
- 지표 변화 알림
- 과거 데이터 분석
- 예측 모델링 지원

API 문서: https://fred.stlouisfed.org/docs/api/fred/
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import Enum

# 설정
FRED_API_BASE = "https://api.stlouisfed.org/fred"
CONFIG_DIR = Path.home() / ".claude" / "modules" / "trading" / "data_sources"
CREDENTIALS_FILE = Path.home() / ".claude" / "credentials" / "api-keys.json"
ARCHIVE_DIR = Path.home() / ".claude" / "modules" / "trading" / "data_sources" / "fred_data"


class IndicatorCategory(Enum):
    """경제 지표 카테고리"""
    INFLATION = "inflation"          # 인플레이션
    EMPLOYMENT = "employment"        # 고용
    GDP = "gdp"                      # GDP
    INTEREST_RATE = "interest_rate"  # 금리
    MONEY_SUPPLY = "money_supply"    # 통화량
    HOUSING = "housing"              # 주택
    CONSUMER = "consumer"            # 소비자
    MANUFACTURING = "manufacturing"  # 제조업
    TRADE = "trade"                  # 무역


@dataclass
class EconomicIndicator:
    """경제 지표 정의"""
    series_id: str
    name: str
    category: IndicatorCategory
    frequency: str  # D, W, M, Q, A
    units: str
    importance: str  # critical, high, medium, low
    description: str = ""


@dataclass
class IndicatorData:
    """지표 데이터 포인트"""
    series_id: str
    date: str
    value: float
    previous_value: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None


@dataclass
class IndicatorAlert:
    """지표 알림"""
    series_id: str
    name: str
    alert_type: str  # new_release, significant_change, threshold_breach
    message: str
    current_value: float
    previous_value: Optional[float]
    timestamp: datetime = field(default_factory=datetime.now)


# 주요 경제 지표 목록
MONITORED_INDICATORS = [
    # 인플레이션
    EconomicIndicator("CPIAUCSL", "CPI (소비자물가지수)", IndicatorCategory.INFLATION, "M", "Index", "critical", "소비자 물가 변동"),
    EconomicIndicator("PCEPI", "PCE 물가지수", IndicatorCategory.INFLATION, "M", "Index", "critical", "연준 선호 인플레이션 지표"),
    EconomicIndicator("CPILFESL", "Core CPI (식품/에너지 제외)", IndicatorCategory.INFLATION, "M", "Index", "high"),
    EconomicIndicator("T10YIE", "10년 기대 인플레이션", IndicatorCategory.INFLATION, "D", "Percent", "high"),

    # 고용
    EconomicIndicator("UNRATE", "실업률", IndicatorCategory.EMPLOYMENT, "M", "Percent", "critical"),
    EconomicIndicator("PAYEMS", "비농업 고용", IndicatorCategory.EMPLOYMENT, "M", "Thousands", "critical"),
    EconomicIndicator("ICSA", "신규 실업수당 청구", IndicatorCategory.EMPLOYMENT, "W", "Number", "high"),
    EconomicIndicator("JTSJOL", "구인건수 (JOLTS)", IndicatorCategory.EMPLOYMENT, "M", "Thousands", "high"),

    # GDP
    EconomicIndicator("GDP", "GDP", IndicatorCategory.GDP, "Q", "Billions", "critical"),
    EconomicIndicator("GDPC1", "실질 GDP", IndicatorCategory.GDP, "Q", "Billions", "critical"),
    EconomicIndicator("A191RL1Q225SBEA", "GDP 성장률", IndicatorCategory.GDP, "Q", "Percent", "critical"),

    # 금리
    EconomicIndicator("FEDFUNDS", "연방기금금리", IndicatorCategory.INTEREST_RATE, "D", "Percent", "critical"),
    EconomicIndicator("DGS10", "10년 국채 수익률", IndicatorCategory.INTEREST_RATE, "D", "Percent", "critical"),
    EconomicIndicator("DGS2", "2년 국채 수익률", IndicatorCategory.INTEREST_RATE, "D", "Percent", "high"),
    EconomicIndicator("T10Y2Y", "10Y-2Y 스프레드 (역전 지표)", IndicatorCategory.INTEREST_RATE, "D", "Percent", "critical"),
    EconomicIndicator("MORTGAGE30US", "30년 모기지 금리", IndicatorCategory.INTEREST_RATE, "W", "Percent", "high"),

    # 통화량
    EconomicIndicator("M2SL", "M2 통화량", IndicatorCategory.MONEY_SUPPLY, "M", "Billions", "high"),
    EconomicIndicator("WALCL", "연준 총자산", IndicatorCategory.MONEY_SUPPLY, "W", "Millions", "high"),

    # 소비자
    EconomicIndicator("UMCSENT", "미시간 소비자심리지수", IndicatorCategory.CONSUMER, "M", "Index", "high"),
    EconomicIndicator("PCE", "개인소비지출", IndicatorCategory.CONSUMER, "M", "Billions", "high"),
    EconomicIndicator("RSXFS", "소매판매 (자동차 제외)", IndicatorCategory.CONSUMER, "M", "Millions", "medium"),

    # 제조업
    EconomicIndicator("INDPRO", "산업생산지수", IndicatorCategory.MANUFACTURING, "M", "Index", "medium"),
    EconomicIndicator("DGORDER", "내구재 주문", IndicatorCategory.MANUFACTURING, "M", "Millions", "medium"),

    # 주택
    EconomicIndicator("HOUST", "주택착공건수", IndicatorCategory.HOUSING, "M", "Thousands", "medium"),
    EconomicIndicator("CSUSHPINSA", "케이스-쉴러 주택가격지수", IndicatorCategory.HOUSING, "M", "Index", "medium"),
]


class FREDMonitor:
    """FRED 경제 지표 모니터"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or self._load_api_key()
        self.indicators = {ind.series_id: ind for ind in MONITORED_INDICATORS}
        self.cache = {}  # 간단한 메모리 캐시
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    def _load_api_key(self) -> str:
        """API 키 로드"""
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                creds = json.load(f)
                keys = creds.get('fred', {}).get('keys', [])
                if keys:
                    return keys[0]['key']
        except Exception as e:
            print(f"[경고] API 키 로드 실패: {e}")
        return ""

    def _api_request(self, endpoint: str, params: Dict[str, str]) -> Dict:
        """FRED API 요청"""
        params['api_key'] = self.api_key
        params['file_type'] = 'json'

        query = urllib.parse.urlencode(params)
        url = f"{FRED_API_BASE}/{endpoint}?{query}"

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"[에러] API 요청 실패: {endpoint} - {e}")
            return {}

    def get_series_data(self, series_id: str,
                       start_date: str = None,
                       end_date: str = None,
                       limit: int = 100) -> List[IndicatorData]:
        """
        시계열 데이터 조회

        Args:
            series_id: FRED 시리즈 ID
            start_date: 시작일 (YYYY-MM-DD)
            end_date: 종료일 (YYYY-MM-DD)
            limit: 최대 데이터 포인트 수
        """
        params = {
            'series_id': series_id,
            'sort_order': 'desc',
            'limit': str(limit)
        }

        if start_date:
            params['observation_start'] = start_date
        if end_date:
            params['observation_end'] = end_date

        result = self._api_request('series/observations', params)
        observations = result.get('observations', [])

        data_points = []
        prev_value = None

        for obs in reversed(observations):  # 오래된 것부터 처리
            try:
                value = float(obs['value']) if obs['value'] != '.' else None
                if value is None:
                    continue

                change = (value - prev_value) if prev_value else None
                change_pct = ((value - prev_value) / prev_value * 100) if prev_value else None

                data_points.append(IndicatorData(
                    series_id=series_id,
                    date=obs['date'],
                    value=value,
                    previous_value=prev_value,
                    change=change,
                    change_percent=change_pct
                ))

                prev_value = value
            except (ValueError, KeyError):
                continue

        return data_points

    def get_latest_value(self, series_id: str) -> Optional[IndicatorData]:
        """최신 값 조회"""
        data = self.get_series_data(series_id, limit=2)
        return data[-1] if data else None

    def get_category_summary(self, category: IndicatorCategory) -> Dict[str, Any]:
        """카테고리별 요약"""
        summary = {
            'category': category.value,
            'indicators': [],
            'updated_at': datetime.now().isoformat()
        }

        for indicator in MONITORED_INDICATORS:
            if indicator.category == category:
                latest = self.get_latest_value(indicator.series_id)
                if latest:
                    summary['indicators'].append({
                        'series_id': indicator.series_id,
                        'name': indicator.name,
                        'value': latest.value,
                        'date': latest.date,
                        'change': latest.change,
                        'change_percent': latest.change_percent,
                        'importance': indicator.importance
                    })

        return summary

    def get_all_critical_indicators(self) -> List[Dict[str, Any]]:
        """모든 중요 지표 조회"""
        critical = []

        for indicator in MONITORED_INDICATORS:
            if indicator.importance == 'critical':
                latest = self.get_latest_value(indicator.series_id)
                if latest:
                    critical.append({
                        'series_id': indicator.series_id,
                        'name': indicator.name,
                        'category': indicator.category.value,
                        'value': latest.value,
                        'date': latest.date,
                        'change_percent': latest.change_percent,
                        'units': indicator.units
                    })

        return critical

    def check_for_alerts(self, threshold_pct: float = 5.0) -> List[IndicatorAlert]:
        """
        알림 조건 체크

        Args:
            threshold_pct: 변화율 임계치 (%)
        """
        alerts = []

        for indicator in MONITORED_INDICATORS:
            if indicator.importance not in ['critical', 'high']:
                continue

            latest = self.get_latest_value(indicator.series_id)
            if not latest or latest.change_percent is None:
                continue

            # 큰 변화 감지
            if abs(latest.change_percent) >= threshold_pct:
                direction = "상승" if latest.change_percent > 0 else "하락"
                alerts.append(IndicatorAlert(
                    series_id=indicator.series_id,
                    name=indicator.name,
                    alert_type='significant_change',
                    message=f"{indicator.name} {abs(latest.change_percent):.2f}% {direction}",
                    current_value=latest.value,
                    previous_value=latest.previous_value
                ))

            # 특수 조건 체크
            if indicator.series_id == 'T10Y2Y' and latest.value < 0:
                alerts.append(IndicatorAlert(
                    series_id=indicator.series_id,
                    name=indicator.name,
                    alert_type='threshold_breach',
                    message=f"⚠️ 수익률 곡선 역전: {latest.value:.2f}%",
                    current_value=latest.value,
                    previous_value=latest.previous_value
                ))

        return alerts

    def get_yield_curve(self) -> Dict[str, float]:
        """수익률 곡선 데이터"""
        maturities = [
            ('DGS1MO', '1M'),
            ('DGS3MO', '3M'),
            ('DGS6MO', '6M'),
            ('DGS1', '1Y'),
            ('DGS2', '2Y'),
            ('DGS5', '5Y'),
            ('DGS10', '10Y'),
            ('DGS30', '30Y')
        ]

        curve = {}
        for series_id, label in maturities:
            latest = self.get_latest_value(series_id)
            if latest:
                curve[label] = latest.value

        return curve

    def get_inflation_dashboard(self) -> Dict[str, Any]:
        """인플레이션 대시보드"""
        dashboard = {
            'generated_at': datetime.now().isoformat(),
            'headline_cpi': None,
            'core_cpi': None,
            'pce': None,
            'expected_inflation': None,
            'trend': None
        }

        # CPI
        cpi_data = self.get_series_data('CPIAUCSL', limit=13)  # 1년치
        if cpi_data:
            latest = cpi_data[-1]
            year_ago = cpi_data[0] if len(cpi_data) >= 12 else None

            dashboard['headline_cpi'] = {
                'value': latest.value,
                'date': latest.date,
                'mom_change': latest.change_percent,
                'yoy_change': ((latest.value - year_ago.value) / year_ago.value * 100) if year_ago else None
            }

        # Core CPI
        core = self.get_latest_value('CPILFESL')
        if core:
            dashboard['core_cpi'] = {
                'value': core.value,
                'date': core.date
            }

        # PCE
        pce = self.get_latest_value('PCEPI')
        if pce:
            dashboard['pce'] = {
                'value': pce.value,
                'date': pce.date
            }

        # 기대 인플레이션
        expected = self.get_latest_value('T10YIE')
        if expected:
            dashboard['expected_inflation'] = {
                'value': expected.value,
                'date': expected.date
            }

        return dashboard

    def save_snapshot(self, categories: List[IndicatorCategory] = None):
        """지표 스냅샷 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if categories is None:
            categories = list(IndicatorCategory)

        snapshot = {
            'timestamp': timestamp,
            'categories': {}
        }

        for category in categories:
            snapshot['categories'][category.value] = self.get_category_summary(category)

        filename = ARCHIVE_DIR / f"snapshot_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        print(f"[저장] {filename}")
        return filename


# 사용 예시
if __name__ == "__main__":
    monitor = FREDMonitor()

    print("=== 주요 경제 지표 ===")
    critical = monitor.get_all_critical_indicators()
    for ind in critical:
        change = f"({ind['change_percent']:+.2f}%)" if ind['change_percent'] else ""
        print(f"  {ind['name']}: {ind['value']:.2f} {ind['units']} {change}")

    print("\n=== 수익률 곡선 ===")
    curve = monitor.get_yield_curve()
    for maturity, rate in curve.items():
        print(f"  {maturity}: {rate:.2f}%")

    print("\n=== 인플레이션 대시보드 ===")
    inflation = monitor.get_inflation_dashboard()
    if inflation['headline_cpi']:
        print(f"  CPI: {inflation['headline_cpi']['value']:.2f} (YoY: {inflation['headline_cpi'].get('yoy_change', 'N/A')}%)")
    if inflation['expected_inflation']:
        print(f"  기대 인플레이션: {inflation['expected_inflation']['value']:.2f}%")

    print("\n=== 알림 체크 ===")
    alerts = monitor.check_for_alerts(threshold_pct=3.0)
    for alert in alerts:
        print(f"  🚨 {alert.message}")
