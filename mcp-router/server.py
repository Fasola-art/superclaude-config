#!/usr/bin/env python3
"""
MCP Router Server
SuperClaude v2.0.9 MCP 라우터

Mac Studio Ultra M2 최적화
- 24 CPU 코어 활용
- 동적 로드 밸런싱
- 서버 상태 모니터링
- 실제 MCP 프로토콜 지원
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import signal

# MCP 프로토콜 임포트
from mcp_protocol import MCPProtocolManager, create_manager_from_config

# 설정
CLAUDE_DIR = Path.home() / '.claude'
CONFIG_FILE = CLAUDE_DIR / 'mcp.json'
ROUTER_LOG_DIR = CLAUDE_DIR / 'logs' / 'mcp-router'
ROUTER_SOCKET = CLAUDE_DIR / 'mcp-router' / 'router.sock'

# 로깅 설정
ROUTER_LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(ROUTER_LOG_DIR / 'router.log')
    ]
)
logger = logging.getLogger('mcp-router')


class ServerStatus(Enum):
    UNKNOWN = 'unknown'
    HEALTHY = 'healthy'
    DEGRADED = 'degraded'
    UNHEALTHY = 'unhealthy'
    OFFLINE = 'offline'


@dataclass
class ServerConfig:
    name: str
    command: str
    args: List[str]
    env: Dict[str, str]
    priority: int = 0
    timeout: int = 30000
    maxRetries: int = 3
    healthCheck: Optional[str] = None
    enabled: bool = True


@dataclass
class ServerState:
    name: str
    status: ServerStatus
    lastCheck: str
    responseTime: float
    errorCount: int
    successCount: int
    tools: List[str] = None

    def __post_init__(self):
        if self.tools is None:
            self.tools = []


class MCPRouter:
    """MCP 서버 라우터 (프로토콜 통합)"""

    def __init__(self):
        self.servers: Dict[str, ServerConfig] = {}
        self.states: Dict[str, ServerState] = {}
        self.protocol_manager: Optional[MCPProtocolManager] = None
        self.load_balancer = LoadBalancer()
        self.config = self._load_config()
        self._init_servers()

    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        if CONFIG_FILE.exists():
            try:
                return json.loads(CONFIG_FILE.read_text())
            except Exception as e:
                logger.error(f"설정 로드 실패: {e}")
        return {'mcpServers': {}}

    def _init_servers(self):
        """서버 설정 초기화"""
        mcp_servers = self.config.get('mcpServers', {})

        for name, config in mcp_servers.items():
            self.servers[name] = ServerConfig(
                name=name,
                command=config.get('command', ''),
                args=config.get('args', []),
                env=config.get('env', {}),
                priority=config.get('priority', 0),
                timeout=config.get('timeout', 30000),
                maxRetries=config.get('maxRetries', 3),
                healthCheck=config.get('healthCheck'),
                enabled=config.get('enabled', True)
            )

            self.states[name] = ServerState(
                name=name,
                status=ServerStatus.UNKNOWN,
                lastCheck=datetime.now().isoformat(),
                responseTime=0.0,
                errorCount=0,
                successCount=0
            )

        logger.info(f"{len(self.servers)}개 MCP 서버 설정 로드됨")

    async def start(self):
        """라우터 시작 (MCP 서버들 연결)"""
        logger.info("MCP Router 시작 중...")

        self.protocol_manager = await create_manager_from_config(CONFIG_FILE)

        # 상태 업데이트
        status = self.protocol_manager.get_status()
        for name, server_status in status.get('servers', {}).items():
            if name in self.states:
                self.states[name].status = (
                    ServerStatus.HEALTHY if server_status['initialized']
                    else ServerStatus.UNHEALTHY
                )
                self.states[name].tools = server_status.get('tools', [])
                self.states[name].lastCheck = datetime.now().isoformat()

        logger.info("MCP Router 시작 완료")

    async def stop(self):
        """라우터 중지"""
        if self.protocol_manager:
            await self.protocol_manager.shutdown()
        logger.info("MCP Router 중지됨")

    async def health_check(self, server_name: str) -> ServerStatus:
        """서버 상태 체크"""
        if server_name not in self.states:
            return ServerStatus.UNKNOWN

        state = self.states[server_name]
        start_time = datetime.now()

        try:
            if self.protocol_manager and server_name in self.protocol_manager.connections:
                conn = self.protocol_manager.connections[server_name]
                if conn.initialized and conn.process and conn.process.returncode is None:
                    state.status = ServerStatus.HEALTHY
                    state.successCount += 1
                else:
                    state.status = ServerStatus.OFFLINE
            else:
                state.status = ServerStatus.OFFLINE

        except Exception as e:
            logger.error(f"헬스체크 실패 [{server_name}]: {e}")
            state.status = ServerStatus.UNHEALTHY
            state.errorCount += 1

        state.lastCheck = datetime.now().isoformat()
        state.responseTime = (datetime.now() - start_time).total_seconds() * 1000

        return state.status

    async def check_all_servers(self):
        """모든 서버 상태 체크"""
        tasks = [self.health_check(name) for name in self.servers]
        await asyncio.gather(*tasks)

    def get_best_server(self, capability: str) -> Optional[str]:
        """요청에 적합한 서버 선택"""
        # 라우팅 규칙 확인
        routing = self.config.get('routing', {})
        rules = routing.get('rules', [])

        import re
        for rule in rules:
            pattern = rule.get('pattern', '')
            if re.search(pattern, capability, re.IGNORECASE):
                server = rule.get('server')
                if server in self.states and self.states[server].status == ServerStatus.HEALTHY:
                    return server

        # 기본 로드 밸런서 사용
        return self.load_balancer.select(self.servers, self.states, capability)

    async def call_tool(self, tool_name: str, arguments: Dict = None) -> Dict:
        """도구 호출"""
        if not self.protocol_manager:
            return {'success': False, 'error': 'Router not started'}

        start_time = datetime.now()
        result = await self.protocol_manager.call_tool(tool_name, arguments)

        # 메트릭 업데이트
        server_name = self.protocol_manager.tool_registry.get(tool_name)
        if server_name and server_name in self.states:
            state = self.states[server_name]
            state.responseTime = (datetime.now() - start_time).total_seconds() * 1000
            if result.get('success'):
                state.successCount += 1
            else:
                state.errorCount += 1

        return result

    async def route_request(self, request: Dict) -> Dict:
        """요청 라우팅"""
        action = request.get('action', '')

        if action == 'health_check':
            await self.check_all_servers()
            return {'success': True, 'status': 'healthy'}

        elif action == 'get_status':
            return {'success': True, 'data': self.get_status_report()}

        elif action == 'list_tools':
            tools = self.protocol_manager.list_all_tools() if self.protocol_manager else []
            return {'success': True, 'tools': tools}

        elif action == 'call':
            tool_name = request.get('tool')
            arguments = request.get('arguments', {})
            return await self.call_tool(tool_name, arguments)

        elif action == 'call_capability':
            capability = request.get('capability', '')
            params = request.get('params', {})

            server_name = self.get_best_server(capability)
            if not server_name:
                return {'success': False, 'error': f'서버 없음: {capability}'}

            # 해당 서버의 첫 번째 도구 호출 (또는 capability와 매칭되는 도구)
            if self.protocol_manager and server_name in self.protocol_manager.connections:
                conn = self.protocol_manager.connections[server_name]
                matching_tools = [t for t in conn.tools if capability.lower() in t.name.lower()]
                if matching_tools:
                    return await self.call_tool(matching_tools[0].name, params)

            return {'success': False, 'error': f'도구를 찾을 수 없음'}

        return {'success': False, 'error': f'알 수 없는 액션: {action}'}

    def get_status_report(self) -> Dict:
        """전체 상태 리포트"""
        return {
            'timestamp': datetime.now().isoformat(),
            'totalServers': len(self.servers),
            'healthyServers': sum(1 for s in self.states.values()
                                   if s.status == ServerStatus.HEALTHY),
            'totalTools': len(self.protocol_manager.tool_registry) if self.protocol_manager else 0,
            'servers': {
                name: {
                    'status': state.status.value,
                    'enabled': self.servers[name].enabled if name in self.servers else False,
                    'lastCheck': state.lastCheck,
                    'responseTime': state.responseTime,
                    'errorCount': state.errorCount,
                    'successCount': state.successCount,
                    'tools': state.tools
                }
                for name, state in self.states.items()
            }
        }


class LoadBalancer:
    """로드 밸런서"""

    def __init__(self):
        self.strategy = 'weighted_round_robin'
        self.current_index = 0

    def select(
        self,
        servers: Dict[str, ServerConfig],
        states: Dict[str, ServerState],
        capability: str
    ) -> Optional[str]:
        """서버 선택"""
        # 건강하고 활성화된 서버만 필터링
        healthy_servers = [
            name for name, state in states.items()
            if state.status in [ServerStatus.HEALTHY, ServerStatus.UNKNOWN]
            and servers.get(name, ServerConfig(name, '', [], {})).enabled
        ]

        if not healthy_servers:
            return None

        # 가중치 기반 라운드 로빈
        if self.strategy == 'weighted_round_robin':
            return self._weighted_round_robin(healthy_servers, servers)

        # 가장 낮은 지연시간
        if self.strategy == 'least_latency':
            return self._least_latency(healthy_servers, states)

        return healthy_servers[0]

    def _weighted_round_robin(
        self,
        healthy_servers: List[str],
        servers: Dict[str, ServerConfig]
    ) -> str:
        """가중치 기반 라운드 로빈"""
        sorted_servers = sorted(
            healthy_servers,
            key=lambda n: servers[n].priority if n in servers else 0,
            reverse=True
        )

        self.current_index = (self.current_index + 1) % len(sorted_servers)
        return sorted_servers[self.current_index]

    def _least_latency(
        self,
        healthy_servers: List[str],
        states: Dict[str, ServerState]
    ) -> str:
        """가장 낮은 지연시간 서버"""
        return min(
            healthy_servers,
            key=lambda n: states[n].responseTime if states[n].responseTime > 0 else float('inf')
        )


# ============ Unix 소켓 서버 ============

class RouterServer:
    """Unix 소켓 기반 라우터 서버"""

    def __init__(self, router: MCPRouter):
        self.router = router
        self.server: Optional[asyncio.Server] = None

    async def handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ):
        """클라이언트 요청 처리"""
        addr = writer.get_extra_info('peername')
        logger.debug(f"클라이언트 연결: {addr}")

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                try:
                    request = json.loads(data.decode().strip())
                    response = await self.router.route_request(request)
                except json.JSONDecodeError:
                    response = {'success': False, 'error': 'JSON 파싱 오류'}
                except Exception as e:
                    response = {'success': False, 'error': str(e)}

                writer.write((json.dumps(response) + '\n').encode())
                await writer.drain()

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"클라이언트 처리 오류: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        """서버 시작"""
        # 기존 소켓 파일 제거
        if ROUTER_SOCKET.exists():
            ROUTER_SOCKET.unlink()

        self.server = await asyncio.start_unix_server(
            self.handle_client,
            path=str(ROUTER_SOCKET)
        )

        logger.info(f"Unix 소켓 서버 시작: {ROUTER_SOCKET}")

    async def stop(self):
        """서버 중지"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()

        if ROUTER_SOCKET.exists():
            ROUTER_SOCKET.unlink()


# ============ 메인 ============

async def main():
    """메인 실행"""
    router = MCPRouter()
    server = RouterServer(router)

    # 시그널 핸들러
    loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        logger.info("종료 시그널 수신")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        # 라우터 시작
        await router.start()

        # 소켓 서버 시작
        await server.start()

        logger.info("MCP Router 실행 중...")
        logger.info(f"소켓: {ROUTER_SOCKET}")

        # 주기적 헬스체크
        while not stop_event.is_set():
            await router.check_all_servers()
            report = router.get_status_report()
            logger.info(
                f"상태: {report['healthyServers']}/{report['totalServers']} 서버, "
                f"{report['totalTools']}개 도구"
            )

            # 10초 대기 (또는 종료 시그널)
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=10.0)
            except asyncio.TimeoutError:
                pass

    finally:
        await server.stop()
        await router.stop()
        logger.info("MCP Router 종료 완료")


if __name__ == '__main__':
    asyncio.run(main())
