"""
폴더 감시 모듈
새 녹음 파일 감지 → 자동 처리

사용법:
    python watcher.py                    # 기본 폴더 감시
    python watcher.py /path/to/folder    # 지정 폴더 감시
"""

from __future__ import annotations

import time
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Union

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from pipeline import process_lesson


class LessonFileHandler(FileSystemEventHandler):
    """새 오디오 파일 감지 핸들러"""

    SUPPORTED_EXTENSIONS = {".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg"}

    def __init__(self, processed_dir: Optional[Path] = None):
        """
        Args:
            processed_dir: 처리 완료 파일 이동 경로 (None이면 이동 안함)
        """
        self.processed_dir = processed_dir
        self.processing = set()  # 현재 처리 중인 파일

    def on_created(self, event: FileCreatedEvent) -> None:
        """새 파일 생성 시 호출"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # 지원 형식 확인
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return

        # 숨김 파일 무시
        if file_path.name.startswith("."):
            return

        # 중복 처리 방지
        if file_path in self.processing:
            return

        self.processing.add(file_path)

        try:
            # 파일 쓰기 완료 대기 (큰 파일 복사 중일 수 있음)
            self._wait_for_file_ready(file_path)

            print(f"\n🆕 새 파일 감지: {file_path.name}")
            print(f"   시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # 파이프라인 실행
            result = process_lesson(file_path)

            if result.notion_url:
                print(f"📎 Notion: {result.notion_url}")

            # 처리 완료 파일 이동 (옵션)
            if self.processed_dir:
                self.processed_dir.mkdir(parents=True, exist_ok=True)
                new_path = self.processed_dir / file_path.name
                file_path.rename(new_path)
                print(f"📁 파일 이동: {new_path}")

        except Exception as e:
            print(f"❌ 처리 실패: {e}")

        finally:
            self.processing.discard(file_path)

    def _wait_for_file_ready(self, file_path: Path, timeout: int = 60) -> None:
        """파일 쓰기 완료 대기"""
        prev_size = -1
        stable_count = 0
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                current_size = file_path.stat().st_size
            except FileNotFoundError:
                time.sleep(0.5)
                continue

            if current_size == prev_size:
                stable_count += 1
                if stable_count >= 3:  # 1.5초 동안 크기 변화 없음
                    return
            else:
                stable_count = 0

            prev_size = current_size
            time.sleep(0.5)


def load_watcher_config() -> dict:
    """감시 설정 로드"""
    config_path = Path(__file__).parent / "config.json"

    # Windows Google Drive 기본 경로 (환경에 따라 G: 드라이브 문자 조정 필요)
    default_watch_path = str(Path("G:/내 드라이브/클로바노트"))

    if not config_path.exists():
        return {
            "watch_path": default_watch_path,
            "processed_dir": None,
            "recursive": False
        }

    with open(config_path) as f:
        config = json.load(f)

    return {
        "watch_path": config.get("watch_path", default_watch_path),
        "processed_dir": config.get("processed_dir"),
        "recursive": config.get("recursive", False)
    }


def start_watcher(
    watch_path: Optional[Union[str, Path]] = None,
    recursive: bool = False
) -> None:
    """
    폴더 감시 시작

    Args:
        watch_path: 감시할 폴더 경로 (없으면 설정에서 로드)
        recursive: 하위 폴더 포함 여부
    """
    config = load_watcher_config()

    if watch_path is None:
        watch_path = config["watch_path"]

    watch_path = Path(watch_path)

    if not watch_path.exists():
        print(f"❌ 폴더가 존재하지 않습니다: {watch_path}")
        return

    processed_dir = None
    if config.get("processed_dir"):
        processed_dir = Path(config["processed_dir"])

    handler = LessonFileHandler(processed_dir=processed_dir)
    observer = Observer()
    observer.schedule(handler, str(watch_path), recursive=recursive)

    print("🔍 음악 레슨 폴더 감시 시작")
    print(f"   경로: {watch_path}")
    print(f"   하위 폴더: {'포함' if recursive else '제외'}")
    print(f"   지원 형식: {', '.join(handler.SUPPORTED_EXTENSIONS)}")
    print("\n종료하려면 Ctrl+C를 누르세요...\n")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 감시 종료")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    import sys

    watch_path = sys.argv[1] if len(sys.argv) > 1 else None
    start_watcher(watch_path)
