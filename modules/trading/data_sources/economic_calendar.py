#!/usr/bin/env python3
"""
경제 지표 발표 일정 캘린더.

- 주요 경제 지표 발표 일정 추적
- 1개월 일정표 생성
- 발표일 알림
- 예상치 vs 실제치 비교

주요 발표 일정:
- CPI: 매월 중순 (보통 10-15일)
- 고용보고서 (NFP): 매월 첫째 금요일
- FOMC: 연 8회 (1,3,5,6,7,9,11,12월)
- GDP: 분기별 (1,4,7,10월)
- PCE: 매월 말
"""

from __future__ import annotations

import calendar
import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any

# 로거 설정
logger = logging.getLogger(__name__)

# 설정 - config에서 가져오거나 기본값 사용
try:
    from config import CALENDAR_DIR
except ImportError:
    CALENDAR_DIR = Path.home() / ".claude" / "modules" / "trading" / "data_sources" / "calendar"
    CALENDAR_DIR.mkdir(parents=True, exist_ok=True)


class Importance(Enum):
    """중요도."""

    CRITICAL = "critical"  # 시장에 큰 영향
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EventType(Enum):
    """이벤트 유형."""

    INFLATION = "inflation"
    EMPLOYMENT = "employment"
    GDP = "gdp"
    CENTRAL_BANK = "central_bank"
    CONSUMER = "consumer"
    HOUSING = "housing"
    MANUFACTURING = "manufacturing"
    TRADE = "trade"


@dataclass
class EconomicEvent:
    """경제 이벤트."""

    name: str
    event_type: EventType
    importance: Importance
    date: datetime
    time_est: str  # "08:30 ET" 형식
    frequency: str  # monthly, weekly, quarterly, annual
    description: str = ""
    previous: float | None = None
    forecast: float | None = None
    actual: float | None = None
    unit: str = ""
    impact: str = ""  # 예상 영향


@dataclass
class MonthlyCalendar:
    """월간 캘린더."""

    year: int
    month: int
    events: list[EconomicEvent] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)


# 2026년 주요 경제 지표 발표 일정 (예상)
# 실제 일정은 각 기관에서 발표
RECURRING_EVENTS = [
    # CPI - 매월 중순
    {
        "name": "CPI (소비자물가지수)",
        "event_type": EventType.INFLATION,
        "importance": Importance.CRITICAL,
        "time_est": "08:30 ET",
        "frequency": "monthly",
        "day_rule": "second_tuesday_plus_one",  # 둘째 주 화요일 다음날(수)
        "description": "전월 대비 물가 변동률",
        "unit": "%",
        "impact": "높으면 금리 인상 압력, 주식 하락 가능"
    },
    # Core CPI
    {
        "name": "Core CPI (근원 CPI)",
        "event_type": EventType.INFLATION,
        "importance": Importance.CRITICAL,
        "time_est": "08:30 ET",
        "frequency": "monthly",
        "day_rule": "second_tuesday_plus_one",
        "description": "식품/에너지 제외 물가",
        "unit": "%",
        "impact": "연준 정책 결정에 핵심 지표"
    },
    # 고용보고서 (NFP)
    {
        "name": "비농업 고용 (NFP)",
        "event_type": EventType.EMPLOYMENT,
        "importance": Importance.CRITICAL,
        "time_est": "08:30 ET",
        "frequency": "monthly",
        "day_rule": "first_friday",
        "description": "전월 비농업 부문 신규 고용",
        "unit": "천 명",
        "impact": "예상 상회시 달러 강세, 금리 상승 압력"
    },
    # 실업률
    {
        "name": "실업률",
        "event_type": EventType.EMPLOYMENT,
        "importance": Importance.CRITICAL,
        "time_est": "08:30 ET",
        "frequency": "monthly",
        "day_rule": "first_friday",
        "description": "실업자 비율",
        "unit": "%",
        "impact": "상승시 경기 침체 우려"
    },
    # PCE
    {
        "name": "PCE 물가지수",
        "event_type": EventType.INFLATION,
        "importance": Importance.CRITICAL,
        "time_est": "08:30 ET",
        "frequency": "monthly",
        "day_rule": "last_friday",
        "description": "연준 선호 인플레이션 지표",
        "unit": "%",
        "impact": "연준 금리 결정의 핵심"
    },
    # 신규 실업수당 청구
    {
        "name": "신규 실업수당 청구",
        "event_type": EventType.EMPLOYMENT,
        "importance": Importance.HIGH,
        "time_est": "08:30 ET",
        "frequency": "weekly",
        "day_rule": "every_thursday",
        "description": "주간 신규 실업수당 청구 건수",
        "unit": "천 건",
        "impact": "증가시 고용 시장 악화 신호"
    },
    # 소비자심리지수
    {
        "name": "미시간 소비자심리지수",
        "event_type": EventType.CONSUMER,
        "importance": Importance.HIGH,
        "time_est": "10:00 ET",
        "frequency": "monthly",
        "day_rule": "second_friday",  # 예비치
        "description": "소비자 경기 전망",
        "unit": "Index",
        "impact": "하락시 소비 위축 우려"
    },
    # 소매판매
    {
        "name": "소매판매",
        "event_type": EventType.CONSUMER,
        "importance": Importance.HIGH,
        "time_est": "08:30 ET",
        "frequency": "monthly",
        "day_rule": "mid_month",  # 15일 전후
        "description": "전월 소매판매 변동",
        "unit": "%",
        "impact": "소비 트렌드 파악"
    },
    # ISM 제조업
    {
        "name": "ISM 제조업 PMI",
        "event_type": EventType.MANUFACTURING,
        "importance": Importance.HIGH,
        "time_est": "10:00 ET",
        "frequency": "monthly",
        "day_rule": "first_business_day",
        "description": "제조업 경기 선행지표",
        "unit": "Index",
        "impact": "50 이하 = 위축"
    },
    # ISM 서비스업
    {
        "name": "ISM 서비스업 PMI",
        "event_type": EventType.MANUFACTURING,
        "importance": Importance.HIGH,
        "time_est": "10:00 ET",
        "frequency": "monthly",
        "day_rule": "third_business_day",
        "description": "서비스업 경기 선행지표",
        "unit": "Index",
        "impact": "50 이하 = 위축"
    },
    # 주택착공
    {
        "name": "주택착공건수",
        "event_type": EventType.HOUSING,
        "importance": Importance.MEDIUM,
        "time_est": "08:30 ET",
        "frequency": "monthly",
        "day_rule": "mid_month",
        "description": "신규 주택 착공",
        "unit": "만 호",
        "impact": "주택 시장 선행지표"
    },
]

