#!/usr/bin/env python3
"""
JARVIS 통합 테스트: GitHub + Project + Memory
"""

import tempfile
from pathlib import Path
from datetime import datetime

import pytest

from jarvis.modules.github.monitor import GitHubMonitor
from jarvis.modules.project.monitor import ProjectMonitor
from jarvis.memory.manager import (
    WorkSessionManager,
    TaskManager,
    ContextManager,
)
from jarvis.memory.db import init_database


@pytest.fixture
def test_db():
    """테스트용 DB 초기화"""
    init_database()
    yield
    # cleanup if needed


@pytest.fixture
def temp_project():
    """임시 프로젝트 생성"""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        (project_path / "main.py").write_text("print('hello')")
        (project_path / "README.md").write_text("# Test Project")
        yield project_path


def test_project_session_workflow(test_db, temp_project):
    """시나리오 1: 프로젝트 스캔 → 세션 기록"""
    # ProjectMonitor로 스캔
    monitor = ProjectMonitor()
    state = monitor.scan_project(temp_project)

    assert state.total_files == 2
    assert '.py' in state.file_types or 'py' in state.file_types

    # WorkSession 시작
    session_id = f"test-{datetime.now().isoformat()}"
    ws_id = WorkSessionManager.start_session(str(temp_project), session_id)
    assert ws_id > 0

    # 파일 수정 시뮬레이션
    (temp_project / "new.py").write_text("# new")
    changes = monitor.detect_changes(temp_project)
    assert changes['added'] == 1

    # 세션 종료
    WorkSessionManager.end_session(
        session_id,
        files_edited=["new.py"],
        tools_used=["edit"],
        summary="Added new file"
    )

    recent = WorkSessionManager.get_recent_sessions(limit=1)
    assert len(recent) == 1
    assert recent[0]['session_id'] == session_id


def test_github_task_integration(test_db):
    """시나리오 2: GitHub 모니터 → TaskManager 연동"""
    # GitHub 모니터 초기화 (repos 없이)
    gh = GitHubMonitor(repos=[])

    # Task 추가 (PR 리뷰 시뮬레이션)
    task_id = TaskManager.add_task(
        title="Review PR #123",
        description="Code review needed",
        priority=1,
        project_path="owner/repo"
    )
    assert task_id > 0

    # 대기 중인 작업 확인
    pending = TaskManager.get_pending_tasks()
    assert len(pending) >= 1
    # 방금 추가한 작업 찾기
    our_task = next((t for t in pending if t['id'] == task_id), None)
    assert our_task is not None
    assert our_task['title'] == "Review PR #123"

    # 작업 완료
    TaskManager.complete_task(task_id)
    completed_pending = TaskManager.get_pending_tasks()
    assert all(t['id'] != task_id for t in completed_pending)


def test_full_workflow(test_db, temp_project):
    """시나리오 3: 전체 워크플로우"""
    # 1. ProjectMonitor 스캔
    pm = ProjectMonitor()
    state = pm.scan_project(temp_project)

    # 2. WorkSession 시작
    session_id = f"full-{datetime.now().isoformat()}"
    WorkSessionManager.start_session(str(temp_project), session_id)

    # 3. GitHub 모니터 초기화 (repos 없음)
    gh = GitHubMonitor(repos=[])
    notifications = gh.check_for_updates()
    # repos가 없으므로 알림도 없음
    assert notifications == []

    # 4. 프로젝트 변경
    (temp_project / "feature.py").write_text("def new_feature(): pass")
    changes = pm.detect_changes(temp_project)
    assert changes['added'] == 1

    # 5. 세션 종료
    WorkSessionManager.end_session(
        session_id,
        files_edited=["feature.py"],
        tools_used=["write", "edit"],
        summary="Implemented new feature"
    )

    # 6. Context 저장 (remember 기능)
    ContextManager.save_context(
        project_path=str(temp_project),
        last_file="feature.py",
        last_action="write",
        summary="Added feature implementation"
    )

    # 7. 검증
    last_ctx = ContextManager.get_last_context(str(temp_project))
    assert last_ctx is not None
    assert last_ctx['last_file'] == "feature.py"

    recent_sessions = WorkSessionManager.get_recent_sessions(limit=10)
    our_session = next((s for s in recent_sessions if s['session_id'] == session_id), None)
    assert our_session is not None
    assert our_session['summary'] == "Implemented new feature"
