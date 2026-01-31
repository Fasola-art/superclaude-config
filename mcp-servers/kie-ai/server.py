#!/usr/bin/env python3
"""
Kie.ai MCP Server
- 영상, 이미지, 음악 생성 API 통합
"""

import asyncio
import json
import os
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# API 설정
API_BASE = "https://api.kie.ai"
API_KEY = os.environ.get("KIE_API_KEY", "")

server = Server("kie-ai")

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

async def api_request(method: str, endpoint: str, data: dict = None) -> dict:
    """API 요청 실행"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        url = f"{API_BASE}{endpoint}"
        if method == "GET":
            response = await client.get(url, headers=get_headers(), params=data)
        else:
            response = await client.post(url, headers=get_headers(), json=data)
        return response.json()

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="kie_check_credits",
            description="크레딧 잔액 확인",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="kie_generate_video",
            description="영상 생성 (Runway, Veo3, Sora 등)",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "모델명 (runway, veo3, sora2, wan2.5)",
                        "enum": ["runway", "veo3", "sora2", "wan2.5"]
                    },
                    "prompt": {
                        "type": "string",
                        "description": "영상 설명 프롬프트"
                    },
                    "image_url": {
                        "type": "string",
                        "description": "이미지 URL (image-to-video용, 선택)"
                    },
                    "duration": {
                        "type": "integer",
                        "description": "영상 길이 (초)",
                        "default": 5
                    }
                },
                "required": ["model", "prompt"]
            }
        ),
        Tool(
            name="kie_generate_image",
            description="이미지 생성 (Midjourney, Flux, 4o Image 등)",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "모델명",
                        "enum": ["4o-image", "flux-kontext", "midjourney"]
                    },
                    "prompt": {
                        "type": "string",
                        "description": "이미지 설명 프롬프트"
                    },
                    "aspect_ratio": {
                        "type": "string",
                        "description": "비율 (1:1, 16:9, 9:16 등)",
                        "default": "1:1"
                    }
                },
                "required": ["model", "prompt"]
            }
        ),
        Tool(
            name="kie_generate_music",
            description="음악 생성 (Suno)",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "음악 설명 또는 가사"
                    },
                    "style": {
                        "type": "string",
                        "description": "음악 스타일 (pop, rock, jazz 등)"
                    },
                    "title": {
                        "type": "string",
                        "description": "곡 제목"
                    },
                    "instrumental": {
                        "type": "boolean",
                        "description": "인스트루멘탈 여부",
                        "default": False
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="kie_check_task",
            description="작업 상태 확인",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "작업 ID"
                    },
                    "task_type": {
                        "type": "string",
                        "description": "작업 유형",
                        "enum": ["video", "image", "music"]
                    }
                },
                "required": ["task_id", "task_type"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "kie_check_credits":
            result = await api_request("GET", "/api/v1/chat/credit")
            return [TextContent(
                type="text",
                text=f"💰 크레딧 잔액: {json.dumps(result, ensure_ascii=False, indent=2)}"
            )]

        elif name == "kie_generate_video":
            model = arguments.get("model", "runway")
            prompt = arguments["prompt"]
            image_url = arguments.get("image_url")
            duration = arguments.get("duration", 5)

            # 모델별 엔드포인트
            endpoints = {
                "runway": "/api/v1/runway/generate",
                "veo3": "/api/v1/video/veo3/generate",
                "sora2": "/api/v1/video/sora2/generate",
                "wan2.5": "/api/v1/video/wan/generate"
            }

            data = {
                "prompt": prompt,
                "duration": duration
            }
            if image_url:
                data["image_url"] = image_url

            result = await api_request("POST", endpoints[model], data)
            return [TextContent(
                type="text",
                text=f"🎬 영상 생성 시작\n모델: {model}\ntask_id: {result.get('task_id', result)}\n\n`kie_check_task`로 상태 확인하세요."
            )]

        elif name == "kie_generate_image":
            model = arguments.get("model", "4o-image")
            prompt = arguments["prompt"]
            aspect_ratio = arguments.get("aspect_ratio", "1:1")

            endpoints = {
                "4o-image": "/api/v1/gpt4o-image/generate",
                "flux-kontext": "/api/v1/flux/kontext/generate",
                "midjourney": "/api/v1/midjourney/generate"
            }

            data = {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio
            }

            result = await api_request("POST", endpoints[model], data)
            return [TextContent(
                type="text",
                text=f"🖼️ 이미지 생성 시작\n모델: {model}\ntask_id: {result.get('task_id', result)}\n\n`kie_check_task`로 상태 확인하세요."
            )]

        elif name == "kie_generate_music":
            prompt = arguments["prompt"]
            style = arguments.get("style", "")
            title = arguments.get("title", "")
            instrumental = arguments.get("instrumental", False)

            data = {
                "prompt": prompt,
                "make_instrumental": instrumental
            }
            if style:
                data["style"] = style
            if title:
                data["title"] = title

            result = await api_request("POST", "/api/v1/generate", data)
            return [TextContent(
                type="text",
                text=f"🎵 음악 생성 시작\ntask_id: {result.get('task_id', result)}\n\n`kie_check_task`로 상태 확인하세요."
            )]

        elif name == "kie_check_task":
            task_id = arguments["task_id"]
            task_type = arguments["task_type"]

            endpoints = {
                "video": "/api/v1/runway/record-detail",
                "image": "/api/v1/gpt4o-image/record-info",
                "music": "/api/v1/generate/record-info"
            }

            result = await api_request("GET", endpoints[task_type], {"task_id": task_id})

            # 상태 파싱
            status = result.get("status", "unknown")
            output_url = result.get("output_url") or result.get("video_url") or result.get("audio_url")

            status_emoji = {"pending": "⏳", "processing": "🔄", "completed": "✅", "failed": "❌"}.get(status, "❓")

            text = f"{status_emoji} 상태: {status}"
            if output_url:
                text += f"\n📥 결과: {output_url}"

            return [TextContent(type="text", text=text)]

        else:
            return [TextContent(type="text", text=f"❌ 알 수 없는 도구: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"❌ 오류: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