# FOMC 회의 일정 (2026년 예상)
FOMC_2026 = [
    {"start": "2026-01-27", "end": "2026-01-28", "statement": "2026-01-28"},
    {"start": "2026-03-17", "end": "2026-03-18", "statement": "2026-03-18"},
    {"start": "2026-05-05", "end": "2026-05-06", "statement": "2026-05-06"},
    {"start": "2026-06-16", "end": "2026-06-17", "statement": "2026-06-17"},
    {"start": "2026-07-28", "end": "2026-07-29", "statement": "2026-07-29"},
    {"start": "2026-09-15", "end": "2026-09-16", "statement": "2026-09-16"},
    {"start": "2026-11-03", "end": "2026-11-04", "statement": "2026-11-04"},
    {"start": "2026-12-15", "end": "2026-12-16", "statement": "2026-12-16"},
]

# GDP 발표 일정 (분기별, 3차례 발표)
GDP_RELEASES = {
    "Q4_2025": {"advance": "2026-01-30", "second": "2026-02-27", "third": "2026-03-27"},
    "Q1_2026": {"advance": "2026-04-30", "second": "2026-05-28", "third": "2026-06-25"},
    "Q2_2026": {"advance": "2026-07-30", "second": "2026-08-27", "third": "2026-09-24"},
    "Q3_2026": {"advance": "2026-10-29", "second": "2026-11-25", "third": "2026-12-23"},
}


