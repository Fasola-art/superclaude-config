"""
Jarvis 사용 예시
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis import TaskManager, CalendarManager, ContextManager, NLUParser
from datetime import datetime, timedelta


def demo_nlu():
    """자연어 이해 데모"""
    print("=" * 60)
    print("NLU Parser Demo")
    print("=" * 60)

    parser = NLUParser()

    commands = [
        "할 일 추가: 보고서 작성 긴급",
        "내일 오후 3시 회의 일정 추가",
        "할 일 목록 보여줘",
        "오늘 일정 보여줘",
    ]

    for cmd in commands:
        result = parser.parse(cmd)
        print(f"\n입력: {cmd}")
        print(f"의도: {result['intent']}")
        print(f"엔티티: {result['entities']}")


def demo_task_manager():
    """작업 관리 데모"""
    print("\n" + "=" * 60)
    print("Task Manager Demo")
    print("=" * 60)

    tm = TaskManager()

    # 작업 추가
    tasks = [
        {"title": "프로젝트 문서 작성", "priority": 9, "tags": ["work", "urgent"]},
        {"title": "코드 리뷰", "priority": 7, "tags": ["work"]},
        {"title": "운동하기", "priority": 5, "tags": ["health"]},
    ]

    print("\n작업 추가 중...")
    for task in tasks:
        task_id = tm.add_task(**task)
        print(f"  ✓ {task['title']} (ID: {task_id})")

    # 작업 목록 조회
    print("\n현재 작업 목록:")
    all_tasks = tm.get_tasks(status="todo")
    for task in all_tasks:
        print(f"  [{task['priority']}] {task['title']} - {task['tags']}")

    # 작업 완료
    if all_tasks:
        tm.complete_task(all_tasks[0]['id'])
        print(f"\n✓ 작업 완료: {all_tasks[0]['title']}")

    tm.close()


def demo_calendar():
    """일정 관리 데모"""
    print("\n" + "=" * 60)
    print("Calendar Manager Demo")
    print("=" * 60)

    cm = CalendarManager()

    # 일정 추가
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 15:00")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d 10:00")

    events = [
        {"title": "팀 회의", "start_time": tomorrow, "location": "회의실 A"},
        {"title": "클라이언트 미팅", "start_time": next_week, "location": "온라인"},
    ]

    print("\n일정 추가 중...")
    for event in events:
        event_id = cm.add_event(**event)
        print(f"  ✓ {event['title']} - {event['start_time']}")

    # 일정 조회
    print("\n예정된 일정:")
    upcoming = cm.get_events(start_date=datetime.now().strftime("%Y-%m-%d"))
    for event in upcoming:
        print(f"  • {event['title']}")
        print(f"    시간: {event['start_time']}")
        print(f"    장소: {event['location']}")

    cm.close()


def demo_context():
    """컨텍스트 관리 데모"""
    print("\n" + "=" * 60)
    print("Context Manager Demo")
    print("=" * 60)

    ctm = ContextManager()

    # 컨텍스트 추가
    contexts = [
        {"context_type": "conversation", "data": "사용자가 프로젝트 진행 상황에 대해 질문함"},
        {"context_type": "task", "data": "새로운 작업 추가: 보고서 작성"},
        {"context_type": "query", "data": "데이터베이스 쿼리 실행"},
    ]

    print("\n컨텍스트 저장 중...")
    for ctx in contexts:
        ctx_id = ctm.add_context(**ctx)
        print(f"  ✓ {ctx['context_type']}: {ctx['data'][:50]}...")

    # 최근 컨텍스트 조회
    print("\n최근 컨텍스트:")
    recent = ctm.get_recent_context(limit=5)
    for ctx in recent:
        print(f"  [{ctx['timestamp']}] {ctx['context_type']}: {ctx['data'][:50]}...")

    ctm.close()


if __name__ == "__main__":
    demo_nlu()
    demo_task_manager()
    demo_calendar()
    demo_context()

    print("\n" + "=" * 60)
    print("✅ 모든 데모 완료")
    print("=" * 60)
