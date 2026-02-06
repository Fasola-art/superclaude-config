"""jarvis/core/io.py - 파일 I/O 유틸리티 (70줄)"""
import json
import os
import fcntl
import tempfile
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def ensure_dir(path: Path) -> None:
    """디렉토리 생성"""
    path.mkdir(parents=True, exist_ok=True)


def safe_load_json(
    path: Path,
    default: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """JSON 파일 안전하게 로드"""
    if default is None:
        default = {}

    if not path.exists():
        return default

    try:
        content = path.read_text(encoding='utf-8')
        data = json.loads(content)
        return data if isinstance(data, dict) else default

    except json.JSONDecodeError as e:
        backup = path.with_suffix('.json.corrupt')
        try:
            path.rename(backup)
            logger.warning(f"Corrupted JSON backed up: {backup}")
        except OSError:
            pass
        return default

    except (PermissionError, OSError) as e:
        logger.error(f"Cannot read {path}: {e}")
        return default


def atomic_write_json(
    path: Path,
    data: Dict[str, Any],
    mode: int = 0o600
) -> bool:
    """원자적 JSON 파일 쓰기"""
    ensure_dir(path.parent)

    try:
        fd, temp_path = tempfile.mkstemp(
            dir=path.parent, prefix='.tmp_', suffix='.json'
        )
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            os.chmod(temp_path, mode)
            os.replace(temp_path, path)
            return True
        except Exception:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    except (PermissionError, OSError) as e:
        logger.error(f"Cannot save {path}: {e}")
        return False
