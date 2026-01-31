#!/usr/bin/env python3
"""
COT (Commitment of Traders) 보고서 수집 및 분석
- CFTC 데이터 자동 수집
- 포지션 분석
- 트렌드 추적
- 주간 자동 업데이트

발표 일정: 매주 금요일 3:30 PM ET (화요일 기준 데이터)
데이터 소스: https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
"""

import json
import csv
import io
import zipfile
import urllib.request
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import Enum

# 설정
CFTC_BASE_URL = "https://www.cftc.gov/dea/newcot"
ARCHIVE_DIR = Path.home() / ".claude" / "modules" / "trading" / "data_sources" / "cot_data"
CONFIG_DIR = Path.home() / ".claude" / "modules" / "trading" / "data_sources"


class ReportType(Enum):
    """COT 보고서 유형"""
    LEGACY = "legacy"           # 레거시 보고서 (Commercials, Non-Commercials, Small Specs)
    DISAGGREGATED = "disagg"    # 세분화 보고서 (Producer, Swap Dealer, Managed Money, Other)
    TFF = "tff"                 # Traders in Financial Futures


class PositionType(Enum):
    """포지션 유형"""
    COMMERCIAL = "commercial"
    NON_COMMERCIAL = "non_commercial"
    SMALL_SPECULATORS = "small_spec"
    MANAGED_MONEY = "managed_money"
    SWAP_DEALERS = "swap_dealers"


@dataclass
class COTPosition:
    """COT 포지션 데이터"""
    report_date: str
    market_name: str
    contract_code: str
    exchange: str

    # 상업적 거래자 (헤저)
    commercial_long: int = 0
    commercial_short: int = 0
    commercial_net: int = 0

    # 비상업적 거래자 (투기자)
    non_commercial_long: int = 0
    non_commercial_short: int = 0
    non_commercial_net: int = 0
    non_commercial_spreading: int = 0

    # 소규모 투기자
    small_spec_long: int = 0
    small_spec_short: int = 0
    small_spec_net: int = 0

    # 총 미결제약정
    open_interest: int = 0
    open_interest_change: int = 0

    # 계산된 지표
    commercial_pct: float = 0.0      # 상업적 포지션 비율
    non_commercial_pct: float = 0.0  # 비상업적 포지션 비율


@dataclass
class COTAnalysis:
    """COT 분석 결과"""
    market_name: str
    contract_code: str
    report_date: str

    # 현재 상태
    net_position_commercials: int
    net_position_speculators: int

    # 변화
    weekly_change_commercials: int
    weekly_change_speculators: int

    # 극단값 분석 (52주 기준)
    commercials_percentile: float  # 0-100, 상업적 순포지션의 52주 백분위
    speculators_percentile: float

    # 시그널
    signal: str  # bullish, bearish, neutral
    signal_strength: str  # strong, moderate, weak
    commentary: str


# 주요 추적 시장
TRACKED_MARKETS = {
    # 에너지
    'CL': {'name': '원유 (WTI)', 'exchange': 'NYMEX', 'category': 'energy'},
    'NG': {'name': '천연가스', 'exchange': 'NYMEX', 'category': 'energy'},

    # 금속
    'GC': {'name': '금', 'exchange': 'COMEX', 'category': 'metals'},
    'SI': {'name': '은', 'exchange': 'COMEX', 'category': 'metals'},
    'HG': {'name': '구리', 'exchange': 'COMEX', 'category': 'metals'},

    # 농산물
    'ZC': {'name': '옥수수', 'exchange': 'CBOT', 'category': 'agriculture'},
    'ZS': {'name': '대두', 'exchange': 'CBOT', 'category': 'agriculture'},
    'ZW': {'name': '밀', 'exchange': 'CBOT', 'category': 'agriculture'},

    # 통화
    'EC': {'name': '유로 (EUR/USD)', 'exchange': 'CME', 'category': 'currencies'},
    'JY': {'name': '엔 (USD/JPY)', 'exchange': 'CME', 'category': 'currencies'},
    'BP': {'name': '파운드 (GBP/USD)', 'exchange': 'CME', 'category': 'currencies'},

    # 주가지수
    'ES': {'name': 'E-mini S&P 500', 'exchange': 'CME', 'category': 'indices'},
    'NQ': {'name': 'E-mini Nasdaq', 'exchange': 'CME', 'category': 'indices'},

    # 금리
    'ZN': {'name': '10년 국채', 'exchange': 'CBOT', 'category': 'rates'},
    'ZB': {'name': '30년 국채', 'exchange': 'CBOT', 'category': 'rates'},

    # 암호화폐
    'BTC': {'name': '비트코인', 'exchange': 'CME', 'category': 'crypto'},
}


