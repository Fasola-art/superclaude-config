#!/usr/bin/env python3
"""
Session Auto-Snapshot Hook
- Create snapshot on important changes
- Maintain maximum 10 snapshots
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

SNAPSHOT_DIR = Path.home() / ".claude" / "shell-snapshots"
MAX_SNAPSHOTS = 10

def create_snapshot(tool_name: str, file_path: str = None):
    """Create snapshot"""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"{timestamp}_{tool_name}"

    snapshot_data = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "file": file_path,
        "cwd": os.getcwd()
    }

    # Save snapshot metadata
    snapshot_file = SNAPSHOT_DIR / f"{snapshot_name}.json"
    with open(snapshot_file, 'w') as f:
        json.dump(snapshot_data, f, indent=2)

    # Backup file (for Edit/Write)
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
    """Clean up old snapshots"""
    snapshots = sorted(SNAPSHOT_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime)

    while len(snapshots) > MAX_SNAPSHOTS:
        oldest = snapshots.pop(0)
        oldest.unlink()

        # Delete related directory
        related_dir = SNAPSHOT_DIR / oldest.stem
        if related_dir.exists():
            shutil.rmtree(related_dir)

def main():
    tool_name = os.environ.get("TOOL_NAME", "unknown")
    file_path = os.environ.get("FILE_PATH", "")

    # Only create snapshots for important tools
    important_tools = ["Edit", "Write", "MultiEdit", "Bash"]

    if tool_name in important_tools:
        snapshot = create_snapshot(tool_name, file_path if file_path else None)
        # Run silently (no log output)

if __name__ == "__main__":
    main()
