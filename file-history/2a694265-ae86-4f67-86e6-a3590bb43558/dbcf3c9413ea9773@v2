#!/usr/bin/env python3
"""경제 시황 보고서 PNG 생성기"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

# 설정
WIDTH = 1200
PADDING = 40
LINE_HEIGHT = 32
SECTION_GAP = 20

# 색상
BG_COLOR = "#1a1a2e"
TEXT_COLOR = "#ffffff"
HEADER_COLOR = "#00d4ff"
ACCENT_COLOR = "#ff6b6b"
TABLE_HEADER_BG = "#16213e"
TABLE_ROW_BG = "#0f3460"
TABLE_ALT_BG = "#1a1a40"
POSITIVE_COLOR = "#00ff88"
NEGATIVE_COLOR = "#ff4757"

# 폰트 설정 (시스템 폰트 사용)
def get_font(size, bold=False):
    font_paths = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS 한글
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

# 데이터 (2026-01-31)
report_date = "2026-01-31"
generated_time = datetime.now().strftime("%Y-%m-%d %H:%M")

market_data = [
    ("VIX (공포지수)", "17.01", "+0.77%", True),
    ("MOVE Index", "60.73", "-", None),
    ("Gold (금)", "$5,067.50", "-5.37%", False),
    ("EUR/USD", "1.19", "-0.68%", False),
    ("USD/JPY", "154.73", "+1.12%", True),
    ("NASDAQ (NQ)", "25,859.25", "-0.54%", False),
    ("S&P 500 (ES)", "6,975.50", "-0.25%", False),
    ("Bitcoin", "$82,659", "+0.03%", True),
]

fred_data = [
    ("연방기금금리", "3.72%", "2025-12"),
    ("10년 국채", "4.24%", "01-29"),
    ("2년 국채", "3.53%", "01-29"),
    ("10Y-2Y 스프레드", "0.74%", "01-30"),
    ("CPI", "326.03", "2025-12"),
    ("실업률", "4.40%", "2025-12"),
]

sofr_data = {
    "current": "3.65%",
    "trend": "01-23: 3.65% → 01-29: 3.65%",
    "analysis": "일주일간 안정 유지"
}

move_data = {
    "current": "60.73",
    "trend": "01-26: 55.8 → 01-30: 59.2",
    "analysis": "낮은 변동성 (안정적)"
}

# 이미지 생성
def create_report():
    # 높이 계산
    height = 1400
    img = Image.new('RGB', (WIDTH, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(36, bold=True)
    font_section = get_font(24, bold=True)
    font_normal = get_font(18)
    font_small = get_font(14)
    font_table = get_font(16)

    y = PADDING

    # 제목
    draw.text((PADDING, y), "📊 일일 경제 보고서", fill=HEADER_COLOR, font=font_title)
    y += 50
    draw.text((PADDING, y), f"{report_date} | 생성: {generated_time}", fill="#888888", font=font_small)
    y += 40

    # 구분선
    draw.line([(PADDING, y), (WIDTH - PADDING, y)], fill="#333355", width=2)
    y += SECTION_GAP

    # 1. 시세표
    draw.text((PADDING, y), "1️⃣ 시세표", fill=HEADER_COLOR, font=font_section)
    y += 40

    # 테이블 헤더
    col_widths = [300, 180, 120]
    headers = ["항목", "가격", "변동"]
    x = PADDING
    draw.rectangle([(x, y), (WIDTH - PADDING, y + 35)], fill=TABLE_HEADER_BG)
    for i, (header, width) in enumerate(zip(headers, col_widths)):
        draw.text((x + 10, y + 8), header, fill=TEXT_COLOR, font=font_table)
        x += width
    y += 38

    # 테이블 데이터
    for idx, (name, price, change, is_positive) in enumerate(market_data):
        bg = TABLE_ROW_BG if idx % 2 == 0 else TABLE_ALT_BG
        draw.rectangle([(PADDING, y), (WIDTH - PADDING, y + 32)], fill=bg)

        x = PADDING
        draw.text((x + 10, y + 6), name, fill=TEXT_COLOR, font=font_table)
        x += col_widths[0]
        draw.text((x + 10, y + 6), price, fill=TEXT_COLOR, font=font_table)
        x += col_widths[1]

        if is_positive is True:
            color = POSITIVE_COLOR
        elif is_positive is False:
            color = NEGATIVE_COLOR
        else:
            color = "#888888"
        draw.text((x + 10, y + 6), change, fill=color, font=font_table)
        y += 34

    y += SECTION_GAP

    # 2. SOFR / MOVE
    draw.text((PADDING, y), "2️⃣ SOFR / MOVE Index", fill=HEADER_COLOR, font=font_section)
    y += 40

    # SOFR 박스
    draw.rectangle([(PADDING, y), (WIDTH//2 - 20, y + 100)], fill=TABLE_HEADER_BG, outline="#00d4ff", width=1)
    draw.text((PADDING + 15, y + 10), "SOFR", fill=HEADER_COLOR, font=font_normal)
    draw.text((PADDING + 15, y + 40), f"현재: {sofr_data['current']}", fill=TEXT_COLOR, font=font_table)
    draw.text((PADDING + 15, y + 65), sofr_data['analysis'], fill="#888888", font=font_small)

    # MOVE 박스
    draw.rectangle([(WIDTH//2 + 20, y), (WIDTH - PADDING, y + 100)], fill=TABLE_HEADER_BG, outline="#ff6b6b", width=1)
    draw.text((WIDTH//2 + 35, y + 10), "MOVE Index", fill=ACCENT_COLOR, font=font_normal)
    draw.text((WIDTH//2 + 35, y + 40), f"현재: {move_data['current']}", fill=TEXT_COLOR, font=font_table)
    draw.text((WIDTH//2 + 35, y + 65), move_data['analysis'], fill="#888888", font=font_small)

    y += 120

    # 3. FRED 지표
    draw.text((PADDING, y), "3️⃣ 주요 경제 지표 (FRED)", fill=HEADER_COLOR, font=font_section)
    y += 40

    # FRED 테이블
    col_widths_fred = [250, 150, 150]
    headers_fred = ["지표", "값", "기준일"]
    x = PADDING
    draw.rectangle([(x, y), (WIDTH - PADDING, y + 35)], fill=TABLE_HEADER_BG)
    for header, width in zip(headers_fred, col_widths_fred):
        draw.text((x + 10, y + 8), header, fill=TEXT_COLOR, font=font_table)
        x += width
    y += 38

    for idx, (name, value, date) in enumerate(fred_data):
        bg = TABLE_ROW_BG if idx % 2 == 0 else TABLE_ALT_BG
        draw.rectangle([(PADDING, y), (WIDTH - PADDING, y + 32)], fill=bg)

        x = PADDING
        draw.text((x + 10, y + 6), name, fill=TEXT_COLOR, font=font_table)
        x += col_widths_fred[0]
        draw.text((x + 10, y + 6), value, fill=HEADER_COLOR, font=font_table)
        x += col_widths_fred[1]
        draw.text((x + 10, y + 6), date, fill="#888888", font=font_table)
        y += 34

    y += SECTION_GAP

    # 4. 시장 분석
    draw.text((PADDING, y), "4️⃣ 시장 현황 분석", fill=HEADER_COLOR, font=font_section)
    y += 40

    analysis_items = [
        ("VIX 17.01", "보통 수준의 변동성", "#ffcc00"),
        ("10Y-2Y 스프레드 0.74%", "정상적인 수익률 곡선", POSITIVE_COLOR),
        ("연방기금금리 3.72%", "금리 동결 기조 유지", "#888888"),
    ]

    for label, desc, color in analysis_items:
        draw.ellipse([(PADDING, y + 6), (PADDING + 12, y + 18)], fill=color)
        draw.text((PADDING + 25, y), f"{label} - {desc}", fill=TEXT_COLOR, font=font_normal)
        y += 35

    y += SECTION_GAP

    # 푸터
    draw.line([(PADDING, y), (WIDTH - PADDING, y)], fill="#333355", width=1)
    y += 15
    draw.text((PADDING, y), "출처: Yahoo Finance, NY Fed, FRED, CoinGecko", fill="#666666", font=font_small)
    y += 25
    draw.text((PADDING, y), "⚠️ 본 보고서는 정보 제공 목적이며 투자 조언이 아닙니다.", fill="#ff6b6b", font=font_small)

    # 이미지 저장
    output_path = os.path.expanduser("~/.claude/modules/trading/reports/export/daily_report_2026-01-31.png")
    img.save(output_path, "PNG", quality=95)
    print(f"✅ PNG 생성 완료: {output_path}")
    return output_path

if __name__ == "__main__":
    create_report()
