#!/usr/bin/env python3
"""
Do 기능 테스트
"""

import sys
from pathlib import Path

# 경로 추가
jarvis_root = Path(__file__).parent.parent
sys.path.insert(0, str(jarvis_root))

from jarvis.actions.do import execute_command


def test_do_commands():
    """Do 명령 테스트"""
    test_cases = [
        {
            'command': '내일까지 "보고서 작성" 추가해줘',
            'expected_action': 'add_task'
        },
        {
            'command': '할 일 목록 보여줘',
            'expected_action': 'list_tasks'
        },
        {
            'command': 'GitHub PR 확인해줘',
            'expected_action': 'github_check'
        },
        {
            'command': '오늘 일정 보여줘',
            'expected_action': 'list_events'
        },
        {
            'command': '지금까지 작업 내용 기억해줘',
            'expected_action': 'remember'
        },
        {
            'command': '어디까지 했더라',
            'expected_action': 'recall'
        },
    ]

    print("=== JARVIS Do Test ===\n")
    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        command = test['command']
        expected = test['expected_action']

        print(f"Test {i}: {command}")
        result = execute_command(command)

        if result.get('action') == expected:
            print(f"✅ PASS - Action: {result.get('action')}")
            passed += 1
        else:
            print(f"❌ FAIL - Expected: {expected}, Got: {result.get('action')}")
            failed += 1

        print(f"   Result: {result.get('message', '')}\n")

    print(f"\n=== Summary ===")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")

    return failed == 0


if __name__ == "__main__":
    success = test_do_commands()
    sys.exit(0 if success else 1)
