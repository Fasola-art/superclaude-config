"""
PostgreSQL 스키마 확장 테스트 (TDD)

모듈별 테이블 스키마 검증
"""
import pytest
from pathlib import Path


class TestJarvisSchema:
    """JARVIS 모듈별 스키마 테스트"""

    @pytest.fixture
    def schema_sql(self):
        """스키마 SQL 로드"""
        schema_path = Path(__file__).parent.parent / "schema" / "jarvis_tables.sql"
        if schema_path.exists():
            return schema_path.read_text()
        return None

    def test_schema_file_exists(self, schema_sql):
        """스키마 파일 존재 확인"""
        assert schema_sql is not None, "jarvis_tables.sql 파일이 필요합니다"

    def test_learning_table(self, schema_sql):
        """learning 테이블 정의 확인"""
        assert "CREATE TABLE" in schema_sql
        assert "learning_patterns" in schema_sql.lower()

    def test_habit_table(self, schema_sql):
        """habit 테이블 정의 확인"""
        assert "habits" in schema_sql.lower()

    def test_client_table(self, schema_sql):
        """client 테이블 정의 확인"""
        assert "clients" in schema_sql.lower()
        assert "work_logs" in schema_sql.lower()

    def test_indexes(self, schema_sql):
        """인덱스 정의 확인"""
        assert "CREATE INDEX" in schema_sql

    def test_timestamp_columns(self, schema_sql):
        """timestamp 컬럼 존재 확인"""
        assert "created_at" in schema_sql.lower()
        assert "timestamp" in schema_sql.lower()
