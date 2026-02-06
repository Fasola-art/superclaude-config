"""로컬 LLM 서브에이전트 타입 정의."""
from dataclasses import dataclass
from typing import Literal, Any
from enum import Enum

class ModelSize(Enum):
    SMALL = "3b"
    MEDIUM = "7b"

@dataclass(frozen=True, slots=True)
class ModelConfig:
    name: str
    size: ModelSize
    quantization: str
    vram_gb: float

@dataclass
class InferenceRequest:
    prompt: str
    model: str
    max_tokens: int = 512
    temperature: float = 0.7

@dataclass
class InferenceResponse:
    text: str
    model: str
    tokens_used: int
    latency_ms: float
