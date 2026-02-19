"""jarvis/core/security.py - 보안 유틸리티 (55줄)"""
import re
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

SAFE_BASE_DIRS = [Path.home(), Path('/tmp')]

SENSITIVE_PATTERNS = [
    (r'(?i)(api[_-]?key|token|secret|password)[=:]\s*["\']?(\S+)', r'\1=[REDACTED]'),
    (r'(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*', 'Bearer [REDACTED]'),
    (r'(?i)(aws_secret_access_key|aws_access_key_id)[=:]\s*\S+', r'\1=[REDACTED]'),
]


def is_safe_path(path_str: str) -> bool:
    """경로 안전성 검증"""
    try:
        path = Path(path_str).resolve()
        return any(path.is_relative_to(base) for base in SAFE_BASE_DIRS)
    except (ValueError, RuntimeError, OSError):
        return False


def sanitize_file_path(path_str: Optional[str]) -> Optional[str]:
    """경로 정제 및 검증"""
    if not path_str or not isinstance(path_str, str):
        return None

    if '..' in path_str:
        logger.warning(f"Path traversal detected: {path_str[:50]}")
        return '[REDACTED]'

    sensitive = ('/etc', '/var', '/private/etc')
    if any(path_str.startswith(p) for p in sensitive):
        return '[REDACTED]'

    if not is_safe_path(path_str):
        return '[REDACTED]'

    return path_str


def mask_sensitive_data(text: str) -> str:
    """민감 정보 마스킹"""
    if not text:
        return ''
    result = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result
