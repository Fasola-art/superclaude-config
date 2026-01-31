#!/usr/bin/env python3
"""
MCP Protocol Implementation
Model Context Protocol 실제 구현

MCP 스펙: https://modelcontextprotocol.io/
"""

import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger('mcp-protocol')


# ============ MCP 메시지 타입 ============

class MCPMessageType(Enum):
    """MCP 메시지 타입"""
    # 요청
    INITIALIZE = 'initialize'
    LIST_TOOLS = 'tools/list'
    CALL_TOOL = 'tools/call'
    LIST_RESOURCES = 'resources/list'
    READ_RESOURCE = 'resources/read'
    LIST_PROMPTS = 'prompts/list'
    GET_PROMPT = 'prompts/get'

    # 알림
    INITIALIZED = 'notifications/initialized'
    PROGRESS = 'notifications/progress'
    CANCELLED = 'notifications/cancelled'


@dataclass
class MCPRequest:
    """MCP 요청 메시지"""
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    method: str = ""
    params: Dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps({
            'jsonrpc': self.jsonrpc,
            'id': self.id,
            'method': self.method,
            'params': self.params
        })


@dataclass
class MCPResponse:
    """MCP 응답 메시지"""
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    result: Optional[Dict] = None
    error: Optional[Dict] = None

    @classmethod
    def from_json(cls, data: str) -> 'MCPResponse':
        parsed = json.loads(data)
        return cls(
            jsonrpc=parsed.get('jsonrpc', '2.0'),
            id=parsed.get('id'),
            result=parsed.get('result'),
            error=parsed.get('error')
        )


@dataclass
class MCPTool:
    """MCP 도구 정의"""
    name: str
    description: str
    inputSchema: Dict = field(default_factory=dict)


@dataclass
class MCPResource:
    """MCP 리소스 정의"""
    uri: str
    name: str
    description: Optional[str] = None
    mimeType: Optional[str] = None


# ============ MCP 서버 연결 ============

