"""
Notion 업로드 모듈
레슨 요약을 Notion 페이지로 생성

사용법:
    from notion_uploader import upload_to_notion
    from summarizer import LessonSummary

    page_url = upload_to_notion(summary)
    print(f"페이지 생성: {page_url}")
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import date
from typing import List, Dict, Optional

import requests

from summarizer import LessonSummary


def load_notion_config() -> Dict:
    """Notion 설정 로드"""
    key_path = Path.home() / ".claude" / "credentials" / "api-keys.json"
    if not key_path.exists():
        raise FileNotFoundError(f"API 키 파일 없음: {key_path}")

    with open(key_path) as f:
        keys = json.load(f)

    if "notion" not in keys:
        raise KeyError("notion 키가 api-keys.json에 없음")

    return keys["notion"]


def create_notion_blocks(summary: LessonSummary) -> List[Dict]:
    """
    LessonSummary를 Notion 블록 형식으로 변환

    Args:
        summary: 레슨 요약 데이터

    Returns:
        Notion API용 블록 리스트
    """
    blocks = []

    # 메타데이터 (콜아웃)
    meta_text = f"📅 날짜: {summary.date}"

    blocks.append({
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": meta_text}}],
            "icon": {"emoji": "📚"}
        }
    })

    # 구분선
    blocks.append({"object": "block", "type": "divider", "divider": {}})

    # 1. 중요 개념
    if summary.key_concepts:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📌 중요 개념"}}]
            }
        })
        for concept in summary.key_concepts:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": concept}}]
                }
            })

    # 2. 개념별 상세 설명
    if summary.concept_details:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📖 개념별 상세 설명"}}]
            }
        })
        for detail in summary.concept_details:
            # 개념 이름 (토글 헤더)
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": detail.name}}]
                }
            })
            # 설명
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": detail.explanation}}]
                }
            })

    # 3. 암기용 요약
    if summary.memorization_summary:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🧠 암기용 요약"}}]
            }
        })
        blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": summary.memorization_summary}}],
                "icon": {"emoji": "💡"}
            }
        })

    # 전체 요약 (인용)
    if summary.raw_summary:
        blocks.append({"object": "block", "type": "divider", "divider": {}})
        blocks.append({
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": [{"type": "text", "text": {"content": summary.raw_summary}}]
            }
        })

    return blocks


def upload_to_notion(
    summary: LessonSummary,
    parent_page_id: Optional[str] = None
) -> str:
    """
    레슨 요약을 Notion 페이지로 업로드

    Args:
        summary: 레슨 요약 데이터
        parent_page_id: 부모 페이지 ID (없으면 설정 파일에서 로드)

    Returns:
        생성된 페이지 URL
    """
    config = load_notion_config()
    secret = config["internal_secret"]

    if parent_page_id is None:
        parent_page_id = config["page_id"]

    # API 헤더
    headers = {
        "Authorization": f"Bearer {secret}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # 페이지 제목 생성
    page_title = f"[{summary.date}] {summary.title}"

    # 블록 생성
    blocks = create_notion_blocks(summary)

    # 페이지 생성 요청
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": page_title}}]
            }
        },
        "children": blocks
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    result = response.json()

    # 페이지 URL 반환
    page_id = result["id"]
    page_url = f"https://notion.so/{page_id.replace('-', '')}"

    return page_url


def get_page_info(page_id: str) -> dict:
    """페이지 정보 조회 (테스트용)"""
    config = load_notion_config()
    secret = config["internal_secret"]

    headers = {
        "Authorization": f"Bearer {secret}",
        "Notion-Version": "2022-06-28"
    }

    response = requests.get(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Notion 연결 테스트
    try:
        config = load_notion_config()
        page_id = config["page_id"]

        print("Notion 연결 테스트...")
        info = get_page_info(page_id)
        print(f"✅ 연결 성공!")
        print(f"페이지 ID: {page_id}")
        print(f"생성일: {info.get('created_time', 'N/A')}")
    except Exception as e:
        print(f"❌ 오류: {e}")
