#!/usr/bin/env python3
"""Auto-run related tests after changes"""
import subprocess
import sys
import json
import os
from pathlib import Path

def main():
    tool_result = os.environ.get('CLAUDE_TOOL_RESULT', '{}')

    try:
        result = json.loads(tool_result)
        file_path = result.get('filePath', '')

        if not file_path:
            return

        path = Path(file_path)

        # Python tests
        if file_path.endswith('.py'):
            test_file = path.parent / f"test_{path.name}"
            if test_file.exists():
                subprocess.run(['pytest', str(test_file), '-v', '--tb=short'], capture_output=True)

        # JavaScript/TypeScript tests
        elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            test_patterns = [
                path.with_suffix('.test' + path.suffix),
                path.with_suffix('.spec' + path.suffix),
            ]
            for test_file in test_patterns:
                if test_file.exists():
                    subprocess.run(['npx', 'jest', str(test_file)], capture_output=True)
                    break
    except:
        pass

if __name__ == '__main__':
    main()
