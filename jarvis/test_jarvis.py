#!/usr/bin/env python3
"""
JARVIS Test Suite
"""

import sys
from pathlib import Path

# 경로 설정
JARVIS_DIR = Path(__file__).parent
sys.path.insert(0, str(JARVIS_DIR / "memory"))
sys.path.insert(0, str(JARVIS_DIR / "automation"))


def test_database():
    """데이터베이스 테스트"""
    print("\n=== Database Test ===")

    from manager import (
        init_database, TaskManager,
        ContextManager, UsagePatternTracker
    )

    # 초기화
    init_database()
    print("✓ Database initialized")

    # 작업 추가
    task_id = TaskManager.add_task("테스트 작업", "테스트용 작업입니다")
    print(f"✓ Task added: #{task_id}")

    # 작업 조회
    tasks = TaskManager.get_pending_tasks()
    print(f"✓ Tasks retrieved: {len(tasks)} tasks")

    # 패턴 기록
    UsagePatternTracker.record_usage("code_editing")
    print("✓ Usage pattern recorded")

    # 컨텍스트 저장
    ContextManager.save_context("/test/path", "test.py", "edit", "테스트 컨텍스트")
    print("✓ Context saved")

    # 컨텍스트 조회
    context = ContextManager.get_last_context()
    print(f"✓ Context retrieved: {context is not None}")

    return True


def test_task_executor():
    """작업 실행기 테스트"""
    print("\n=== Task Executor Test ===")

    from task_executor import get_executor

    executor = get_executor()

    # 의도 분석 테스트
    tests = [
        ("할 일 목록 보여줘", "list_tasks"),
        ('"새 작업" 추가해줘', "add_task"),
        ("어디까지 했더라", "recall"),
        ("오늘 일정", "list_events"),
    ]

    for command, expected_intent in tests:
        result = executor.analyze_intent(command)
        status = "✓" if result['intent'] == expected_intent else "✗"
        print(f"{status} '{command}' -> {result['intent']} (expected: {expected_intent})")

    return True


def test_ml_predictor():
    """ML 예측기 테스트"""
    print("\n=== ML Predictor Test ===")

    from ml_predictor import get_predictor, classify_work_type

    # 작업 유형 분류 테스트
    tests = [
        ("Edit", "src/app.tsx", "code_editing"),
        ("Read", "test/app.test.tsx", "testing"),
        ("Bash", "", "command_execution"),
        ("Grep", "", "code_search"),
    ]

    for tool, path, expected in tests:
        result = classify_work_type(tool, path)
        status = "✓" if result == expected else "✗"
        print(f"{status} {tool} + '{path}' -> {result} (expected: {expected})")

    # 예측기 테스트
    predictor = get_predictor()
    prediction = predictor.predict_work_type()

    if prediction:
        print(f"✓ Prediction available: {prediction['predicted_work_type']}")
    else:
        print("○ Not enough data for prediction (need 10+ patterns)")

    return True


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 50)
    print("JARVIS Test Suite")
    print("=" * 50)

    results = []

    try:
        results.append(("Database", test_database()))
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        results.append(("Database", False))

    try:
        results.append(("Task Executor", test_task_executor()))
    except Exception as e:
        print(f"✗ Task Executor test failed: {e}")
        results.append(("Task Executor", False))

    try:
        results.append(("ML Predictor", test_ml_predictor()))
    except Exception as e:
        print(f"✗ ML Predictor test failed: {e}")
        results.append(("ML Predictor", False))

    # 결과 요약
    print("\n" + "=" * 50)
    print("Test Results")
    print("=" * 50)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name}: {status}")

    print(f"\n{passed}/{total} tests passed")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