class COTCollector:
    """COT 보고서 수집기"""

    def __init__(self):
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
        self.historical_data: Dict[str, List[COTPosition]] = {}

    def download_latest_report(self, report_type: ReportType = ReportType.LEGACY) -> str:
        """
        최신 COT 보고서 다운로드

        Returns:
            다운로드된 파일 경로
        """
        # CFTC 보고서 URL 패턴
        year = datetime.now().year
        urls = {
            ReportType.LEGACY: f"{CFTC_BASE_URL}/{year}/deacot{year}.zip",
            ReportType.DISAGGREGATED: f"{CFTC_BASE_URL}/{year}/f_disagg{year}.zip",
            ReportType.TFF: f"{CFTC_BASE_URL}/{year}/fut_fin_txt_{year}.zip"
        }

        url = urls.get(report_type, urls[ReportType.LEGACY])

        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                zip_data = response.read()

            # ZIP 파일 저장 및 압축 해제
            timestamp = datetime.now().strftime('%Y%m%d')
            zip_path = ARCHIVE_DIR / f"cot_{report_type.value}_{timestamp}.zip"

            with open(zip_path, 'wb') as f:
                f.write(zip_data)

            # CSV 추출
            with zipfile.ZipFile(zip_path, 'r') as z:
                csv_files = [f for f in z.namelist() if f.endswith('.txt') or f.endswith('.csv')]
                if csv_files:
                    csv_path = ARCHIVE_DIR / f"cot_{report_type.value}_{timestamp}.csv"
                    with open(csv_path, 'wb') as f:
                        f.write(z.read(csv_files[0]))

                    print(f"[다운로드] COT 보고서: {csv_path}")
                    return str(csv_path)

        except Exception as e:
            print(f"[에러] COT 다운로드 실패: {e}")

        return ""

    def parse_legacy_report(self, csv_path: str) -> List[COTPosition]:
        """레거시 COT 보고서 파싱"""
        positions = []

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    try:
                        # 필드명은 CFTC 포맷에 따라 다를 수 있음
                        market_name = row.get('Market_and_Exchange_Names', row.get('Market and Exchange Names', ''))
                        report_date = row.get('Report_Date_as_MM_DD_YYYY', row.get('As of Date in Form YYYY-MM-DD', ''))

                        # 주요 시장만 필터링
                        is_tracked = False
                        contract_code = ""
                        for code, info in TRACKED_MARKETS.items():
                            if info['name'].split()[0].lower() in market_name.lower():
                                is_tracked = True
                                contract_code = code
                                break

                        if not is_tracked:
                            continue

                        # 포지션 데이터 추출
                        def safe_int(val):
                            try:
                                return int(str(val).replace(',', '').strip())
                            except:
                                return 0

                        comm_long = safe_int(row.get('Comm_Positions_Long_All', row.get('Commercial Long', 0)))
                        comm_short = safe_int(row.get('Comm_Positions_Short_All', row.get('Commercial Short', 0)))
                        noncomm_long = safe_int(row.get('NonComm_Positions_Long_All', row.get('Noncommercial Long', 0)))
                        noncomm_short = safe_int(row.get('NonComm_Positions_Short_All', row.get('Noncommercial Short', 0)))
                        noncomm_spread = safe_int(row.get('NonComm_Positions_Spread_All', row.get('Noncommercial Spreads', 0)))
                        oi = safe_int(row.get('Open_Interest_All', row.get('Open Interest', 0)))
                        oi_change = safe_int(row.get('Change_in_Open_Interest_All', 0))

                        # 소규모 투기자 계산
                        small_long = oi - comm_long - noncomm_long - noncomm_spread
                        small_short = oi - comm_short - noncomm_short - noncomm_spread

                        position = COTPosition(
                            report_date=report_date,
                            market_name=market_name,
                            contract_code=contract_code,
                            exchange=TRACKED_MARKETS.get(contract_code, {}).get('exchange', ''),
                            commercial_long=comm_long,
                            commercial_short=comm_short,
                            commercial_net=comm_long - comm_short,
                            non_commercial_long=noncomm_long,
                            non_commercial_short=noncomm_short,
                            non_commercial_net=noncomm_long - noncomm_short,
                            non_commercial_spreading=noncomm_spread,
                            small_spec_long=max(0, small_long),
                            small_spec_short=max(0, small_short),
                            small_spec_net=small_long - small_short,
                            open_interest=oi,
                            open_interest_change=oi_change,
                            commercial_pct=(comm_long + comm_short) / (2 * oi) * 100 if oi > 0 else 0,
                            non_commercial_pct=(noncomm_long + noncomm_short) / (2 * oi) * 100 if oi > 0 else 0
                        )

                        positions.append(position)

                    except Exception as e:
                        continue

        except Exception as e:
            print(f"[에러] CSV 파싱 실패: {e}")

        return positions

    def analyze_position(self, contract_code: str,
                        current: COTPosition,
                        historical: List[COTPosition] = None) -> COTAnalysis:
        """
        포지션 분석

        Args:
            contract_code: 계약 코드
            current: 현재 포지션
            historical: 과거 데이터 (52주)
        """
        # 주간 변화 계산
        weekly_change_comm = 0
        weekly_change_spec = 0

        if historical and len(historical) >= 2:
            prev = historical[-2]
            weekly_change_comm = current.commercial_net - prev.commercial_net
            weekly_change_spec = current.non_commercial_net - prev.non_commercial_net

        # 백분위 계산 (52주 기준)
        comm_percentile = 50.0
        spec_percentile = 50.0

        if historical and len(historical) >= 10:
            comm_nets = [h.commercial_net for h in historical]
            spec_nets = [h.non_commercial_net for h in historical]

            # 현재 값의 백분위
            comm_percentile = sum(1 for x in comm_nets if x <= current.commercial_net) / len(comm_nets) * 100
            spec_percentile = sum(1 for x in spec_nets if x <= current.non_commercial_net) / len(spec_nets) * 100

        # 시그널 결정
        signal, strength, commentary = self._determine_signal(
            current, comm_percentile, spec_percentile, weekly_change_comm, weekly_change_spec
        )

        return COTAnalysis(
            market_name=current.market_name,
            contract_code=contract_code,
            report_date=current.report_date,
            net_position_commercials=current.commercial_net,
            net_position_speculators=current.non_commercial_net,
            weekly_change_commercials=weekly_change_comm,
            weekly_change_speculators=weekly_change_spec,
            commercials_percentile=comm_percentile,
            speculators_percentile=spec_percentile,
            signal=signal,
            signal_strength=strength,
            commentary=commentary
        )

    def _determine_signal(self, position: COTPosition,
                         comm_pct: float, spec_pct: float,
                         comm_change: int, spec_change: int) -> Tuple[str, str, str]:
        """시그널 결정 로직"""

        # 상업적 거래자는 역행 지표 (극단적 롱 = 하락 신호)
        # 투기자는 순행 지표 (극단적 롱 = 상승 모멘텀, but 과열 주의)

        signal = "neutral"
        strength = "weak"
        commentary = ""

        # 상업적 거래자 분석
        if comm_pct >= 90:
            signal = "bearish"
            strength = "strong"
            commentary = "상업적 거래자 극단적 롱 (역행 신호: 하락 경고)"
        elif comm_pct <= 10:
            signal = "bullish"
            strength = "strong"
            commentary = "상업적 거래자 극단적 숏 (역행 신호: 상승 기대)"
        elif comm_pct >= 75:
            signal = "bearish"
            strength = "moderate"
            commentary = "상업적 거래자 높은 롱 비율"
        elif comm_pct <= 25:
            signal = "bullish"
            strength = "moderate"
            commentary = "상업적 거래자 높은 숏 비율"

        # 투기자 포지션으로 보완
        if spec_pct >= 90 and signal == "bullish":
            strength = "weak"
            commentary += " | 주의: 투기 포지션 과열"
        elif spec_pct <= 10 and signal == "bearish":
            strength = "weak"
            commentary += " | 투기자 익스트림 숏 (반등 가능)"

        # 변화 추세 확인
        if comm_change > 0 and spec_change < 0:
            commentary += " | 헤저 매수, 투기자 매도 중"
        elif comm_change < 0 and spec_change > 0:
            commentary += " | 헤저 매도, 투기자 매수 중"

        return signal, strength, commentary

    def generate_weekly_report(self) -> Dict[str, Any]:
        """주간 COT 분석 리포트 생성"""

        report = {
            'generated_at': datetime.now().isoformat(),
            'report_date': None,
            'markets': {},
            'alerts': [],
            'summary': {
                'bullish_markets': [],
                'bearish_markets': [],
                'neutral_markets': []
            }
        }

        # 최신 데이터 다운로드
        csv_path = self.download_latest_report()
        if not csv_path:
            return report

        # 파싱
        positions = self.parse_legacy_report(csv_path)
        if not positions:
            return report

        report['report_date'] = positions[0].report_date if positions else None

        # 시장별 분석
        for position in positions:
            code = position.contract_code
            if code not in TRACKED_MARKETS:
                continue

            analysis = self.analyze_position(code, position, self.historical_data.get(code, []))

            report['markets'][code] = {
                'name': TRACKED_MARKETS[code]['name'],
                'category': TRACKED_MARKETS[code]['category'],
                'position': asdict(position),
                'analysis': asdict(analysis)
            }

            # 요약 분류
            if analysis.signal == 'bullish':
                report['summary']['bullish_markets'].append(code)
            elif analysis.signal == 'bearish':
                report['summary']['bearish_markets'].append(code)
            else:
                report['summary']['neutral_markets'].append(code)

            # 강한 시그널 알림
            if analysis.signal_strength == 'strong':
                report['alerts'].append({
                    'market': TRACKED_MARKETS[code]['name'],
                    'signal': analysis.signal,
                    'message': analysis.commentary
                })

            # 히스토리 업데이트
            if code not in self.historical_data:
                self.historical_data[code] = []
            self.historical_data[code].append(position)
            # 52주만 유지
            self.historical_data[code] = self.historical_data[code][-52:]

        return report

    def save_report(self, report: Dict[str, Any]) -> str:
        """리포트 저장"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = ARCHIVE_DIR / f"cot_analysis_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        print(f"[저장] {filename}")
        return str(filename)

    def get_market_summary(self, contract_code: str) -> Optional[Dict[str, Any]]:
        """특정 시장 요약"""
        if contract_code not in TRACKED_MARKETS:
            return None

        # 최신 데이터에서 조회
        # 실제로는 캐시된 데이터나 DB에서 조회
        return {
            'contract': contract_code,
            'name': TRACKED_MARKETS[contract_code]['name'],
            'category': TRACKED_MARKETS[contract_code]['category'],
            'message': "데이터 로드 필요 - generate_weekly_report() 실행"
        }


def get_next_release_date() -> datetime:
    """다음 COT 발표일 계산 (매주 금요일 3:30 PM ET)"""
    now = datetime.now()
    days_until_friday = (4 - now.weekday()) % 7

    if days_until_friday == 0 and now.hour >= 16:  # 금요일 4PM 이후면 다음 주
        days_until_friday = 7

    next_friday = now + timedelta(days=days_until_friday)
    return next_friday.replace(hour=15, minute=30, second=0, microsecond=0)


# 사용 예시
if __name__ == "__main__":
    collector = COTCollector()

    print("=== COT 보고서 분석 ===")
    print(f"다음 발표일: {get_next_release_date().strftime('%Y-%m-%d %H:%M ET')}")

    # 주간 리포트 생성
    print("\n주간 리포트 생성 중...")
    report = collector.generate_weekly_report()

    if report['report_date']:
        print(f"\n보고서 날짜: {report['report_date']}")

        print("\n=== 시장별 시그널 ===")
        print(f"🟢 강세: {', '.join(report['summary']['bullish_markets']) or '없음'}")
        print(f"🔴 약세: {', '.join(report['summary']['bearish_markets']) or '없음'}")
        print(f"⚪ 중립: {', '.join(report['summary']['neutral_markets']) or '없음'}")

        if report['alerts']:
            print("\n=== 알림 ===")
            for alert in report['alerts']:
                emoji = "🟢" if alert['signal'] == 'bullish' else "🔴"
                print(f"{emoji} {alert['market']}: {alert['message']}")

        # 저장
        collector.save_report(report)
    else:
        print("보고서 데이터를 가져오지 못했습니다.")
