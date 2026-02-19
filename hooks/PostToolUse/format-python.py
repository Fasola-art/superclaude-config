#!/usr/bin/env python3
"""Python file auto-formatter (ruff)"""
import subprocess
import sys
import json
import os

def main():
    # Get tool result from environment variables
    tool_result = os.environ.get('CLAUDE_TOOL_RESULT', '{}')

    try:
        result = json.loads(tool_result)
        file_path = result.get('filePath', '')

        if file_path.endswith('.py'):
            # Format with ruff
            subprocess.run(['ruff', 'format', file_path], capture_output=True)
            subprocess.run(['ruff', 'check', '--fix', file_path], capture_output=True)
    except:
        pass

if __name__ == '__main__':
    main()
