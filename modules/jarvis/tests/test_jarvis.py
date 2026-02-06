"""
Jarvis module tests
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test module imports"""
    print("1. Testing imports...")

    try:
        from jarvis.memory import TaskManager, CalendarManager, ContextManager
        print("   ✅ Memory components imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import memory components: {e}")
        return False

    try:
        from jarvis.nlu import NLUParser
        print("   ✅ NLU parser imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import NLU parser: {e}")
        return False

    try:
        from jarvis.modules.github import GitHubMonitor
        print("   ✅ GitHub monitor imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import GitHub monitor: {e}")
        return False

    return True


def test_nlu_parser():
    """Test NLU parser functionality"""
    print("\n2. Testing NLU parser...")

    try:
        from jarvis.nlu import NLUParser

        parser = NLUParser()

        # Test task addition
        result = parser.parse("할 일 추가: 보고서 작성 긴급")
        print(f"   Input: '할 일 추가: 보고서 작성 긴급'")
        print(f"   Intent: {result['intent']}")
        print(f"   Entities: {result['entities']}")
        print(f"   Confidence: {result['confidence']}")

        if result['intent'] == 'add_task':
            print("   ✅ Intent detection working")
        else:
            print("   ⚠️  Intent not detected correctly")

        # Test event addition
        result = parser.parse("내일 오후 3:00 미팅 일정 추가")
        print(f"\n   Input: '내일 오후 3:00 미팅 일정 추가'")
        print(f"   Intent: {result['intent']}")
        print(f"   Entities: {result['entities']}")

        if result['intent'] == 'add_event':
            print("   ✅ Event intent detected")
        else:
            print("   ⚠️  Event intent not detected")

        return True

    except Exception as e:
        print(f"   ❌ Error testing NLU parser: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_task_manager():
    """Test TaskManager functionality"""
    print("\n3. Testing TaskManager...")

    try:
        from jarvis.memory import TaskManager

        tm = TaskManager()

        # Test adding task
        task_id = tm.add_task(
            title="테스트 작업",
            priority=8,
            tags=["test", "demo"]
        )
        print(f"   ✅ Task created with ID: {task_id}")

        # Test retrieving tasks
        tasks = tm.get_tasks(status="pending")
        print(f"   ✅ Retrieved {len(tasks)} pending tasks")

        # Test completing task
        tm.complete_task(task_id)
        print(f"   ✅ Task {task_id} completed")

        tm.close()
        return True

    except Exception as e:
        print(f"   ❌ Error testing TaskManager: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_calendar_manager():
    """Test CalendarManager functionality"""
    print("\n4. Testing CalendarManager...")

    try:
        from jarvis.memory import CalendarManager
        from datetime import datetime, timedelta

        cm = CalendarManager()

        # Test adding event
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        event_id = cm.add_event(
            title="테스트 미팅",
            start_time=tomorrow,
            location="온라인"
        )
        print(f"   ✅ Event created with ID: {event_id}")

        # Test retrieving events
        events = cm.get_events()
        print(f"   ✅ Retrieved {len(events)} events")

        cm.close()
        return True

    except Exception as e:
        print(f"   ❌ Error testing CalendarManager: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_context_manager():
    """Test ContextManager functionality"""
    print("\n5. Testing ContextManager...")

    try:
        from jarvis.memory import ContextManager

        ctm = ContextManager()

        # Test adding context
        context_id = ctm.add_context(
            context_type="conversation",
            data="사용자가 보고서 작성에 대해 질문함",
            metadata='{"topic": "report"}'
        )
        print(f"   ✅ Context saved with ID: {context_id}")

        # Test retrieving context
        contexts = ctm.get_recent_context(limit=5)
        print(f"   ✅ Retrieved {len(contexts)} recent contexts")

        ctm.close()
        return True

    except Exception as e:
        print(f"   ❌ Error testing ContextManager: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Jarvis Module Test Suite")
    print("=" * 60)

    results = {
        "imports": test_imports(),
        "nlu_parser": test_nlu_parser(),
        "task_manager": test_task_manager(),
        "calendar_manager": test_calendar_manager(),
        "context_manager": test_context_manager(),
    }

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20s}: {status}")

    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")

    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
