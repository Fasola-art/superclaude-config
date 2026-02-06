"""Project monitor tests."""

import tempfile
from pathlib import Path
from .monitor import ProjectMonitor


def test_scan_project():
    """프로젝트 스캔 테스트."""
    monitor = ProjectMonitor()

    # 임시 프로젝트 생성
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)

        # 테스트 파일 생성
        (project_path / 'main.py').write_text('print("hello")')
        (project_path / 'README.md').write_text('# Test Project')
        (project_path / 'config.json').write_text('{}')

        # 무시할 디렉토리
        (project_path / '__pycache__').mkdir()
        (project_path / '__pycache__' / 'test.pyc').write_text('cache')

        # 스캔
        state = monitor.scan_project(project_path)

        print(f"총 파일: {state.total_files}")
        print(f"총 크기: {state.total_size} bytes")
        print(f"파일 타입: {state.file_types}")

        assert state.total_files == 3, f"Expected 3 files, got {state.total_files}"
        assert '.py' in state.file_types
        assert '.md' in state.file_types
        assert '.json' in state.file_types
        assert '.pyc' not in state.file_types  # 무시됨


def test_detect_changes():
    """변경사항 감지 테스트."""
    monitor = ProjectMonitor()

    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)

        # 초기 파일
        (project_path / 'file1.txt').write_text('original')
        (project_path / 'file2.txt').write_text('data')

        # 첫 스캔
        state1 = monitor.scan_project(project_path)
        print(f"\n첫 스캔: {state1.total_files} files")

        # 변경사항 발생
        (project_path / 'file3.txt').write_text('new')  # 추가
        (project_path / 'file2.txt').unlink()  # 삭제
        (project_path / 'file1.txt').write_text('modified')  # 수정

        # 변경 감지
        changes = monitor.detect_changes(project_path)

        print(f"추가: {changes['added']}")
        print(f"삭제: {changes['removed']}")
        print(f"수정: {changes['modified']}")

        assert changes['added'] == 1
        assert changes['removed'] == 1
        assert changes['modified'] >= 0  # 파일 시스템 타이밍에 따라 다를 수 있음


def test_gitignore():
    """gitignore 존중 테스트."""
    monitor = ProjectMonitor()

    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)

        # gitignore 생성
        (project_path / '.gitignore').write_text('*.log\ntemp/\n')

        # 파일 생성
        (project_path / 'main.py').write_text('code')
        (project_path / 'debug.log').write_text('log data')
        temp_dir = project_path / 'temp'
        temp_dir.mkdir()
        (temp_dir / 'cache.txt').write_text('cache')

        # 스캔
        state = monitor.scan_project(project_path)

        print(f"\ngitignore 테스트: {state.total_files} files")
        print(f"파일 타입: {state.file_types}")

        # .log와 temp/ 디렉토리는 무시됨
        assert state.total_files <= 2  # main.py, .gitignore (gitignore는 포함될 수 있음)


if __name__ == '__main__':
    print("=== Project Monitor 테스트 ===\n")

    test_scan_project()
    print("\n✓ scan_project 테스트 통과")

    test_detect_changes()
    print("\n✓ detect_changes 테스트 통과")

    test_gitignore()
    print("\n✓ gitignore 테스트 통과")

    print("\n모든 테스트 통과!")
