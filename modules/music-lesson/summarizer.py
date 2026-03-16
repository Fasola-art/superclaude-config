"""
Ollama 요약 모듈 (Qwen2.5-7B)
STT 결과를 음악 레슨 요약으로 변환

사용법:
    from summarizer import summarize_lesson

    summary = summarize_lesson("레슨 텍스트 내용...")
    print(summary["main_points"])
"""

from __future__ import annotations

import json
import requests
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"


@dataclass
class ConceptDetail:
    """개념 상세 설명"""
    name: str           # 개념 이름
    explanation: str    # 초보자용 설명


@dataclass
class LessonSummary:
    """레슨 요약 결과"""
    title: str                          # 레슨 제목 (자동 생성)
    date: str                           # 레슨 날짜
    key_concepts: List[str]             # 중요 개념 목록
    concept_details: List[ConceptDetail] # 개념별 상세 설명
    memorization_summary: str           # 암기용 요약
    raw_summary: str                    # 전체 요약 텍스트


def check_ollama() -> bool:
    """Ollama 서버 상태 체크"""
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


LESSON_SUMMARY_PROMPT = """[수업 녹음 내용]
{transcript}

---
위 수업 녹음을 분석하여 아래 형식으로 요약하라.
예시의 형식만 참고하고, 내용은 반드시 위 수업 녹음에서 추출하라.

[출력 형식]
# (수업 주제)

## 📌 중요 개념
- (수업에서 선생님이 강조한 핵심)
- (수업에서 나온 중요 포인트)
- (필요시 추가)

## 📖 개념별 상세 설명

### (수업에서 다룬 개념명)
(수업 내용 기반 3-4문장 설명. 선생님이 말한 예시 포함.)

### (수업에서 다룬 개념명)
(수업 내용 기반 설명)

## 🧠 암기용 요약

• (핵심 1)
• (핵심 2)
• (핵심 3)

---
*(전체 수업 2문장 요약)*

[필수 규칙]
- 반드시 한국어로만 작성
- 수업 녹음 내용을 기반으로 작성 (예시 복사 금지)
- "-다" 체 사용
"""


def summarize_lesson(
    transcript: str,
    lesson_date: Optional[str] = None
) -> LessonSummary:
    """
    레슨 녹음 텍스트를 요약 (마크다운 직접 출력)

    Args:
        transcript: STT 변환된 레슨 텍스트
        lesson_date: 레슨 날짜 (YYYY-MM-DD 형식, 없으면 오늘)

    Returns:
        LessonSummary: 구조화된 레슨 요약
    """
    from datetime import date

    # 날짜 설정
    if lesson_date is None:
        lesson_date = date.today().isoformat()

    # Ollama 서버 체크
    if not check_ollama():
        raise ConnectionError("Ollama 서버 연결 실패 (localhost:11434)")

    # 텍스트가 너무 길면 앞부분만 사용 (토큰 제한)
    max_chars = 8000
    if len(transcript) > max_chars:
        transcript = transcript[:max_chars] + "\n\n[...이하 생략...]"

    # Ollama 호출 (최대 2회 시도)
    response_text = ""
    for attempt in range(2):
        prompt = LESSON_SUMMARY_PROMPT.format(transcript=transcript)
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 2048, "temperature": 0.5}
            },
            timeout=180
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API 오류: {response.status_code}")

        response_text = response.json().get("response", "").strip()

        # 형식 검증: 필수 섹션 확인
        if "## 📌" in response_text and "## 📖" in response_text and "## 🧠" in response_text:
            break  # 형식 OK
        elif attempt == 0:
            print("  ⚠️ 형식 오류, 재시도...")

    # 제목 추출 시도
    title = "수업"
    lines = response_text.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    return LessonSummary(
        title=title,
        date=lesson_date,
        key_concepts=[],  # 마크다운에 포함됨
        concept_details=[],  # 마크다운에 포함됨
        memorization_summary="",  # 마크다운에 포함됨
        raw_summary=response_text  # 전체 마크다운 저장
    )


def format_summary_markdown(summary: LessonSummary) -> str:
    """요약을 마크다운 형식으로 변환"""
    # 마크다운이 이미 raw_summary에 있으면 날짜만 추가
    if summary.raw_summary and summary.raw_summary.startswith('#'):
        md = summary.raw_summary
        # 제목 다음에 날짜 삽입
        lines = md.split('\n')
        result = [lines[0], "", f"**날짜**: {summary.date}", ""]
        result.extend(lines[1:])
        return '\n'.join(result)

    # 기존 방식 (fallback)
    lines = [
        f"# {summary.title}",
        f"",
        f"**날짜**: {summary.date}",
        f"",
    ]

    if summary.key_concepts:
        lines.append("## 📌 중요 개념")
        for concept in summary.key_concepts:
            lines.append(f"- {concept}")
        lines.append("")

    if summary.concept_details:
        lines.append("## 📖 개념별 상세 설명")
        lines.append("")
        for detail in summary.concept_details:
            lines.append(f"### {detail.name}")
            lines.append(f"{detail.explanation}")
            lines.append("")

    if summary.memorization_summary:
        lines.append("## 🧠 암기용 요약")
        lines.append("")
        lines.append(summary.memorization_summary)
        lines.append("")

    if summary.raw_summary:
        lines.append("---")
        lines.append(f"*{summary.raw_summary}*")

    return "\n".join(lines)


if __name__ == "__main__":
    # 테스트용 샘플 텍스트
    sample_transcript = """
    오늘 레슨에서는 바흐의 인벤션 1번을 집중적으로 연습했습니다.
    특히 오른손과 왼손의 독립적인 움직임이 중요합니다.
    메트로놈 60으로 시작해서 천천히 템포를 올려보세요.
    다음 주까지 1페이지를 완성해 오시고, 손가락 번호를 꼭 확인하세요.
    """

    try:
        summary = summarize_lesson(sample_transcript)
        print(format_summary_markdown(summary))
    except Exception as e:
        print(f"❌ 오류: {e}")
