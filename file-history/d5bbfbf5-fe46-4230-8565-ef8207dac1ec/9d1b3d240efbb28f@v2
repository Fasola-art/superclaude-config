#!/usr/bin/env python3
"""
JARVIS Task Completion Hook
TodoWrite에서 완료 상태 감지하고 축하 메시지 표시
Hook Type: PostToolUse
"""

import os
import sys
import json
from pathlib import Path

# JARVIS 모듈 경로 추가
JARVIS_DIR = Path.home() / ".claude" / "jarvis"
sys.path.insert(0, str(JARVIS_DIR / "memory"))


def get_celebration_message(progress: int) -> str:
    """진행률에 따른 축하 메시지"""
    if progress >= 100:
        return "🎉 축하합니다! 모든 작업을 완료했습니다!"
    elif progress >= 80:
        return "🚀 거의 다 왔어요! 80% 이상 완료!"
    elif progress >= 50:
        return "💪 절반 이상 완료! 계속 화이팅!"
    else:
        return None


def main():
    # TodoWrite 도구인지 확인
    tool_name = os.environ.get('CLAUDE_TOOL_NAME', '')

    if tool_name not in ['TodoWrite', 'TaskUpdate']:
        return

    tool_input = os.environ.get('CLAUDE_TOOL_INPUT', '{}')

    try:
        input_data = json.loads(tool_input)
    except:
        input_data = {}

    # 완료 상태 체크
    status = input_data.get('status', '')

    if status != 'completed':
        return

    try:
        from manager import init_database, ContextManager

        init_database()

        # 마일스톤 저장
        project_path = os.environ.get('CLAUDE_PROJECT_PATH', str(Path.cwd()))
        task_id = input_data.get('taskId', input_data.get('id', ''))

        ContextManager.save_context(
            project_path=project_path,
            last_file='',
            last_action='task_completed',
            summary=f'Task #{task_id} completed'
        )

        # 진행률 계산 (간단한 추정)
        # 실제로는 TodoList에서 전체 작업 수와 완료 수를 가져와야 함
        print(f"\n✅ 작업이 완료되었습니다!")

    except Exception as e:
        pass


if __name__ == "__main__":
    main()
