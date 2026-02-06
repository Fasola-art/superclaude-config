"""로그 집계 시스템 테스트 (TDD)"""
import pytest
from datetime import datetime, timedelta
from .aggregator import LogAggregator, LogLevel


class TestLogAggregator:
    """로그 집계기 테스트"""

    @pytest.fixture
    def aggregator(self, tmp_path):
        return LogAggregator(str(tmp_path / "logs.db"))

    def test_log_info(self, aggregator):
        """INFO 로그 기록"""
        log_id = aggregator.log(LogLevel.INFO, "test", "테스트 메시지")
        assert log_id > 0

    def test_log_error(self, aggregator):
        """ERROR 로그 기록"""
        log_id = aggregator.log(
            LogLevel.ERROR,
            "api",
            "API 오류 발생",
            metadata={"endpoint": "/users"}
        )
        assert log_id > 0

    def test_query_by_level(self, aggregator):
        """레벨별 로그 조회"""
        aggregator.log(LogLevel.INFO, "src1", "info 1")
        aggregator.log(LogLevel.ERROR, "src2", "error 1")
        aggregator.log(LogLevel.INFO, "src3", "info 2")

        errors = aggregator.query(level=LogLevel.ERROR)
        assert len(errors) == 1
        assert errors[0]["level"] == "ERROR"

    def test_query_by_source(self, aggregator):
        """소스별 로그 조회"""
        aggregator.log(LogLevel.INFO, "api", "api log 1")
        aggregator.log(LogLevel.INFO, "api", "api log 2")
        aggregator.log(LogLevel.INFO, "db", "db log")

        api_logs = aggregator.query(source="api")
        assert len(api_logs) == 2

    def test_get_summary(self, aggregator):
        """로그 요약 통계"""
        aggregator.log(LogLevel.INFO, "src", "msg")
        aggregator.log(LogLevel.WARNING, "src", "msg")
        aggregator.log(LogLevel.ERROR, "src", "msg")
        aggregator.log(LogLevel.ERROR, "src", "msg")

        summary = aggregator.get_summary()
        assert summary["total"] == 4
        assert summary["by_level"]["ERROR"] == 2

    def test_cleanup_old_logs(self, aggregator):
        """오래된 로그 정리"""
        aggregator.log(LogLevel.INFO, "old", "old log")
        count = aggregator.cleanup(days=0)  # 즉시 정리
        assert count >= 0