class EconomicCalendar:
    """경제 지표 캘린더."""

    def __init__(self) -> None:
        """캘린더 초기화."""
        self.events: list[EconomicEvent] = []

    def _get_nth_weekday(self, year: int, month: int, weekday: int, n: int) -> datetime:
        """n번째 특정 요일 찾기 (weekday: 0=월, 4=금)."""
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()

        # 첫 번째 해당 요일까지의 일수
        days_until = (weekday - first_weekday + 7) % 7
        first_occurrence = first_day + timedelta(days=days_until)

        # n번째 (1-indexed)
        return first_occurrence + timedelta(weeks=n-1)

    def _get_last_weekday(self, year: int, month: int, weekday: int) -> datetime:
        """마지막 특정 요일 찾기."""
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])
        days_back = (last_day.weekday() - weekday + 7) % 7
        return last_day - timedelta(days=days_back)

    def _get_first_business_day(self, year: int, month: int) -> datetime:
        """첫 영업일."""
        day = datetime(year, month, 1)
        while day.weekday() >= 5:  # 주말이면
            day += timedelta(days=1)
        return day

    def _apply_day_rule(self, year: int, month: int, rule: str) -> datetime | None:
        """날짜 규칙 적용."""
        if rule == "first_friday":
            return self._get_nth_weekday(year, month, 4, 1)
        elif rule == "second_friday":
            return self._get_nth_weekday(year, month, 4, 2)
        elif rule == "second_tuesday_plus_one":
            tuesday = self._get_nth_weekday(year, month, 1, 2)
            return tuesday + timedelta(days=1)  # 수요일
        elif rule == "last_friday":
            return self._get_last_weekday(year, month, 4)
        elif rule == "first_business_day":
            return self._get_first_business_day(year, month)
        elif rule == "third_business_day":
            first = self._get_first_business_day(year, month)
            day = first
            count = 1
            while count < 3:
                day += timedelta(days=1)
                if day.weekday() < 5:
                    count += 1
            return day
        elif rule == "mid_month":
            return datetime(year, month, 15)
        elif rule == "every_thursday":
            # 주간 이벤트는 별도 처리
            return None
        else:
            return datetime(year, month, 15)

    def generate_monthly_events(self, year: int, month: int) -> list[EconomicEvent]:
        """월간 이벤트 생성."""
        events = []

        # 반복 이벤트
        for event_def in RECURRING_EVENTS:
            if event_def["frequency"] == "weekly":
                # 주간 이벤트 (목요일 실업수당)
                if event_def["day_rule"] == "every_thursday":
                    first_day = datetime(year, month, 1)
                    last_day = datetime(year, month, calendar.monthrange(year, month)[1])
                    day = first_day
                    while day <= last_day:
                        if day.weekday() == 3:  # 목요일
                            events.append(EconomicEvent(
                                name=event_def["name"],
                                event_type=event_def["event_type"],
                                importance=event_def["importance"],
                                date=day,
                                time_est=event_def["time_est"],
                                frequency=event_def["frequency"],
                                description=event_def["description"],
                                unit=event_def.get("unit", ""),
                                impact=event_def.get("impact", "")
                            ))
                        day += timedelta(days=1)
            else:
                # 월간 이벤트
                event_date = self._apply_day_rule(year, month, event_def["day_rule"])
                if event_date:
                    events.append(EconomicEvent(
                        name=event_def["name"],
                        event_type=event_def["event_type"],
                        importance=event_def["importance"],
                        date=event_date,
                        time_est=event_def["time_est"],
                        frequency=event_def["frequency"],
                        description=event_def["description"],
                        unit=event_def.get("unit", ""),
                        impact=event_def.get("impact", "")
                    ))

        # FOMC
        for fomc in FOMC_2026:
            stmt_date = datetime.strptime(fomc["statement"], "%Y-%m-%d")
            if stmt_date.year == year and stmt_date.month == month:
                events.append(EconomicEvent(
                    name="FOMC 성명서 발표",
                    event_type=EventType.CENTRAL_BANK,
                    importance=Importance.CRITICAL,
                    date=stmt_date,
                    time_est="14:00 ET",
                    frequency="8x/year",
                    description="연방준비제도 금리 결정",
                    impact="금리 변동시 전 자산 급변동"
                ))

        # GDP
        for quarter, dates in GDP_RELEASES.items():
            for release_type, date_str in dates.items():
                gdp_date = datetime.strptime(date_str, "%Y-%m-%d")
                if gdp_date.year == year and gdp_date.month == month:
                    release_name = {
                        "advance": "GDP 속보치",
                        "second": "GDP 수정치",
                        "third": "GDP 확정치"
                    }[release_type]

                    events.append(EconomicEvent(
                        name=f"{release_name} ({quarter})",
                        event_type=EventType.GDP,
                        importance=Importance.CRITICAL if release_type == "advance" else Importance.HIGH,
                        date=gdp_date,
                        time_est="08:30 ET",
                        frequency="quarterly",
                        description=f"분기별 경제성장률 ({release_type})",
                        unit="%",
                        impact="예상 하회시 경기 침체 우려"
                    ))

        # 날짜순 정렬
        events.sort(key=lambda x: x.date)
        return events

    def get_upcoming_events(self, days: int = 30) -> list[EconomicEvent]:
        """향후 N일 이벤트."""
        today = datetime.now()
        end_date = today + timedelta(days=days)

        all_events = []

        # 필요한 달 계산
        current = today
        while current <= end_date:
            month_events = self.generate_monthly_events(current.year, current.month)
            all_events.extend(month_events)
            # 다음 달로
            if current.month == 12:
                current = datetime(current.year + 1, 1, 1)
            else:
                current = datetime(current.year, current.month + 1, 1)

        # 기간 필터링
        filtered = [e for e in all_events if today <= e.date <= end_date]
        filtered.sort(key=lambda x: x.date)

        return filtered

    def get_this_week_events(self) -> list[EconomicEvent]:
        """이번 주 이벤트."""
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        all_events = self.generate_monthly_events(today.year, today.month)
        return [e for e in all_events if start_of_week <= e.date <= end_of_week]

    def generate_calendar_table(self, days: int = 30) -> str:
        """마크다운 캘린더 테이블 생성."""
        events = self.get_upcoming_events(days)

        lines = [
            f"# 경제 지표 발표 일정 (향후 {days}일)",
            f"> 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 주요 일정 요약",
            "",
            "| 날짜 | 시간 | 지표 | 중요도 | 예상 영향 |",
            "|------|------|------|--------|----------|"
        ]

        importance_emoji = {
            Importance.CRITICAL: "🔴",
            Importance.HIGH: "🟠",
            Importance.MEDIUM: "🟡",
            Importance.LOW: "⚪"
        }

        for event in events:
            emoji = importance_emoji.get(event.importance, "⚪")
            date_str = event.date.strftime("%m/%d (%a)")
            impact = event.impact[:30] + "..." if len(event.impact) > 30 else event.impact
            lines.append(
                f"| {date_str} | {event.time_est} | {emoji} {event.name} | {event.importance.value} | {impact} |"
            )

        # 카테고리별 정리
        lines.extend([
            "",
            "---",
            "",
            "## 카테고리별 분류",
            ""
        ])

        categories = {}
        for event in events:
            cat = event.event_type.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(event)

        cat_names = {
            "inflation": "📊 인플레이션",
            "employment": "👷 고용",
            "gdp": "📈 GDP",
            "central_bank": "🏦 중앙은행",
            "consumer": "🛒 소비자",
            "housing": "🏠 주택",
            "manufacturing": "🏭 제조업"
        }

        for cat, cat_events in categories.items():
            lines.append(f"### {cat_names.get(cat, cat)}")
            for event in cat_events:
                lines.append(f"- **{event.date.strftime('%m/%d')}** {event.name}")
            lines.append("")

        return "\n".join(lines)

    def save_calendar(self, days: int = 30) -> str:
        """캘린더 저장."""
        content = self.generate_calendar_table(days)
        filename = CALENDAR_DIR / f"calendar_{datetime.now().strftime('%Y%m%d')}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"캘린더 저장 완료: {filename}")
        return str(filename)

    def get_today_events(self) -> list[EconomicEvent]:
        """오늘 이벤트."""
        today = datetime.now().date()
        events = self.generate_monthly_events(today.year, today.month)
        return [e for e in events if e.date.date() == today]

    def check_alerts(self) -> list[dict[str, Any]]:
        """알림 체크 (오늘/내일 중요 이벤트)."""
        alerts = []
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        events = self.get_upcoming_events(days=2)

        for event in events:
            if event.importance in [Importance.CRITICAL, Importance.HIGH]:
                if event.date.date() == today:
                    alerts.append({
                        "type": "today",
                        "event": event.name,
                        "time": event.time_est,
                        "importance": event.importance.value,
                        "message": f"🚨 오늘 {event.time_est}: {event.name}"
                    })
                elif event.date.date() == tomorrow:
                    alerts.append({
                        "type": "tomorrow",
                        "event": event.name,
                        "time": event.time_est,
                        "importance": event.importance.value,
                        "message": f"📅 내일 {event.time_est}: {event.name}"
                    })

        return alerts


# 사용 예시
if __name__ == "__main__":
    calendar = EconomicCalendar()

    print("=== 이번 주 경제 지표 ===")
    this_week = calendar.get_this_week_events()
    for event in this_week:
        print(f"  {event.date.strftime('%m/%d %a')} {event.time_est}: {event.name}")

    print("\n=== 향후 30일 일정표 ===")
    table = calendar.generate_calendar_table(30)
    print(table[:2000])  # 처음 2000자만

    # 저장
    calendar.save_calendar(30)

    print("\n=== 알림 ===")
    alerts = calendar.check_alerts()
    for alert in alerts:
        print(f"  {alert['message']}")
