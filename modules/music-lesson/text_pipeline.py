"""
텍스트 기반 음악 레슨 파이프라인
클로바노트 텍스트 파일 → Claude 요약 → Notion 업로드

사용법:
    from text_pipeline import process_text_file

    result = process_text_file("/path/to/lesson.txt")
    print(result["notion_url"])
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from summarizer import summarize_lesson, LessonSummary, format_summary_markdown
from notion_uploader import upload_to_notion


@dataclass
class TextPipelineResult:
    """파이프라인 실행 결과"""
    text_path: str
    transcript: str
    summary: LessonSummary
    notion_url: str
    processed_at: str


def extract_date_from_filename(filename: str) -> Optional[str]:
    """
    파일명에서 날짜 추출

    지원 형식:
    - 2026-02-01_레슨.txt
    - 20260201_레슨.txt
    - 레슨_2026.02.01.txt
    """
    patterns = [
        r'(\d{4}-\d{2}-\d{2})',      # 2026-02-01
        r'(\d{4})(\d{2})(\d{2})',    # 20260201
        r'(\d{4})\.(\d{2})\.(\d{2})', # 2026.02.01
    ]

    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            groups = match.groups()
            if len(groups) == 1:
                return groups[0]
            else:
                return f"{groups[0]}-{groups[1]}-{groups[2]}"

    return None


def process_text_file(
    text_path: str | Path,
    lesson_date: Optional[str] = None,
    upload: bool = True,
    save_markdown: bool = True
) -> TextPipelineResult:
    """
    텍스트 파일에서 레슨 요약 생성 및 Notion 업로드

    Args:
        text_path: 텍스트 파일 경로
        lesson_date: 레슨 날짜 (없으면 파일명에서 추출 또는 오늘)
        upload: Notion 업로드 여부

    Returns:
        TextPipelineResult: 처리 결과
    """
    text_path = Path(text_path)

    if not text_path.exists():
        raise FileNotFoundError(f"파일 없음: {text_path}")

    print(f"📄 처리 시작: {text_path.name}")

    # 1. 텍스트 파일 읽기
    print("  [1/2] 텍스트 읽는 중...")
    with open(text_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    print(f"  ✓ 텍스트 로드 완료 ({len(transcript)}자)")

    # 날짜 추출
    if lesson_date is None:
        lesson_date = extract_date_from_filename(text_path.name)
    if lesson_date is None:
        lesson_date = datetime.now().strftime("%Y-%m-%d")

    # 2. Claude 요약
    print("  [2/2] Claude 요약 생성 중...")
    summary = summarize_lesson(transcript, lesson_date)
    print(f"  ✓ 요약 완료: {summary.title}")

    # 3. 마크다운 파일 저장 (옵션)
    if save_markdown:
        md_content = format_summary_markdown(summary)
        md_path = text_path.parent / f"{text_path.stem}_요약.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"  ✓ 요약 파일 저장: {md_path.name}")

    # 4. Notion 업로드 (옵션)
    notion_url = ""
    if upload:
        print("  [+] Notion 업로드 중...")
        notion_url = upload_to_notion(summary)
        print(f"  ✓ Notion 업로드 완료")

    print(f"✅ 처리 완료!")

    return TextPipelineResult(
        text_path=str(text_path),
        transcript=transcript,
        summary=summary,
        notion_url=notion_url,
        processed_at=datetime.now().isoformat()
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("사용법: python text_pipeline.py <텍스트 파일 경로> [레슨 날짜]")
        print("예시: python text_pipeline.py ~/클로바노트/레슨.txt 2026-02-01")
        sys.exit(1)

    text_file = sys.argv[1]
    lesson_date = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = process_text_file(text_file, lesson_date)

        print("\n" + "="*50)
        print(format_summary_markdown(result.summary))
        print("="*50)

        if result.notion_url:
            print(f"\n📎 Notion 페이지: {result.notion_url}")

    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)
