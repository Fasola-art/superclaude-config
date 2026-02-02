#!/usr/bin/env python3
"""
일일 경제 보고서 내보내기
- Excel (.xlsx): 모든 데이터 통합 (5개 시트 - 시황 포함)
- PNG 이미지: 시세표 + SOFR/MOVE 차트 + 시황 통합 (1개 파일)

매일 저녁 10시 자동 생성
"""

import json
import os
import textwrap
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# 경로 설정
REPORTS_DIR = Path.home() / ".claude" / "modules" / "trading" / "reports" / "daily"
EXPORT_DIR = Path.home() / ".claude" / "modules" / "trading" / "reports" / "export"
HISTORY_FILE = EXPORT_DIR / "daily_history.xlsx"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_report_json(date: str = None) -> Optional[Dict]:
    """보고서 JSON 로드"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    json_file = REPORTS_DIR / f"daily_report_{date}.json"
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def load_outlook(date: str = None) -> Optional[Dict]:
    """시황 로드"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    outlook_file = REPORTS_DIR / f"outlook_{date}.json"
    if outlook_file.exists():
        with open(outlook_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def export_to_excel(report: Dict, outlook: Dict = None, append_history: bool = True) -> str:
    """
    Excel 파일로 내보내기 (5개 시트 통합)
    """
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

    date = report.get('date', datetime.now().strftime('%Y-%m-%d'))

    wb = openpyxl.Workbook()

    # 스타일 정의
    header_font = Font(bold=True, color="FFFFFF", size=11)
    header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
    number_font = Font(size=11, bold=True)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # ===== 시트 1: 시세표 =====
    ws1 = wb.active
    ws1.title = "시세표"

    ws1['A1'] = f"일일 시세표 - {date}"
    ws1['A1'].font = Font(bold=True, size=14)
    ws1.merge_cells('A1:D1')

    headers = ['#', '항목', '가격', '변동']
    for col, header in enumerate(headers, 1):
        cell = ws1.cell(row=3, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
        cell.border = thin_border

    quotes = report.get('quotes', [])
    for i, q in enumerate(quotes, 1):
        row = i + 3
        ws1.cell(row=row, column=1, value=i).border = thin_border
        ws1.cell(row=row, column=2, value=q.get('name', '')).border = thin_border

        price_cell = ws1.cell(row=row, column=3, value=q.get('price', 0))
        price_cell.number_format = '#,##0.00'
        price_cell.font = number_font
        price_cell.border = thin_border

        change = q.get('change_pct')
        change_cell = ws1.cell(row=row, column=4, value=f"{change:+.2f}%" if change else "-")
        change_cell.border = thin_border
        if change:
            change_cell.font = Font(color="00AA00" if change > 0 else "AA0000", bold=True)

    ws1.column_dimensions['A'].width = 5
    ws1.column_dimensions['B'].width = 30
    ws1.column_dimensions['C'].width = 15
    ws1.column_dimensions['D'].width = 12

    # ===== 시트 2: SOFR/MOVE =====
    ws2 = wb.create_sheet("SOFR_MOVE")

    ws2['A1'] = f"SOFR / MOVE Index 동향 - {date}"
    ws2['A1'].font = Font(bold=True, size=14)
    ws2.merge_cells('A1:C1')

    ws2['A3'] = "SOFR (Secured Overnight Financing Rate)"
    ws2['A3'].font = Font(bold=True, size=12)
    ws2['A4'] = "현재"
    ws2['B4'] = report.get('sofr_current', 0)
    ws2['C4'] = "%"

    ws2['A5'] = "분석"
    ws2['B5'] = report.get('sofr_analysis', '')
    ws2.merge_cells('B5:D5')

    sofr_trend = report.get('sofr_trend', [])
    ws2['A7'] = "일별 추이"
    ws2['A7'].font = Font(bold=True)
    for i, t in enumerate(sofr_trend[-7:], 8):
        ws2.cell(row=i, column=1, value=t.get('date', ''))
        ws2.cell(row=i, column=2, value=t.get('rate', 0))

    ws2['A17'] = "MOVE Index (채권 변동성)"
    ws2['A17'].font = Font(bold=True, size=12)
    ws2['A18'] = "현재"
    ws2['B18'] = report.get('move_current', 0)

    ws2['A19'] = "분석"
    ws2['B19'] = report.get('move_analysis', '')
    ws2.merge_cells('B19:D19')

    move_trend = report.get('move_trend', [])
    ws2['A21'] = "일별 추이"
    ws2['A21'].font = Font(bold=True)
    for i, t in enumerate(move_trend[-7:], 22):
        ws2.cell(row=i, column=1, value=t.get('date', ''))
        ws2.cell(row=i, column=2, value=t.get('value', 0))

    ws2.column_dimensions['A'].width = 15
    ws2.column_dimensions['B'].width = 50

    # ===== 시트 3: 경제 지표 =====
    ws3 = wb.create_sheet("경제지표")

    ws3['A1'] = f"주요 경제 지표 (FRED) - {date}"
    ws3['A1'].font = Font(bold=True, size=14)
    ws3.merge_cells('A1:C1')

    headers = ['지표', '값', '기준일']
    for col, header in enumerate(headers, 1):
        cell = ws3.cell(row=3, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border

    indicators = report.get('economic_indicators', [])
    for i, ind in enumerate(indicators, 1):
        row = i + 3
        ws3.cell(row=row, column=1, value=ind.get('name', '')).border = thin_border

        value_cell = ws3.cell(row=row, column=2, value=ind.get('value', 0))
        value_cell.number_format = '0.00'
        value_cell.font = number_font
        value_cell.border = thin_border

        ws3.cell(row=row, column=3, value=ind.get('date', '')).border = thin_border

    ws3.column_dimensions['A'].width = 25
    ws3.column_dimensions['B'].width = 15
    ws3.column_dimensions['C'].width = 15

    # ===== 시트 4: 내일 일정 =====
    ws4 = wb.create_sheet("내일일정")

    ws4['A1'] = f"내일 예정 이벤트"
    ws4['A1'].font = Font(bold=True, size=14)

    headers = ['시간', '지표', '중요도']
    for col, header in enumerate(headers, 1):
        cell = ws4.cell(row=3, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border

    events = report.get('tomorrow_events', [])
    for i, event in enumerate(events, 1):
        row = i + 3
        ws4.cell(row=row, column=1, value=event.get('time', '')).border = thin_border
        ws4.cell(row=row, column=2, value=event.get('name', '')).border = thin_border

        importance = event.get('importance', '')
        imp_cell = ws4.cell(row=row, column=3, value=importance)
        imp_cell.border = thin_border
        if importance == 'critical':
            imp_cell.fill = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")
        elif importance == 'high':
            imp_cell.fill = PatternFill(start_color="FFB347", end_color="FFB347", fill_type="solid")

    ws4.column_dimensions['A'].width = 12
    ws4.column_dimensions['B'].width = 35
    ws4.column_dimensions['C'].width = 12

    # ===== 시트 5: 시황/전망 =====
    ws5 = wb.create_sheet("시황전망")

    ws5['A1'] = f"경제 시황 및 전망 - {date}"
    ws5['A1'].font = Font(bold=True, size=14)
    ws5.merge_cells('A1:D1')

    if outlook:
        outlook_text = outlook.get('text', '')
        ws5['A3'] = outlook_text
        ws5['A3'].alignment = Alignment(wrap_text=True, vertical='top')
        ws5.merge_cells('A3:D30')

        ws5['A32'] = f"생성: {outlook.get('model', 'N/A')} | 비용: ${outlook.get('cost', 0):.4f}"
        ws5['A32'].font = Font(size=9, color="888888")
    else:
        ws5['A3'] = "(시황 데이터 없음)"

    ws5.column_dimensions['A'].width = 80

    # 저장
    daily_file = EXPORT_DIR / f"daily_report_{date}.xlsx"
    wb.save(daily_file)
    print(f"[저장] Excel: {daily_file}")

    # 히스토리에 추가
    if append_history:
        append_to_history(report)

    return str(daily_file)


def append_to_history(report: Dict):
    """히스토리 파일에 데이터 추가 (누적)"""
    import openpyxl
    from openpyxl.styles import Font, Border, Side

    date = report.get('date', datetime.now().strftime('%Y-%m-%d'))

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    if HISTORY_FILE.exists():
        wb = openpyxl.load_workbook(HISTORY_FILE)
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "시세히스토리"

        headers = ['날짜', 'VIX', 'MOVE', 'Gold', 'EUR/USD', 'USD/JPY', 'NASDAQ', 'S&P500', 'Bitcoin', 'SOFR', '10Y', '2Y', '10Y-2Y']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.border = thin_border

    ws = wb['시세히스토리']

    last_row = ws.max_row + 1

    for row in range(2, last_row):
        if ws.cell(row=row, column=1).value == date:
            print(f"[스킵] {date} 데이터 이미 존재")
            return

    quotes = {q['symbol']: q['price'] for q in report.get('quotes', [])}
    indicators = {i['series_id']: i['value'] for i in report.get('economic_indicators', [])}

    row_data = [
        date,
        quotes.get('VIX', 0),
        quotes.get('MOVE', 0),
        quotes.get('GOLD', 0),
        quotes.get('EUR_USD', 0),
        quotes.get('USD_JPY', 0),
        quotes.get('NASDAQ', 0),
        quotes.get('SP500', 0),
        quotes.get('BTC', 0),
        report.get('sofr_current', 0),
        indicators.get('DGS10', 0),
        indicators.get('DGS2', 0),
        indicators.get('T10Y2Y', 0)
    ]

    for col, value in enumerate(row_data, 1):
        cell = ws.cell(row=last_row, column=col, value=value)
        cell.border = thin_border
        if col > 1 and isinstance(value, (int, float)):
            cell.number_format = '#,##0.00' if col in [4, 5, 6, 7, 8, 9] else '0.00'

    wb.save(HISTORY_FILE)
    print(f"[누적] 히스토리: {HISTORY_FILE}")


def export_to_image(report: Dict, outlook: Dict = None) -> str:
    """
    이미지로 내보내기 (분할 저장 - 날짜별 폴더)
    - 1페이지: 시세표 + 차트
    - 2페이지~: 시황 (섹션별 분할)
    """
    import matplotlib.pyplot as plt

    plt.rcParams['font.family'] = 'AppleGothic'
    plt.rcParams['axes.unicode_minus'] = False

    date = report.get('date', datetime.now().strftime('%Y-%m-%d'))
    quotes = report.get('quotes', [])

    # 날짜별 폴더 생성
    date_dir = EXPORT_DIR / date
    date_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    # ===== 1페이지: 시세표 + 차트 =====
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), dpi=120)
    fig.suptitle(f'일일 경제 보고서 - {date}', fontsize=18, fontweight='bold', y=0.98)

    # 시세표
    ax1 = axes[0]
    ax1.axis('off')

    table_data = []
    for i, q in enumerate(quotes, 1):
        price = f"{q['price']:,.2f}" if q['price'] else "-"
        change = f"{q['change_pct']:+.2f}%" if q.get('change_pct') else "-"
        table_data.append([str(i), q['name'], price, change])

    if table_data:
        table = ax1.table(
            cellText=table_data,
            colLabels=['#', '항목', '가격', '변동'],
            cellLoc='center',
            loc='center',
            colWidths=[0.08, 0.45, 0.25, 0.15]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(16)
        table.scale(1.2, 2.4)

        for i in range(4):
            table[(0, i)].set_facecolor('#2F5496')
            table[(0, i)].set_text_props(color='white', fontweight='bold')
        for i in range(1, len(table_data) + 1):
            for j in range(4):
                table[(i, j)].set_facecolor('#F8F9FA' if i % 2 == 0 else 'white')

    # SOFR 차트
    ax2 = axes[1]
    sofr_trend = report.get('sofr_trend', [])
    if sofr_trend:
        dates_sofr = [t['date'][-5:] for t in sofr_trend]
        values_sofr = [t['rate'] for t in sofr_trend]
        ax2.plot(dates_sofr, values_sofr, 'b-o', linewidth=2, markersize=8)
        ax2.set_title(f'SOFR 추이 (현재: {report.get("sofr_current", 0):.2f}%)', fontweight='bold', fontsize=14)
        ax2.set_ylabel('%', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(labelsize=10)
        if values_sofr:
            ax2.set_ylim([min(values_sofr) - 0.03, max(values_sofr) + 0.03])

    # MOVE 차트
    ax3 = axes[2]
    move_trend = report.get('move_trend', [])
    if move_trend:
        dates_move = [t['date'][-5:] for t in move_trend]
        values_move = [t['value'] for t in move_trend]
        ax3.plot(dates_move, values_move, 'r-o', linewidth=2, markersize=8)
        ax3.set_title(f'MOVE Index 추이 (현재: {report.get("move_current", 0):.1f})', fontweight='bold', fontsize=14)
        ax3.set_ylabel('Index', fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(labelsize=10)
        if values_move:
            ax3.set_ylim([min(values_move) - 2, max(values_move) + 2])

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.figtext(0.5, 0.01, '출처: Yahoo Finance, CoinGecko, NY Fed, FRED', ha='center', fontsize=8, color='gray')

    page1_file = date_dir / "01_시세표_차트.png"
    plt.savefig(page1_file, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    saved_files.append(str(page1_file))
    print(f"[저장] {page1_file.name}")

    # ===== 2~3페이지: 시황 (2장으로 분할) =====
    if outlook:
        outlook_text = outlook.get('text', '')
        outlook_text = outlook_text.replace('$', '\\$')

        # 텍스트를 섹션별로 분할 (## 기준)
        sections = outlook_text.split('\n## ')
        if sections[0].startswith('## '):
            sections[0] = sections[0][3:]

        # "섹터별 동향"까지 2페이지, "종목별 상세 분석"부터 3페이지
        split_point = 0
        for i, sec in enumerate(sections):
            if sec.startswith('종목별 상세 분석') or sec.startswith('종목별'):
                split_point = i
                break
        if split_point == 0:
            split_point = max(1, int(len(sections) * 0.55))  # 폴백: 55%

        page1_sections = sections[:split_point]
        page2_sections = sections[split_point:]

        # 페이지 1 시황
        page1_text = '## ' + '\n## '.join(page1_sections)
        fig, ax = plt.subplots(figsize=(10, 14), dpi=120)
        ax.axis('off')
        ax.text(0.03, 0.97, page1_text, fontsize=11, ha='left', va='top',
                transform=ax.transAxes, family='AppleGothic',
                linespacing=1.25, fontweight='normal')
        ax.set_title(f'경제 시황 (1/2) - {date}', fontsize=18, fontweight='bold', pad=10)
        plt.figtext(0.5, 0.01, '출처: Yahoo Finance, CoinGecko, NY Fed, FRED | 투자 조언 아님', ha='center', fontsize=9, color='gray')

        page2_file = date_dir / "02_시황_1.png"
        plt.savefig(page2_file, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close()
        saved_files.append(str(page2_file))
        print(f"[저장] {page2_file.name}")

        # 페이지 2 시황 (나머지)
        if page2_sections:
            page2_text = '## ' + '\n## '.join(page2_sections)
            fig, ax = plt.subplots(figsize=(10, 14), dpi=120)
            ax.axis('off')
            ax.text(0.03, 0.97, page2_text, fontsize=11, ha='left', va='top',
                    transform=ax.transAxes, family='AppleGothic',
                    linespacing=1.25, fontweight='normal')
            ax.set_title(f'경제 시황 (2/2) - {date}', fontsize=18, fontweight='bold', pad=10)
            plt.figtext(0.5, 0.01, '출처: Yahoo Finance, CoinGecko, NY Fed, FRED | 투자 조언 아님', ha='center', fontsize=9, color='gray')

            page3_file = date_dir / "03_시황_2.png"
            plt.savefig(page3_file, bbox_inches='tight', facecolor='white', edgecolor='none')
            plt.close()
            saved_files.append(str(page3_file))
            print(f"[저장] {page3_file.name}")

    print(f"[완료] {len(saved_files)}개 이미지 → {date_dir}")
    return str(date_dir)


def export_to_pdf(report: Dict, outlook: Dict = None) -> str:
    """
    PDF 파일로 내보내기 (시황 보고서)
    """
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    # 한글 폰트 등록
    font_path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    try:
        pdfmetrics.registerFont(TTFont('AppleGothic', font_path, subfontIndex=0))
        font_name = 'AppleGothic'
    except:
        font_name = 'Helvetica'

    date = report.get('date', datetime.now().strftime('%Y-%m-%d'))
    pdf_file = EXPORT_DIR / f"daily_report_{date}.pdf"

    doc = SimpleDocTemplate(
        str(pdf_file),
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    # 스타일 정의
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='KoreanTitle',
        fontName=font_name,
        fontSize=18,
        leading=22,
        spaceAfter=12,
        alignment=1  # 가운데 정렬
    ))
    styles.add(ParagraphStyle(
        name='KoreanHeading',
        fontName=font_name,
        fontSize=12,
        leading=16,
        spaceAfter=6,
        spaceBefore=12,
        textColor=colors.HexColor('#2F5496')
    ))
    styles.add(ParagraphStyle(
        name='KoreanBody',
        fontName=font_name,
        fontSize=9,
        leading=13,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name='KoreanSmall',
        fontName=font_name,
        fontSize=8,
        leading=10,
        textColor=colors.gray
    ))

    story = []

    # 제목
    story.append(Paragraph(f"일일 경제 시황 보고서", styles['KoreanTitle']))
    story.append(Paragraph(f"{date}", styles['KoreanSmall']))
    story.append(Spacer(1, 10*mm))

    # 시세표
    story.append(Paragraph("시세표", styles['KoreanHeading']))
    quotes = report.get('quotes', [])
    if quotes:
        table_data = [['항목', '가격', '변동']]
        for q in quotes:
            price = f"{q['price']:,.2f}" if q['price'] else "-"
            change = f"{q['change_pct']:+.2f}%" if q.get('change_pct') else "-"
            table_data.append([q['name'], price, change])

        table = Table(table_data, colWidths=[80*mm, 40*mm, 30*mm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F5496')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')])
        ]))
        story.append(table)
    story.append(Spacer(1, 8*mm))

    # 시황
    if outlook:
        story.append(Paragraph("경제 시황 및 전망", styles['KoreanHeading']))

        outlook_text = outlook.get('text', '')
        # 마크다운 헤더 변환
        for line in outlook_text.split('\n'):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 2*mm))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], styles['KoreanHeading']))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], styles['KoreanHeading']))
            elif line.startswith('# '):
                story.append(Paragraph(line[2:], styles['KoreanHeading']))
            elif line.startswith('---'):
                story.append(Spacer(1, 3*mm))
            elif line.startswith('**') and line.endswith('**'):
                story.append(Paragraph(f"<b>{line[2:-2]}</b>", styles['KoreanBody']))
            elif line.startswith('- '):
                story.append(Paragraph(f"• {line[2:]}", styles['KoreanBody']))
            elif line.startswith('  - '):
                story.append(Paragraph(f"    ◦ {line[4:]}", styles['KoreanBody']))
            else:
                # HTML 특수문자 이스케이프
                line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(line, styles['KoreanBody']))

        story.append(Spacer(1, 5*mm))
        story.append(Paragraph(
            f"생성: {outlook.get('model', 'N/A')} | {outlook.get('timestamp', '')[:19]}",
            styles['KoreanSmall']
        ))

    # 푸터
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph(
        "출처: Yahoo Finance, CoinGecko, NY Fed, FRED | 본 보고서는 정보 제공 목적이며 투자 조언이 아닙니다.",
        styles['KoreanSmall']
    ))

    doc.build(story)
    print(f"[저장] PDF: {pdf_file}")
    return str(pdf_file)


