#!/usr/bin/env python3
"""
JARVIS Work Tracker Hook
도구 사용을 SQLite에 기록하고 패턴 학습
Hook Type: PostToolUse
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# JARVIS 모듈 경로 추가
JARVIS_DIR = Path.home() / ".claude" / "jarvis"
sys.path.insert(0, str(JARVIS_DIR / "memory"))


def main():
    # 환경변수에서 도구 정보 가져오기
    tool_name = os.environ.get('CLAUDE_TOOL_NAME', '')
    tool_input = os.environ.get('CLAUDE_TOOL_INPUT', '{}')

    if not tool_name:
        return

    try:
        input_data = json.loads(tool_input)
    except:
        input_data = {}

    # 파일 경로 추출 (여러 도구에서 사용되는 파라미터명)
    file_path = (
        input_data.get('file_path', '') or
        input_data.get('path', '') or
        input_data.get('pattern', '') or
        ''
    )

    try:
        from manager import init_database, UsagePatternTracker
        from ml_predictor import classify_work_type

        init_database()

        # 작업 유형 분류
        work_type = classify_work_type(tool_name, file_path)

        # 패턴 기록
        UsagePatternTracker.record_usage(work_type)

    except Exception as e:
        # 훅 실패는 조용히 처리 (사용자 경험 방해 금지)
        pass


if __name__ == "__main__":
    main()
