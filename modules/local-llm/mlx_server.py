"""MLX 모델 추론 서버."""
import time
import json
from typing import Any

# 상대/절대 import 호환
try:
    from .model_manager import ModelManager
    from .cache import InferenceCache
    from .types import InferenceRequest, InferenceResponse
    from .constants import DEFAULT_MODEL
except ImportError:
    from model_manager import ModelManager
    from cache import InferenceCache
    from types import InferenceRequest, InferenceResponse
    from constants import DEFAULT_MODEL

class MLXServer:
    """MLX 기반 로컬 LLM 추론 서버."""

    def __init__(self):
        self.manager = ModelManager()
        self.cache = InferenceCache()

    def generate(self, request: InferenceRequest) -> InferenceResponse:
        """텍스트 생성."""
        from mlx_lm import generate as mlx_generate

        # 캐시 확인
        params = {"max_tokens": request.max_tokens, "temperature": request.temperature}
        cached = self.cache.get(request.prompt, request.model, params)
        if cached:
            return InferenceResponse(text=cached, model=request.model, tokens_used=0, latency_ms=0)

        start = time.time()
        model, tokenizer = self.manager.load_model(request.model)

        # 프롬프트 포맷팅
        messages = [{"role": "user", "content": request.prompt}]
        formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        output = mlx_generate(
            model, tokenizer, prompt=formatted,
            max_tokens=request.max_tokens, temp=request.temperature, verbose=False
        )

        latency = (time.time() - start) * 1000
        tokens = len(tokenizer.encode(output))

        self.cache.set(request.prompt, request.model, params, output)
        return InferenceResponse(text=output, model=request.model, tokens_used=tokens, latency_ms=latency)

    def health_check(self) -> dict:
        """서버 상태 확인."""
        return {
            "status": "healthy",
            "loaded_models": self.manager.loaded_models,
            "cache_size": self.cache.size,
        }

    def cleanup(self):
        """유휴 리소스 정리."""
        self.manager.cleanup_idle()


def main():
    """테스트 실행."""
    server = MLXServer()
    print(json.dumps(server.health_check(), indent=2))

    req = InferenceRequest(prompt="What is 2+2?", model=DEFAULT_MODEL, max_tokens=50)
    resp = server.generate(req)
    print(f"Response: {resp.text}")
    print(f"Latency: {resp.latency_ms:.1f}ms")


if __name__ == "__main__":
    main()
