"""
Claude Haiku 요약 모듈
STT 결과를 음악 레슨 요약으로 변환

사용법:
    from summarizer import summarize_lesson

    summary = summarize_lesson("레슨 텍스트 내용...")
    print(summary["main_points"])
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import anthropic


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


def load_api_key() -> str:
    """Anthropic API 키 로드"""
    key_path = Path.home() / ".claude" / "credentials" / "api-keys.json"
    if not key_path.exists():
        raise FileNotFoundError(f"API 키 파일 없음: {key_path}")

    with open(key_path) as f:
        keys = json.load(f)

    if "anthropic" not in keys:
        raise KeyError("anthropic 키가 api-keys.json에 없음")

    return keys["anthropic"]["api_key"]


LESSON_SUMMARY_PROMPT = """당신은 수업 내용을 학생이 복습하기 좋게 정리하는 전문가입니다.

다음 수업 녹음 텍스트를 분석하여 구조화된 요약을 작성해주세요.

## 지침

### 1. 중요 개념 (key_concepts)
- 단어가 아닌 **문장형**으로 작성
- 선생님이 강조한 핵심 멘트를 그대로 살려서 작성
- 예시: "선율은 도약보다 스케일로 연결해야 자연스럽다", "리스크 관리가 수익보다 중요하다"

### 2. 개념별 상세 설명 (concept_details)
- 수업에서 **실제 언급된 구체적인 예시, 비유, 설명**을 최대한 포함
- 딱딱한 교과서 문체가 아닌, 선생님이 설명하듯 **친절하고 구어체**로 작성
- 학생이 "아, 그때 그 얘기!" 하고 떠올릴 수 있게 **구체적으로** 작성
- 수업에서 언급한 **숫자, 퍼센트, 구체적 사례, 비유, 작품명, 용어**가 있다면 반드시 포함
- 각 설명은 **3-5문장 이상**으로 충분히 길게 작성
- "예를 들어...", "선생님 말씀으로는...", "실제로..." 같은 표현 활용

### 3. 암기용 요약 (memorization_summary)
- 핵심만 불릿 포인트로 정리
- 시험 직전에 훑어볼 수 있는 형태

## 출력 형식 (JSON)
{{
    "title": "수업 제목",
    "key_concepts": [
        "선생님이 강조한 핵심 멘트 1 (문장형)",
        "선생님이 강조한 핵심 멘트 2 (문장형)",
        "선생님이 강조한 핵심 멘트 3 (문장형)"
    ],
    "concept_details": [
        {{"name": "개념명", "explanation": "수업에서 언급한 구체적 예시와 함께 친절하게 설명. 선생님이 한 비유나 사례가 있다면 포함."}},
        {{"name": "개념명", "explanation": "디테일하고 구어체로 작성. '~하면 안 돼요', '~해야 해요' 같은 톤 사용 가능."}}
    ],
    "memorization_summary": "• 핵심1\\n• 핵심2\\n• 핵심3",
    "full_summary": "전체 수업 내용 2-3문장 요약"
}}

## 수업 녹음 텍스트
{transcript}
"""


def summarize_lesson(
    transcript: str,
    lesson_date: Optional[str] = None
) -> LessonSummary:
    """
    레슨 녹음 텍스트를 요약

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

    # API 키 로드
    api_key = load_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    # Claude 호출
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",  # Haiku 사용 (빠르고 저렴)
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": LESSON_SUMMARY_PROMPT.format(transcript=transcript)
            }
        ]
    )

    # 응답 파싱
    response_text = message.content[0].text

    # JSON 추출 (코드 블록 처리)
    json_str = response_text
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        json_str = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        json_str = response_text[json_start:json_end].strip()

    # JSON 객체 직접 추출 시도 (중괄호 기준)
    if not json_str.startswith("{"):
        start_idx = json_str.find("{")
        end_idx = json_str.rfind("}") + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = json_str[start_idx:end_idx]

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        # 파싱 실패 시 기본값 반환
        return LessonSummary(
            title="수업",
            date=lesson_date,
            key_concepts=["요약 생성 실패"],
            concept_details=[],
            memorization_summary="",
            raw_summary=response_text
        )

    # concept_details 파싱
    concept_details = []
    for item in data.get("concept_details", []):
        if isinstance(item, dict):
            concept_details.append(ConceptDetail(
                name=item.get("name", ""),
                explanation=item.get("explanation", "")
            ))

    return LessonSummary(
        title=data.get("title", "수업"),
        date=lesson_date,
        key_concepts=data.get("key_concepts", []),
        concept_details=concept_details,
        memorization_summary=data.get("memorization_summary", ""),
        raw_summary=data.get("full_summary", "")
    )


def format_summary_markdown(summary: LessonSummary) -> str:
    """요약을 마크다운 형식으로 변환"""
    lines = [
        f"# {summary.title}",
        f"",
        f"**날짜**: {summary.date}",
        f"",
    ]

    # 1. 중요 개념
    if summary.key_concepts:
        lines.append("## 📌 중요 개념")
        for concept in summary.key_concepts:
            lines.append(f"- {concept}")
        lines.append("")

    # 2. 개념별 상세 설명
    if summary.concept_details:
        lines.append("## 📖 개념별 상세 설명")
        lines.append("")
        for detail in summary.concept_details:
            lines.append(f"### {detail.name}")
            lines.append(f"{detail.explanation}")
            lines.append("")

    # 3. 암기용 요약
    if summary.memorization_summary:
        lines.append("## 🧠 암기용 요약")
        lines.append("")
        lines.append(summary.memorization_summary)
        lines.append("")

    # 전체 요약
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
