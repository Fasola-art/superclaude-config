#!/usr/bin/env python3
"""
8-Stage Quality Verification Hook
- Execute quality gates after code changes
- Syntax -> Type -> Lint -> Security -> Test -> Performance -> Docs -> Integration
"""

import os
import json
from pathlib import Path
from datetime import datetime

QUALITY_GATES = [
    {"name": "Syntax", "cmd": "check_syntax", "weight": 0.15},
    {"name": "Type", "cmd": "check_types", "weight": 0.15},
    {"name": "Lint", "cmd": "check_lint", "weight": 0.10},
    {"name": "Security", "cmd": "check_security", "weight": 0.20},
    {"name": "Test", "cmd": "run_tests", "weight": 0.15},
    {"name": "Performance", "cmd": "check_perf", "weight": 0.10},
    {"name": "Docs", "cmd": "check_docs", "weight": 0.05},
    {"name": "Integration", "cmd": "check_integration", "weight": 0.10},
]

STATE_FILE = Path.home() / ".claude" / "cache" / "quality-state.json"

def get_file_type(file_path: str) -> str:
    """Detect file type"""
    ext = Path(file_path).suffix.lower()
    type_map = {
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
        ".py": "python",
        ".go": "go",
        ".rs": "rust",
    }
    return type_map.get(ext, "unknown")

def suggest_gates(file_path: str, file_type: str) -> list:
    """Suggest gates based on file type"""
    suggestions = []

    if file_type == "typescript":
        suggestions = [
            "npx tsc --noEmit",
            "npx eslint " + file_path,
            "npx vitest run --reporter=verbose"
        ]
    elif file_type == "python":
        suggestions = [
            "python -m py_compile " + file_path,
            "python -m pylint " + file_path,
            "python -m pytest"
        ]

    return suggestions

def main():
    tool_name = os.environ.get("TOOL_NAME", "")
    file_path = os.environ.get("FILE_PATH", "")

    # Only run for Write/Edit tools
    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        return

    if not file_path:
        return

    file_type = get_file_type(file_path)

    if file_type == "unknown":
        return

    # Quality gate state
    state = {
        "file": file_path,
        "type": file_type,
        "timestamp": datetime.now().isoformat(),
        "gates": {g["name"]: "pending" for g in QUALITY_GATES}
    }

    # 1-line notification
    print(f"QG:{file_type} -> type 'verify' to run checks")

    # Save state
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    main()
