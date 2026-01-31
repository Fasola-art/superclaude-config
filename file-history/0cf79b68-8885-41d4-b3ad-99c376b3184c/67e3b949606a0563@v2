#!/usr/bin/env python3
"""
세션 자동 스냅샷 Hook
- 중요 변경 시 스냅샷 생성
- 최대 10개 유지
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

SNAPSHOT_DIR = Path.home() / ".claude" / "shell-snapshots"
MAX_SNAPSHOTS = 10

def create_snapshot(tool_name: str, file_path: str = None):
    """스냅샷 생성"""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"{timestamp}_{tool_name}"

    snapshot_data = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "file": file_path,
        "cwd": os.getcwd()
    }

    # 스냅샷 메타데이터 저장
    snapshot_file = SNAPSHOT_DIR / f"{snapshot_name}.json"
    with open(snapshot_file, 'w') as f:
        json.dump(snapshot_data, f, indent=2)

    # 파일 백업 (Edit/Write인 경우)
    if file_path and os.path.exists(file_path):
        backup_dir = SNAPSHOT_DIR / snapshot_name
        backup_dir.mkdir(exist_ok=True)
        try:
            shutil.copy2(file_path, backup_dir / Path(file_path).name)
        except:
            pass

    cleanup_old_snapshots()

    return snapshot_name

def cleanup_old_snapshots():
    """오래된 스냅샷 정리"""
    snapshots = sorted(SNAPSHOT_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime)

    while len(snapshots) > MAX_SNAPSHOTS:
        oldest = snapshots.pop(0)
        oldest.unlink()

        # 관련 디렉토리도 삭제
        related_dir = SNAPSHOT_DIR / oldest.stem
        if related_dir.exists():
            shutil.rmtree(related_dir)

def main():
    tool_name = os.environ.get("TOOL_NAME", "unknown")
    file_path = os.environ.get("FILE_PATH", "")

    # 중요 도구에서만 스냅샷 생성
    important_tools = ["Edit", "Write", "MultiEdit", "Bash"]

    if tool_name in important_tools:
        snapshot = create_snapshot(tool_name, file_path if file_path else None)
        # 조용히 실행 (로그 출력 안함)

if __name__ == "__main__":
    main()
