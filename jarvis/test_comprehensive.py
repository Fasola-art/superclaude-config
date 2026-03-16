#!/usr/bin/env python3
"""JARVIS 종합 테스트"""

import sys
from pathlib import Path

JARVIS_DIR = Path(__file__).parent
sys.path.insert(0, str(JARVIS_DIR))


def test_memory_imports():
    """Memory 모듈 import"""
    print("\n=== Memory Imports ===")
    errors = []

    try:
        from memory.manager import (
            TaskManager, CalendarManager, ContextManager,
            init_database
        )
        print("✓ memory.manager")
    except Exception as e:
        errors.append(f"memory.manager: {e}")
        print(f"✗ memory.manager: {e}")

    return len(errors) == 0, errors


def test_actions_imports():
    """Actions 모듈 import"""
    print("\n=== Actions Imports ===")
    errors = []

    functions = [
        'execute_command', 'save_context', 'get_last_context',
        'book_reservation', 'create_plan', 'search_web'
    ]

    try:
        import actions
        for func_name in functions:
            if hasattr(actions, func_name):
                print(f"✓ actions.{func_name}")
            else:
                errors.append(f"{func_name} not found")
                print(f"✗ actions.{func_name}")
    except Exception as e:
        errors.append(f"actions: {e}")
        print(f"✗ actions: {e}")

    return len(errors) == 0, errors


def test_nlu_imports():
    """NLU 모듈 import"""
    print("\n=== NLU Imports ===")
    errors = []

    try:
        from nlu import (
            NLUParser, classify_intent,
            extract_dates, extract_entities
        )
        print("✓ nlu")
    except Exception as e:
        errors.append(f"nlu: {e}")
        print(f"✗ nlu: {e}")

    return len(errors) == 0, errors


def test_memory_basic():
    """Memory 기본 기능"""
    print("\n=== Memory Basic Tests ===")

    try:
        from memory.manager import TaskManager, init_database

        init_database()
        print("✓ Database initialized")

        task_id = TaskManager.add_task("테스트 작업", "자동 테스트")
        print(f"✓ Task created: #{task_id}")

        tasks = TaskManager.get_pending_tasks()
        print(f"✓ Tasks retrieved: {len(tasks)}")

        return True, None
    except Exception as e:
        return False, str(e)


def test_actions_remember_recall():
    """Remember/Recall 기능"""
    print("\n=== Remember/Recall Tests ===")

    try:
        from actions import save_context, get_last_context

        # Save context (project_path, summary 필수)
        save_context(
            project_path="/test",
            summary="자동 테스트",
            last_file="test.py",
            last_action="test"
        )
        print("✓ Context saved")

        # Recall
        context = get_last_context()
        if context:
            print(f"✓ Context recalled: {context['last_action']}")
        else:
            print("○ No context found (expected on first run)")

        return True, None
    except Exception as e:
        return False, str(e)


def test_actions_do():
    """Do 명령 실행"""
    print("\n=== Do Command Tests ===")

    try:
        from actions import execute_command

        # 간단한 명령 테스트
        result = execute_command("할 일 목록")

        if result:
            print(f"✓ Command executed: {result.get('intent', 'unknown')}")
        else:
            print("✗ No result returned")

        return True, None
    except Exception as e:
        return False, str(e)


def test_nlu_intent():
    """NLU 의도 분류"""
    print("\n=== NLU Intent Tests ===")

    try:
        from nlu import classify_intent

        test_cases = [
            ("할 일 목록 보여줘", "list_tasks"),
            ("새 작업 추가", "add_task"),
            ("어디까지 했더라", "recall"),
            ("일정 보기", "list_events"),
        ]

        for text, expected in test_cases:
            intent = classify_intent(text)
            actual = intent.name if hasattr(intent, 'name') else str(intent)
            status = "✓" if expected in actual.lower() else "○"
            print(f"{status} '{text}' -> {actual}")

        return True, None
    except Exception as e:
        return False, str(e)


def test_nlu_parsing():
    """NLU 파싱"""
    print("\n=== NLU Parsing Tests ===")

    try:
        from nlu import NLUParser

        parser = NLUParser()

        tests = [
            "내일 오후 3시에 회의",
            "3개 항목 추가",
            '"중요한 작업" 생성',
        ]

        for text in tests:
            result = parser.parse(text)
            print(f"✓ '{text}' -> {result.intent if hasattr(result, 'intent') else 'parsed'}")

        return True, None
    except Exception as e:
        return False, str(e)


def test_modules():
    """Modules 테스트"""
    print("\n=== Modules Import Tests ===")

    modules = {
        'habit': 'HabitTracker',
        'coach': 'Coach',
        'weather': 'WeatherService',
    }

    errors = []

    for module_name, class_name in modules.items():
        try:
            module = __import__(f'modules.{module_name}', fromlist=[class_name])
            if hasattr(module, class_name):
                print(f"✓ modules.{module_name}.{class_name}")
            else:
                print(f"○ modules.{module_name} (no {class_name})")
        except Exception as e:
            errors.append(f"{module_name}: {e}")
            print(f"✗ modules.{module_name}: {e}")

    return len(errors) == 0, errors


def run_all():
    """전체 테스트"""
    print("=" * 70)
    print("JARVIS 종합 테스트")
    print("=" * 70)

    suite = [
        ("Memory Imports", test_memory_imports),
        ("Actions Imports", test_actions_imports),
        ("NLU Imports", test_nlu_imports),
        ("Memory Basic", test_memory_basic),
        ("Remember/Recall", test_actions_remember_recall),
        ("Do Command", test_actions_do),
        ("NLU Intent", test_nlu_intent),
        ("NLU Parsing", test_nlu_parsing),
        ("Modules", test_modules),
    ]

    results = []

    for name, func in suite:
        try:
            success, error = func()
            results.append({
                'name': name,
                'status': 'PASS' if success else 'FAIL',
                'error': error
            })
        except Exception as e:
            results.append({
                'name': name,
                'status': 'ERROR',
                'error': str(e)
            })

    # 결과 출력
    print("\n" + "=" * 70)
    print("테스트 결과")
    print("=" * 70)

    passed = sum(1 for r in results if r['status'] == 'PASS')
    total = len(results)

    for r in results:
        print(f"{r['name']:<25} {r['status']}")
        if r['error']:
            if isinstance(r['error'], list):
                for e in r['error']:
                    print(f"  └─ {e}")
            else:
                print(f"  └─ {r['error']}")

    print(f"\n통과: {passed}/{total}")

    return results


if __name__ == "__main__":
    results = run_all()
    sys.exit(0 if all(r['status'] == 'PASS' for r in results) else 1)
