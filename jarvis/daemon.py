#!/usr/bin/env python3
"""
JARVIS Background Daemon
자동 재학습, 백업, 패턴 업데이트
"""

import time
import shutil
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 상대 import를 위한 경로 설정
import sys
sys.path.insert(0, str(Path(__file__).parent / "memory"))
from manager import init_database, DB_PATH

JARVIS_DIR = Path(__file__).parent
DATA_DIR = JARVIS_DIR / "data"
BACKUP_DIR = JARVIS_DIR / "backups"


class JarvisDaemon:
    """JARVIS 백그라운드 데몬"""

    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._ensure_dirs()

    def _ensure_dirs(self):
        """필요한 디렉토리 생성"""
        BACKUP_DIR.mkdir(exist_ok=True)
        DATA_DIR.mkdir(exist_ok=True)

    def start(self):
        """데몬 시작"""
        if self.running:
            print("Daemon already running")
            return

        self.running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("JARVIS Daemon started")

    def stop(self):
        """데몬 중지"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        print("JARVIS Daemon stopped")

    def _run(self):
        """메인 데몬 루프"""
        last_backup = datetime.min
        last_pattern_update = datetime.min

        while self.running:
            now = datetime.now()

            # 매일 백업 (자정 이후)
            if now.hour == 0 and (now - last_backup) > timedelta(hours=23):
                self._backup_data()
                last_backup = now

            # 매시간 패턴 업데이트
            if (now - last_pattern_update) > timedelta(hours=1):
                self._update_patterns()
                last_pattern_update = now

            # 1분마다 체크
            time.sleep(60)

    def _backup_data(self):
        """데이터 백업"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # SQLite 백업
        if DB_PATH.exists():
            backup_path = BACKUP_DIR / f"jarvis_{timestamp}.db"
            shutil.copy(DB_PATH, backup_path)
            print(f"Database backed up: {backup_path}")

        # JSON 데이터 백업
        for json_file in DATA_DIR.glob("*.json"):
            backup_path = BACKUP_DIR / f"{json_file.stem}_{timestamp}.json"
            shutil.copy(json_file, backup_path)

        # 오래된 백업 정리 (7일 이상)
        self._cleanup_old_backups()

    def _cleanup_old_backups(self, days: int = 7):
        """오래된 백업 파일 정리"""
        cutoff = datetime.now() - timedelta(days=days)

        for backup_file in BACKUP_DIR.iterdir():
            if backup_file.is_file():
                mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
                if mtime < cutoff:
                    backup_file.unlink()
                    print(f"Deleted old backup: {backup_file.name}")

    def _update_patterns(self):
        """패턴 모델 업데이트"""
        try:
            from ml_predictor import get_predictor
            predictor = get_predictor()
            predictor._load_or_train()
            print("Pattern model updated")
        except Exception as e:
            print(f"Pattern update failed: {e}")


def main():
    """메인 함수"""
    # 데이터베이스 초기화
    init_database()

    daemon = JarvisDaemon()

    print("=" * 50)
    print("JARVIS Background Daemon")
    print("=" * 50)
    print(f"JARVIS Directory: {JARVIS_DIR}")
    print(f"Database Path: {DB_PATH}")
    print(f"Backup Directory: {BACKUP_DIR}")
    print("=" * 50)

    try:
        daemon.start()
        print("\nPress Ctrl+C to stop...")

        # 메인 스레드 유지
        while daemon.running:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nShutting down...")
        daemon.stop()


if __name__ == "__main__":
    main()
