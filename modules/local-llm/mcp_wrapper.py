"""MCP stdio 래퍼 - Claude Code와 로컬 LLM 연결."""
import sys
import json
from typing import Any

# 상대/절대 import 호환
try:
    from .mlx_server import MLXServer
    from .types import InferenceRequest
except ImportError:
    from mlx_server import MLXServer
    from types import InferenceRequest

class MCPWrapper:
    """MCP 프로토콜 기반 stdio 래퍼."""

    def __init__(self):
        self.server = MLXServer()
        self.tools = {
            "generate": self._handle_generate,
            "classify_news": self._handle_classify_news,
            "interpret_indicator": self._handle_interpret_indicator,
            "validate_signal": self._handle_validate_signal,
            "health": self._handle_health,
        }

    def run(self):
        """메인 루프 - stdin에서 JSON-RPC 요청 처리."""
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self._process_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                self._send_error(-32700, "Parse error")
            except Exception as e:
                self._send_error(-32603, str(e))

    def _process_request(self, request: dict) -> dict:
        """JSON-RPC 요청 처리."""
        method = request.get("method", "")
        params = request.get("params", {})
        req_id = request.get("id")

        if method == "initialize":
            return self._handle_initialize(req_id)
        elif method == "tools/list":
            return self._handle_list_tools(req_id)
        elif method == "tools/call":
            return self._handle_tool_call(req_id, params)
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

    def _handle_initialize(self, req_id) -> dict:
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "local-llm", "version": "1.0.0"},
            "capabilities": {"tools": {}},
        }}

    def _handle_list_tools(self, req_id) -> dict:
        tools = [
            {"name": "generate", "description": "로컬 LLM으로 텍스트 생성", "inputSchema": {"type": "object", "properties": {"prompt": {"type": "string"}, "model": {"type": "string"}, "max_tokens": {"type": "integer"}}}},
            {"name": "classify_news", "description": "뉴스 분류 및 감성 분석", "inputSchema": {"type": "object", "properties": {"headline": {"type": "string"}, "content": {"type": "string"}}}},
            {"name": "interpret_indicator", "description": "경제 지표 해석", "inputSchema": {"type": "object", "properties": {"indicator": {"type": "string"}, "value": {"type": "number"}, "previous": {"type": "number"}}}},
            {"name": "validate_signal", "description": "트레이딩 시그널 검증", "inputSchema": {"type": "object", "properties": {"signal": {"type": "object"}}}},
            {"name": "health", "description": "서버 상태 확인", "inputSchema": {"type": "object"}},
        ]
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools}}

    def _handle_tool_call(self, req_id, params: dict) -> dict:
        tool_name = params.get("name", "")
        args = params.get("arguments", {})
        if tool_name in self.tools:
            result = self.tools[tool_name](args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"}}

    def _handle_generate(self, args: dict) -> dict:
        req = InferenceRequest(prompt=args.get("prompt", ""), model=args.get("model", "qwen2.5-7b"), max_tokens=args.get("max_tokens", 512))
        resp = self.server.generate(req)
        return {"text": resp.text, "model": resp.model, "latency_ms": resp.latency_ms}

    def _handle_classify_news(self, args: dict) -> dict:
        prompt = f"Classify this news headline and provide sentiment (positive/negative/neutral) and category (macro/sector/company):\n\nHeadline: {args.get('headline', '')}\nContent: {args.get('content', '')[:500]}\n\nRespond in JSON format: {{\"sentiment\": \"...\", \"category\": \"...\", \"confidence\": 0.0-1.0}}"
        req = InferenceRequest(prompt=prompt, model="qwen2.5-3b", max_tokens=100)
        resp = self.server.generate(req)
        return {"result": resp.text, "model": resp.model}

    def _handle_interpret_indicator(self, args: dict) -> dict:
        prompt = f"Interpret this economic indicator:\n\nIndicator: {args.get('indicator')}\nCurrent: {args.get('value')}\nPrevious: {args.get('previous')}\n\nProvide brief analysis of impact on markets. Respond in JSON: {{\"interpretation\": \"...\", \"market_impact\": \"bullish/bearish/neutral\", \"confidence\": 0.0-1.0}}"
        req = InferenceRequest(prompt=prompt, model="qwen2.5-7b", max_tokens=200)
        resp = self.server.generate(req)
        return {"result": resp.text, "model": resp.model}

    def _handle_validate_signal(self, args: dict) -> dict:
        signal = args.get("signal", {})
        prompt = f"Validate this trading signal:\n\n{json.dumps(signal, indent=2)}\n\nAssess validity and suggest confidence adjustment. Respond in JSON: {{\"valid\": true/false, \"adjusted_confidence\": 0.0-1.0, \"reason\": \"...\"}}"
        req = InferenceRequest(prompt=prompt, model="qwen2.5-7b", max_tokens=150)
        resp = self.server.generate(req)
        return {"result": resp.text, "model": resp.model}

    def _handle_health(self, args: dict) -> dict:
        return self.server.health_check()

    def _send_error(self, code: int, message: str):
        print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": code, "message": message}}), flush=True)


if __name__ == "__main__":
    wrapper = MCPWrapper()
    wrapper.run()
