#!/usr/bin/env python3
"""
JARVIS Task Completion Hook
Detect completion status from TodoWrite and display celebration message
Hook Type: PostToolUse
"""

import os
import sys
import json
from pathlib import Path

# Add JARVIS module path
JARVIS_DIR = Path.home() / ".claude" / "jarvis"
sys.path.insert(0, str(JARVIS_DIR / "memory"))


def get_celebration_message(progress: int) -> str:
    """Get celebration message based on progress"""
    if progress >= 100:
        return "Congratulations! All tasks completed!"
    elif progress >= 80:
        return "Almost there! Over 80% complete!"
    elif progress >= 50:
        return "More than halfway! Keep going!"
    else:
        return None


def main():
    # Check if TodoWrite tool
    tool_name = os.environ.get('CLAUDE_TOOL_NAME', '')

    if tool_name not in ['TodoWrite', 'TaskUpdate']:
        return

    tool_input = os.environ.get('CLAUDE_TOOL_INPUT', '{}')

    try:
        input_data = json.loads(tool_input)
    except:
        input_data = {}

    # Check completion status
    status = input_data.get('status', '')

    if status != 'completed':
        return

    try:
        from manager import init_database, ContextManager

        init_database()

        # Save milestone
        project_path = os.environ.get('CLAUDE_PROJECT_PATH', str(Path.cwd()))
        task_id = input_data.get('taskId', input_data.get('id', ''))

        ContextManager.save_context(
            project_path=project_path,
            last_file='',
            last_action='task_completed',
            summary=f'Task #{task_id} completed'
        )

        # Calculate progress (simple estimation)
        # In practice, should get total and completed count from TodoList
        print(f"\nTask completed!")

    except Exception as e:
        pass


if __name__ == "__main__":
    main()
