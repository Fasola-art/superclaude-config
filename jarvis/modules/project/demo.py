"""ProjectMonitor 데모."""

from pathlib import Path
from .monitor import ProjectMonitor


def format_size(size_bytes: int) -> str:
    """바이트를 읽기 쉬운 형식으로 변환."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    """데모 실행."""
    monitor = ProjectMonitor()

    # jarvis 프로젝트 스캔
    jarvis_path = Path(__file__).parent.parent.parent
    print(f"프로젝트 경로: {jarvis_path}\n")

    print("=== 초기 스캔 ===")
    state = monitor.scan_project(jarvis_path)

    print(f"총 파일: {state.total_files}개")
    print(f"총 크기: {format_size(state.total_size)}")
    print(f"\n파일 타입별 분포:")
    for ext, count in sorted(state.file_types.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {ext:15s}: {count:4d}개")

    # 변경사항 감지 테스트 (현재는 변경사항 없음)
    print("\n=== 변경사항 확인 ===")
    try:
        changes = monitor.detect_changes(jarvis_path)
        print(f"추가: {changes['added']}개")
        print(f"삭제: {changes['removed']}개")
        print(f"수정: {changes['modified']}개")
        print(f"크기 변화: {format_size(changes['size_change'])}")
    except ValueError as e:
        print(f"변경사항 없음 (초기 스캔)")


if __name__ == '__main__':
    main()
