#!/usr/bin/env python3
"""JavaScript/TypeScript file auto-formatter (prettier)"""
import subprocess
import sys
import json
import os

def main():
    tool_result = os.environ.get('CLAUDE_TOOL_RESULT', '{}')

    try:
        result = json.loads(tool_result)
        file_path = result.get('filePath', '')

        if file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            # Format with prettier
            subprocess.run(['npx', 'prettier', '--write', file_path], capture_output=True)
    except:
        pass

if __name__ == '__main__':
    main()
