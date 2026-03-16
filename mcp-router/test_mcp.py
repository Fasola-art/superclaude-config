#!/usr/bin/env python3
"""MCP 라우터 간단 테스트"""

import asyncio
import json
import sys
from pathlib import Path

# 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

from mcp_protocol import MCPServerConnection

async def test_single_server():
    """단일 서버 테스트"""
    print("=" * 50)
    print("MCP 서버 연결 테스트")
    print("=" * 50)

    # filesystem 서버 테스트
    conn = MCPServerConnection(
        name="filesystem",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem",
              "/Users/reim/Documents", "/Users/reim/.claude"]
    )

    print("\n[1] 서버 시작 중...")
    success = await conn.start()

    if not success:
        print("❌ 서버 시작 실패")
        return False

    print(f"✅ 서버 시작 성공 (PID: {conn.process.pid})")

    # 잠시 대기 (초기화 완료)
    await asyncio.sleep(2)

    print("\n[2] 서버 상태:")
    status = conn.get_status()
    print(f"  - initialized: {status['initialized']}")
    print(f"  - tools: {status['tools_count']}개")

    if status['tools']:
        print("\n[3] 사용 가능한 도구:")
        for tool in conn.tools:
            print(f"  - {tool.name}: {tool.description[:50]}...")

    # 도구 호출 테스트
    if conn.tools:
        print("\n[4] 도구 호출 테스트 (list_allowed_directories)...")
        result = await conn.call_tool("list_allowed_directories", {})
        print(f"  결과: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")

    # 정리
    print("\n[5] 서버 종료...")
    await conn.stop()
    print("✅ 테스트 완료")

    return True

if __name__ == '__main__':
    try:
        result = asyncio.run(test_single_server())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n중단됨")
        sys.exit(1)
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
