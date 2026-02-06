"""MLX 모델 로딩/언로딩 관리자."""
import time
from typing import Any
from pathlib import Path
from threading import Lock

# 상대/절대 import 호환
try:
    from .constants import AVAILABLE_MODELS, MODEL_STRATEGY, IDLE_UNLOAD_MINUTES
except ImportError:
    from constants import AVAILABLE_MODELS, MODEL_STRATEGY, IDLE_UNLOAD_MINUTES

class ModelManager:
    """모델 로딩/언로딩을 관리하는 싱글톤 클래스."""

    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        self._loaded_models: dict[str, Any] = {}
        self._last_used: dict[str, float] = {}
        self._tokenizers: dict[str, Any] = {}

    def load_model(self, model_name: str) -> tuple[Any, Any]:
        """모델 로드. 이미 로드되어 있으면 캐시 반환."""
        from mlx_lm import load

        if model_name in self._loaded_models:
            self._last_used[model_name] = time.time()
            return self._loaded_models[model_name], self._tokenizers[model_name]

        self._check_concurrent_limit()
        repo_id = AVAILABLE_MODELS.get(model_name)
        if not repo_id:
            raise ValueError(f"Unknown model: {model_name}")

        model, tokenizer = load(repo_id)
        self._loaded_models[model_name] = model
        self._tokenizers[model_name] = tokenizer
        self._last_used[model_name] = time.time()
        return model, tokenizer

    def unload_model(self, model_name: str):
        """모델 언로드."""
        if model_name in self._loaded_models:
            del self._loaded_models[model_name]
            del self._tokenizers[model_name]
            del self._last_used[model_name]

    def cleanup_idle(self):
        """유휴 모델 정리."""
        now = time.time()
        timeout = IDLE_UNLOAD_MINUTES * 60
        always_loaded = set(MODEL_STRATEGY["always_loaded"])

        for name in list(self._loaded_models.keys()):
            if name not in always_loaded and now - self._last_used[name] > timeout:
                self.unload_model(name)

    def _check_concurrent_limit(self):
        """동시 로딩 제한 확인."""
        max_models = MODEL_STRATEGY["max_concurrent_models"]
        while len(self._loaded_models) >= max_models:
            self._unload_oldest()

    def _unload_oldest(self):
        """가장 오래된 온디맨드 모델 언로드."""
        always_loaded = set(MODEL_STRATEGY["always_loaded"])
        candidates = [(n, t) for n, t in self._last_used.items() if n not in always_loaded]
        if candidates:
            oldest = min(candidates, key=lambda x: x[1])[0]
            self.unload_model(oldest)

    @property
    def loaded_models(self) -> list[str]:
        return list(self._loaded_models.keys())
