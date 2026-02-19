"""jarvis/core/validation.py - 입력 검증 및 훅 실행 (60줄)"""
import sys
import json
import logging
from typing import Any, Callable, Dict

logger = logging.getLogger(__name__)

MAX_INPUT_SIZE = 1024 * 1024  # 1MB

ALLOWED_KEYS = {
    'tool', 'status', 'file_path', 'command', 'exitCode',
    'taskId', 'subject', 'todos', 'stderr', 'path'
}


def safe_parse_input(raw_input: str) -> Dict[str, Any]:
    """stdin 입력 안전하게 파싱"""
    if len(raw_input) > MAX_INPUT_SIZE:
        raise ValueError("Input exceeds maximum size")
    if not raw_input.strip():
        return {}
    data = json.loads(raw_input)
    if not isinstance(data, dict):
        logger.warning(f"Expected dict, got {type(data).__name__}")
        return {}
    return {k: v for k, v in data.items() if k in ALLOWED_KEYS}


def safe_error_response(e: Exception) -> Dict[str, str]:
    """안전한 오류 응답 (내부 정보 숨김)"""
    logger.error(f"Error: {type(e).__name__}: {e}")
    error_map = {
        json.JSONDecodeError: "Invalid input format",
        ValueError: "Invalid value",
        FileNotFoundError: "Resource not found",
        PermissionError: "Access denied",
    }
    return {'status': 'error', 'message': error_map.get(type(e), "Processing error")}


def run_hook(processor: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
    """공통 훅 실행 패턴 - stdin 파싱 → 처리 → 출력"""
    try:
        data = safe_parse_input(sys.stdin.read())
        result = processor(data)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps(safe_error_response(e), ensure_ascii=False))
        sys.exit(1)
