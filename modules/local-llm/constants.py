"""로컬 LLM 상수 정의."""
from pathlib import Path

MODULE_DIR = Path(__file__).parent
MODELS_DIR = MODULE_DIR / "models"

AVAILABLE_MODELS = {
    "qwen2.5-3b": "mlx-community/Qwen2.5-3B-Instruct-4bit",
    "qwen2.5-7b": "mlx-community/Qwen2.5-7B-Instruct-4bit",
}

MODEL_STRATEGY = {
    "always_loaded": ["qwen2.5-3b"],
    "on_demand": ["qwen2.5-7b"],
    "cache_timeout_minutes": 30,
    "max_concurrent_models": 2,
}

DEFAULT_MODEL = "qwen2.5-7b"
IDLE_UNLOAD_MINUTES = 5
