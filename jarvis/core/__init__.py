"""
jarvis/core - 공통 유틸리티 모듈 (35줄)
JARVIS 훅에서 사용하는 공통 기능 제공
"""
import logging
from typing import Dict

# 로거 캐시
_loggers: Dict[str, logging.Logger] = {}


def get_logger(name: str, level: int = logging.WARNING) -> logging.Logger:
    """캐시된 로거 반환"""
    if name in _loggers:
        return _loggers[name]
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)
    _loggers[name] = logger
    return logger


# 모듈 export
from .io import atomic_write_json, safe_load_json, ensure_dir
from .validation import safe_parse_input, safe_error_response, run_hook, MAX_INPUT_SIZE
from .security import is_safe_path, sanitize_file_path, mask_sensitive_data
from .parallel import run_parallel, run_with_timeout, TaskPool, parallel_async, parallel_sync

__all__ = [
    'get_logger',
    'atomic_write_json', 'safe_load_json', 'ensure_dir',
    'safe_parse_input', 'safe_error_response', 'run_hook', 'MAX_INPUT_SIZE',
    'is_safe_path', 'sanitize_file_path', 'mask_sensitive_data',
    'run_parallel', 'run_with_timeout', 'TaskPool', 'parallel_async', 'parallel_sync',
]