class MCPServerConnection:
    """단일 MCP 서버와의 연결 관리"""

    def __init__(self, name: str, command: str, args: List[str], env: Dict[str, str] = None):
        self.name = name
        self.command = command
        self.args = args
        self.env = env or {}
        self.process: Optional[asyncio.subprocess.Process] = None
        self.request_id = 0
        self.pending_requests: Dict[int, asyncio.Future] = {}
        self.tools: List[MCPTool] = []
        self.resources: List[MCPResource] = []
        self.initialized = False
        self._read_task: Optional[asyncio.Task] = None

    async def start(self) -> bool:
        """서버 프로세스 시작"""
        try:
            # 환경 변수 확장
            import os
            full_env = {**os.environ, **self.env}

            # 경로 확장
            expanded_args = [
                str(Path(arg).expanduser()) if arg.startswith('~') else arg
                for arg in self.args
            ]

            self.process = await asyncio.create_subprocess_exec(
                self.command,
                *expanded_args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=full_env
            )

            # 응답 읽기 태스크 시작
            self._read_task = asyncio.create_task(self._read_responses())

            # 초기화
            await self._initialize()

            logger.info(f"MCP 서버 시작됨: {self.name} (PID: {self.process.pid})")
            return True

        except Exception as e:
            logger.error(f"MCP 서버 시작 실패 [{self.name}]: {e}")
            return False

    async def stop(self):
        """서버 프로세스 중지"""
        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass

        if self.process:
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()

            self.process = None

        self.initialized = False
        logger.info(f"MCP 서버 중지됨: {self.name}")

    async def _send_request(self, method: str, params: Dict = None) -> MCPResponse:
        """요청 전송 및 응답 대기"""
        if not self.process or not self.process.stdin:
            raise ConnectionError(f"서버 연결 안됨: {self.name}")

        self.request_id += 1
        request = MCPRequest(
            id=self.request_id,
            method=method,
            params=params or {}
        )

        # Future 생성
        future = asyncio.get_event_loop().create_future()
        self.pending_requests[self.request_id] = future

        # 요청 전송
        message = request.to_json() + '\n'
        self.process.stdin.write(message.encode())
        await self.process.stdin.drain()

        logger.debug(f"[{self.name}] 요청 전송: {method}")

        # 응답 대기 (타임아웃 30초)
        try:
            response = await asyncio.wait_for(future, timeout=30.0)
            return response
        except asyncio.TimeoutError:
            del self.pending_requests[self.request_id]
            raise TimeoutError(f"요청 타임아웃: {method}")

    async def _read_responses(self):
        """응답 읽기 루프"""
        try:
            while self.process and self.process.stdout:
                line = await self.process.stdout.readline()
                if not line:
                    break

                try:
                    response = MCPResponse.from_json(line.decode().strip())

                    # 대기 중인 요청에 응답 전달
                    if response.id and response.id in self.pending_requests:
                        self.pending_requests[response.id].set_result(response)
                        del self.pending_requests[response.id]

                except json.JSONDecodeError:
                    logger.warning(f"[{self.name}] JSON 파싱 실패: {line}")

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"[{self.name}] 응답 읽기 오류: {e}")

    async def _initialize(self):
        """MCP 초기화 핸드셰이크"""
        response = await self._send_request('initialize', {
            'protocolVersion': '2024-11-05',
            'capabilities': {
                'roots': {'listChanged': True},
                'sampling': {}
            },
            'clientInfo': {
                'name': 'SuperClaude MCP Router',
                'version': '2.0.9'
            }
        })

        if response.error:
            raise RuntimeError(f"초기화 실패: {response.error}")

        # initialized 알림 전송
        await self._send_notification('notifications/initialized', {})

        self.initialized = True
        logger.info(f"[{self.name}] MCP 초기화 완료")

        # 도구 목록 가져오기
        await self.refresh_tools()

    async def _send_notification(self, method: str, params: Dict):
        """알림 전송 (응답 없음)"""
        if not self.process or not self.process.stdin:
            return

        message = json.dumps({
            'jsonrpc': '2.0',
            'method': method,
            'params': params
        }) + '\n'

        self.process.stdin.write(message.encode())
        await self.process.stdin.drain()

    async def refresh_tools(self):
        """도구 목록 새로고침"""
        response = await self._send_request('tools/list', {})

        if response.result and 'tools' in response.result:
            self.tools = [
                MCPTool(
                    name=t['name'],
                    description=t.get('description', ''),
                    inputSchema=t.get('inputSchema', {})
                )
                for t in response.result['tools']
            ]
            logger.info(f"[{self.name}] {len(self.tools)}개 도구 로드됨")

    async def call_tool(self, tool_name: str, arguments: Dict = None) -> Dict:
        """도구 호출"""
        response = await self._send_request('tools/call', {
            'name': tool_name,
            'arguments': arguments or {}
        })

        if response.error:
            return {
                'success': False,
                'error': response.error
            }

        return {
            'success': True,
            'result': response.result
        }

    async def list_resources(self) -> List[MCPResource]:
        """리소스 목록 조회"""
        response = await self._send_request('resources/list', {})

        if response.result and 'resources' in response.result:
            self.resources = [
                MCPResource(
                    uri=r['uri'],
                    name=r['name'],
                    description=r.get('description'),
                    mimeType=r.get('mimeType')
                )
                for r in response.result['resources']
            ]

        return self.resources

    async def read_resource(self, uri: str) -> Dict:
        """리소스 읽기"""
        response = await self._send_request('resources/read', {
            'uri': uri
        })

        if response.error:
            return {'success': False, 'error': response.error}

        return {
            'success': True,
            'contents': response.result.get('contents', [])
        }

    def get_status(self) -> Dict:
        """연결 상태 반환"""
        return {
            'name': self.name,
            'initialized': self.initialized,
            'pid': self.process.pid if self.process else None,
            'tools_count': len(self.tools),
            'tools': [t.name for t in self.tools]
        }


# ============ MCP 프로토콜 매니저 ============

