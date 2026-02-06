#!/usr/bin/env python3
"""Coach 베이스 클래스"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import json


class BaseCoach(ABC):
    """Coach 베이스 클래스"""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.data_dir / f"{self.__class__.__name__.lower()}.json"
        self._load_data()

    def _load_data(self):
        """데이터 로드"""
        if self.log_file.exists():
            with open(self.log_file) as f:
                self.logs = json.load(f)
        else:
            self.logs = []

    def _save_data(self):
        """데이터 저장"""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2, default=str)

    @abstractmethod
    def log_activity(self, **kwargs):
        """활동 기록"""
        pass

    @abstractmethod
    def get_summary(self, days: int = 7):
        """요약 조회"""
        pass

    @abstractmethod
    def suggest(self):
        """추천"""
        pass

    def _filter_recent_logs(self, days: int):
        """최근 N일 로그 필터링"""
        cutoff = datetime.now().timestamp() - (days * 86400)
        return [
            log for log in self.logs
            if datetime.fromisoformat(log['timestamp']).timestamp() > cutoff
        ]
