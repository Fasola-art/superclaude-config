"""
음악 레슨 파이프라인 통합 모듈
녹음 파일 → STT → 요약 → Notion 업로드

사용법:
    from pipeline import process_lesson

    result = process_lesson("/path/to/lesson.mp3")
    print(result["notion_url"])
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

from clova_stt import transcribe_audio, STTResult
from summarizer import summarize_lesson, LessonSummary, format_summary_markdown
from notion_uploader import upload_to_notion


@dataclass
class PipelineResult:
    """파이프라인 실행 결과"""
    audio_path: str
    stt_result: STTResult
    summary: LessonSummary
    notion_url: str
    processed_at: str


def load_config() -> dict:
    """설정 파일 로드"""
    config_path = Path(__file__).parent / "config.json"

    if not config_path.exists():
        # 기본 설정 반환
        return {
            "language": "ko-KR",
            "notion_parent_page_id": None,
            "auto_upload": True,
            "save_transcript": True,
            "transcript_dir": str(Path.home() / ".claude" / "modules" / "music-lesson" / "transcripts")
        }

    with open(config_path) as f:
        return json.load(f)


def process_lesson(
    audio_path: Union[str, Path],
    lesson_date: Optional[str] = None,
    upload: bool = True
) -> PipelineResult:
    """
    음악 레슨 녹음 파일 전체 처리

    Args:
        audio_path: 오디오 파일 경로
        lesson_date: 레슨 날짜 (없으면 오늘)
        upload: Notion 업로드 여부

    Returns:
        PipelineResult: 처리 결과
    """
    audio_path = Path(audio_path)
    config = load_config()

    print(f"🎙️ 처리 시작: {audio_path.name}")

    # 1. STT 변환
    print("  [1/3] CLOVA STT 변환 중...")
    stt_result = transcribe_audio(
        audio_path,
        language=config.get("language", "ko-KR")
    )
    print(f"  ✓ STT 완료 ({len(stt_result['text'])}자)")

    # 트랜스크립트 저장 (옵션)
    if config.get("save_transcript", True):
        transcript_dir = Path(config.get(
            "transcript_dir",
            Path.home() / ".claude" / "modules" / "music-lesson" / "transcripts"
        ))
        transcript_dir.mkdir(parents=True, exist_ok=True)

        transcript_file = transcript_dir / f"{audio_path.stem}_transcript.txt"
        with open(transcript_file, "w") as f:
            f.write(stt_result["text"])
        print(f"  ✓ 트랜스크립트 저장: {transcript_file.name}")

    # 2. Claude 요약
    print("  [2/3] Claude 요약 생성 중...")
    summary = summarize_lesson(stt_result["text"], lesson_date)
    print(f"  ✓ 요약 완료: {summary.title}")

    # 3. Notion 업로드
    notion_url = ""
    if upload and config.get("auto_upload", True):
        print("  [3/3] Notion 업로드 중...")
        notion_url = upload_to_notion(
            summary,
            parent_page_id=config.get("notion_parent_page_id")
        )
        print(f"  ✓ Notion 업로드 완료")
    else:
        print("  [3/3] Notion 업로드 건너뜀")

    print(f"✅ 처리 완료!")

    return PipelineResult(
        audio_path=str(audio_path),
        stt_result=stt_result,
        summary=summary,
        notion_url=notion_url,
        processed_at=datetime.now().isoformat()
    )


def process_multiple(
    audio_paths: List[Union[str, Path]],
    lesson_date: Optional[str] = None
) -> List[PipelineResult]:
    """
    여러 오디오 파일 일괄 처리

    Args:
        audio_paths: 오디오 파일 경로 리스트
        lesson_date: 공통 레슨 날짜

    Returns:
        처리 결과 리스트
    """
    results = []

    for i, path in enumerate(audio_paths, 1):
        print(f"\n[{i}/{len(audio_paths)}] ", end="")
        try:
            result = process_lesson(path, lesson_date)
            results.append(result)
        except Exception as e:
            print(f"❌ 처리 실패: {path}")
            print(f"   오류: {e}")

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("사용법: python pipeline.py <오디오 파일 경로> [레슨 날짜]")
        print("예시: python pipeline.py ~/lesson.mp3 2026-02-01")
        sys.exit(1)

    audio_file = sys.argv[1]
    lesson_date = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = process_lesson(audio_file, lesson_date)

        print("\n" + "="*50)
        print(format_summary_markdown(result.summary))
        print("="*50)

        if result.notion_url:
            print(f"\n📎 Notion 페이지: {result.notion_url}")

    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)