def export_all(report: Dict = None, outlook: Dict = None) -> Dict[str, str]:
    """모든 형식으로 내보내기 (Excel 1개 + 이미지 1개)"""
    if report is None:
        report = load_report_json()

    if not report:
        print("[에러] 보고서 데이터 없음")
        return {}

    # 시황 로드 (없으면 None)
    if outlook is None:
        outlook = load_outlook(report.get('date'))

    results = {}
    date = report.get('date', 'Unknown')

    print(f"\n[내보내기] {date} 보고서")

    # Excel (5개 시트 통합)
    try:
        results['excel'] = export_to_excel(report, outlook)
    except Exception as e:
        print(f"[에러] Excel 내보내기 실패: {e}")

    # 통합 이미지 (시세표 + 차트 + 시황)
    try:
        results['image'] = export_to_image(report, outlook)
    except Exception as e:
        print(f"[에러] 이미지 내보내기 실패: {e}")

    # PDF
    try:
        results['pdf'] = export_to_pdf(report, outlook)
    except Exception as e:
        print(f"[에러] PDF 내보내기 실패: {e}")
        import traceback
        traceback.print_exc()

    print(f"\n[완료] 내보내기 {len(results)}개 파일")
    for name, path in results.items():
        print(f"  - {name}: {path}")

    return results


# CLI 실행
if __name__ == "__main__":
    import sys

    date = sys.argv[1] if len(sys.argv) > 1 else None
    report = load_report_json(date)

    if report:
        outlook = load_outlook(report.get('date'))
        export_all(report, outlook)
    else:
        print(f"보고서 없음: {date or '오늘'}")
