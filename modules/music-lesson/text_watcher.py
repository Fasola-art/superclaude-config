"""
텍스트 파일 감시 모듈
클로바노트 텍스트 파일 감지 → 자동 요약 → Notion 업로드

사용법:
    python text_watcher.py                    # 기본 클로바노트 폴더
    python text_watcher.py /path/to/folder    # 지정 폴더
"""

from __future__ import annotations

import time
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Union, Set

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent

from text_pipeline import process_text_file


class TextFileHandler(FileSystemEventHandler):
    """텍스트 파일 감지 핸들러"""

    SUPPORTED_EXTENSIONS = {".txt", ".text"}  # .md 제외 (요약 파일과 충돌 방지)

    def __init__(
        self,
        processed_dir: Optional[Path] = None,
        upload_notion: bool = True,
        save_markdown: bool = True
    ):
        """
        Args:
            processed_dir: 처리 완료 파일 이동 경로 (None이면 이동 안함)
            upload_notion: Notion 업로드 여부
            save_markdown: 마크다운 파일 저장 여부
        """
        self.processed_dir = processed_dir
        self.upload_notion = upload_notion
        self.save_markdown = save_markdown
        self.processing: Set[Path] = set()
        self.processed_files: Set[str] = set()  # 이미 처리한 파일 추적

    def on_created(self, event: FileCreatedEvent) -> None:
        """새 파일 생성 시 호출"""
        self._handle_file(event.src_path)

    def on_modified(self, event: FileModifiedEvent) -> None:
        """파일 수정 시 호출 (구글 드라이브 동기화 완료 감지용)"""
        self._handle_file(event.src_path)

    def _handle_file(self, src_path: str) -> None:
        """파일 처리"""
        file_path = Path(src_path)

        # 디렉토리 무시
        if file_path.is_dir():
            return

        # 지원 형식 확인
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return

        # 숨김 파일 무시
        if file_path.name.startswith("."):
            return

        # 이미 처리한 파일 무시
        file_key = f"{file_path}:{file_path.stat().st_mtime}"
        if file_key in self.processed_files:
            return

        # 중복 처리 방지
        if file_path in self.processing:
            return

        self.processing.add(file_path)

        try:
            # 파일 쓰기 완료 대기 (동기화 중일 수 있음)
            self._wait_for_file_ready(file_path)

            # 최소 크기 확인 (100자 이상)
            if file_path.stat().st_size < 100:
                return

            print(f"\n🆕 새 텍스트 파일 감지: {file_path.name}")
            print(f"   시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # 파이프라인 실행
            result = process_text_file(
                file_path,
                upload=self.upload_notion,
                save_markdown=self.save_markdown
            )

            if result.notion_url:
                print(f"📎 Notion: {result.notion_url}")

            # 처리 완료 기록
            self.processed_files.add(file_key)

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

    def _wait_for_file_ready(self, file_path: Path, timeout: int = 30) -> None:
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

            if current_size == prev_size and current_size > 0:
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
            "text_watch_path": default_watch_path,
            "processed_dir": None,
            "recursive": True,
            "auto_upload": True,
            "save_markdown": True
        }

    with open(config_path) as f:
        config = json.load(f)

    return {
        "text_watch_path": config.get("text_watch_path", default_watch_path),
        "processed_dir": config.get("processed_dir"),
        "recursive": config.get("recursive", True),
        "auto_upload": config.get("auto_upload", True),
        "save_markdown": config.get("save_markdown", True)
    }


def start_text_watcher(
    watch_path: Optional[Union[str, Path]] = None,
    recursive: bool = True
) -> None:
    """
    텍스트 파일 폴더 감시 시작

    Args:
        watch_path: 감시할 폴더 경로 (없으면 설정에서 로드)
        recursive: 하위 폴더 포함 여부
    """
    config = load_watcher_config()

    if watch_path is None:
        watch_path = config["text_watch_path"]

    watch_path = Path(watch_path).expanduser()

    if not watch_path.exists():
        print(f"❌ 폴더가 존재하지 않습니다: {watch_path}")
        print(f"   구글 드라이브가 동기화되어 있는지 확인하세요.")
        return

    processed_dir = None
    if config.get("processed_dir"):
        processed_dir = Path(config["processed_dir"])

    handler = TextFileHandler(
        processed_dir=processed_dir,
        upload_notion=config.get("auto_upload", True),
        save_markdown=config.get("save_markdown", True)
    )
    observer = Observer()
    observer.schedule(handler, str(watch_path), recursive=recursive)

    print("📝 클로바노트 텍스트 파일 감시 시작")
    print(f"   경로: {watch_path}")
    print(f"   하위 폴더: {'포함' if recursive else '제외'}")
    print(f"   지원 형식: {', '.join(handler.SUPPORTED_EXTENSIONS)}")
    print("\n💡 클로바노트 앱에서 텍스트 내보내기 → 구글 드라이브에 저장")
    print("   → 자동으로 요약 생성 → Notion 업로드")
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
    start_text_watcher(watch_path)