class MCPProtocolManager:
    """MCP 프로토콜 통합 관리자"""

    def __init__(self):
        self.connections: Dict[str, MCPServerConnection] = {}
        self.tool_registry: Dict[str, str] = {}  # tool_name -> server_name

    async def add_server(
        self,
        name: str,
        command: str,
        args: List[str],
        env: Dict[str, str] = None
    ) -> bool:
        """서버 추가 및 시작"""
        connection = MCPServerConnection(name, command, args, env)

        if await connection.start():
            self.connections[name] = connection

            # 도구 레지스트리 업데이트
            for tool in connection.tools:
                self.tool_registry[tool.name] = name

            return True
        return False

    async def remove_server(self, name: str):
        """서버 제거"""
        if name in self.connections:
            await self.connections[name].stop()

            # 도구 레지스트리에서 제거
            self.tool_registry = {
                k: v for k, v in self.tool_registry.items()
                if v != name
            }

            del self.connections[name]

    async def call_tool(self, tool_name: str, arguments: Dict = None) -> Dict:
        """도구 호출 (자동 라우팅)"""
        # 도구가 어느 서버에 있는지 찾기
        server_name = self.tool_registry.get(tool_name)

        if not server_name:
            return {
                'success': False,
                'error': f'도구를 찾을 수 없음: {tool_name}'
            }

        connection = self.connections.get(server_name)
        if not connection or not connection.initialized:
            return {
                'success': False,
                'error': f'서버 연결 안됨: {server_name}'
            }

        return await connection.call_tool(tool_name, arguments)

    async def call_tool_on_server(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict = None
    ) -> Dict:
        """특정 서버의 도구 호출"""
        connection = self.connections.get(server_name)

        if not connection:
            return {
                'success': False,
                'error': f'서버를 찾을 수 없음: {server_name}'
            }

        return await connection.call_tool(tool_name, arguments)

    def list_all_tools(self) -> List[Dict]:
        """모든 서버의 도구 목록"""
        tools = []
        for name, conn in self.connections.items():
            for tool in conn.tools:
                tools.append({
                    'server': name,
                    'name': tool.name,
                    'description': tool.description
                })
        return tools

    def get_status(self) -> Dict:
        """전체 상태"""
        return {
            'timestamp': datetime.now().isoformat(),
            'servers': {
                name: conn.get_status()
                for name, conn in self.connections.items()
            },
            'total_tools': len(self.tool_registry),
            'tool_registry': dict(self.tool_registry)
        }

    async def shutdown(self):
        """모든 서버 종료"""
        for name in list(self.connections.keys()):
            await self.remove_server(name)


# ============ 유틸리티 함수 ============

async def create_manager_from_config(config_path: Path) -> MCPProtocolManager:
    """설정 파일에서 매니저 생성"""
    manager = MCPProtocolManager()

    if not config_path.exists():
        logger.warning(f"설정 파일 없음: {config_path}")
        return manager

    config = json.loads(config_path.read_text())
    mcp_servers = config.get('mcpServers', {})

    for name, server_config in mcp_servers.items():
        if not server_config.get('enabled', True):
            logger.info(f"서버 비활성화됨: {name}")
            continue

        command = server_config.get('command', '')
        args = server_config.get('args', [])
        env = server_config.get('env', {})

        logger.info(f"서버 시작 중: {name}")
        success = await manager.add_server(name, command, args, env)

        if success:
            logger.info(f"서버 시작 성공: {name}")
        else:
            logger.error(f"서버 시작 실패: {name}")

    return manager


# ============ 테스트 ============

async def test_protocol():
    """프로토콜 테스트"""
    config_path = Path.home() / '.claude' / 'mcp.json'

    print("MCP 프로토콜 테스트")
    print("=" * 50)

    manager = await create_manager_from_config(config_path)

    print("\n서버 상태:")
    status = manager.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))

    print("\n등록된 도구:")
    tools = manager.list_all_tools()
    for tool in tools:
        print(f"  [{tool['server']}] {tool['name']}: {tool['description'][:50]}...")

    await manager.shutdown()
    print("\n테스트 완료")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_protocol())
