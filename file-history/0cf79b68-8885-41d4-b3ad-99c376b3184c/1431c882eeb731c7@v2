#!/usr/bin/env python3
"""
MCP Router Client
MCP 라우터와 통신하는 클라이언트 유틸리티
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

CLAUDE_DIR = Path.home() / '.claude'
ROUTER_SOCKET = CLAUDE_DIR / 'mcp-router' / 'router.sock'


class MCPClient:
    """MCP 라우터 클라이언트"""

    def __init__(self):
        self.connected = False
        self.reader = None
        self.writer = None

    async def connect(self) -> bool:
        """라우터에 연결"""
        try:
            # Unix 소켓 연결 (또는 TCP)
            self.reader, self.writer = await asyncio.open_unix_connection(
                str(ROUTER_SOCKET)
            )
            self.connected = True
            return True
        except Exception as e:
            print(f"연결 실패: {e}")
            return False

    async def disconnect(self):
        """연결 해제"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        self.connected = False

    async def send_request(self, request: Dict) -> Dict:
        """요청 전송"""
        if not self.connected:
            return {'success': False, 'error': '연결되지 않음'}

        try:
            # 요청 전송
            data = json.dumps(request).encode() + b'\n'
            self.writer.write(data)
            await self.writer.drain()

            # 응답 수신
            response_data = await self.reader.readline()
            return json.loads(response_data.decode())

        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def health_check(self) -> Dict:
        """라우터 상태 체크"""
        return await self.send_request({'action': 'health_check'})

    async def get_status(self) -> Dict:
        """전체 서버 상태 조회"""
        return await self.send_request({'action': 'get_status'})

    async def call_capability(
        self,
        capability: str,
        params: Optional[Dict] = None
    ) -> Dict:
        """특정 기능 호출"""
        return await self.send_request({
            'action': 'call',
            'capability': capability,
            'params': params or {}
        })


# 동기 래퍼 함수들
def quick_status() -> Dict:
    """빠른 상태 확인 (동기)"""
    async def _check():
        client = MCPClient()
        if await client.connect():
            result = await client.get_status()
            await client.disconnect()
            return result
        return {'error': '연결 실패'}

    return asyncio.run(_check())


def quick_call(capability: str, params: Optional[Dict] = None) -> Dict:
    """빠른 기능 호출 (동기)"""
    async def _call():
        client = MCPClient()
        if await client.connect():
            result = await client.call_capability(capability, params)
            await client.disconnect()
            return result
        return {'error': '연결 실패'}

    return asyncio.run(_call())


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("사용법: python client.py [status|call <capability> [params]]")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'status':
        result = quick_status()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif action == 'call':
        if len(sys.argv) < 3:
            print("capability를 지정해주세요")
            sys.exit(1)

        capability = sys.argv[2]
        params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
        result = quick_call(capability, params)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"알 수 없는 액션: {action}")
        sys.exit(1)
