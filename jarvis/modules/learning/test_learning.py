"""학습 시스템 테스트 - TDD"""
import pytest
from datetime import datetime
from .learning import LearningSystem, Pattern, Feedback


class TestLearningSystem:
    """학습 시스템 핵심 기능 테스트"""

    @pytest.fixture
    def system(self, tmp_path):
        """테스트용 학습 시스템"""
        db_path = tmp_path / "learning.db"
        return LearningSystem(str(db_path))

    def test_record_pattern(self, system):
        """패턴 기록 테스트"""
        pattern = system.record_pattern(
            category="command",
            input_text="매일 아침 브리핑",
            output_action="briefing",
            context={"time": "morning"}
        )
        assert pattern.id is not None
        assert pattern.category == "command"
        assert pattern.confidence == 1.0

    def test_find_similar_patterns(self, system):
        """유사 패턴 검색 테스트"""
        # 패턴 학습
        system.record_pattern("command", "아침 브리핑 해줘", "briefing")
        system.record_pattern("command", "오늘 브리핑", "briefing")
        system.record_pattern("command", "할일 보여줘", "todo_list")

        # 유사 패턴 검색
        matches = system.find_similar("브리핑 부탁해", top_k=2)
        assert len(matches) >= 1
        assert matches[0].output_action == "briefing"

    def test_record_feedback(self, system):
        """피드백 기록 테스트"""
        pattern = system.record_pattern("command", "테스트", "action")

        # 긍정 피드백
        system.record_feedback(pattern.id, positive=True)
        updated = system.get_pattern(pattern.id)
        assert updated.confidence > 1.0

        # 부정 피드백
        system.record_feedback(pattern.id, positive=False)
        updated = system.get_pattern(pattern.id)
        assert updated.confidence < 1.5

    def test_get_suggestions(self, system):
        """제안 생성 테스트"""
        # 반복 패턴 학습
        for _ in range(3):
            system.record_pattern("habit", "9시 운동", "exercise_reminder")

        suggestions = system.get_suggestions(context={"hour": 9})
        assert len(suggestions) > 0

    def test_export_import(self, system, tmp_path):
        """학습 데이터 내보내기/가져오기"""
        system.record_pattern("test", "input", "output")

        export_path = tmp_path / "export.json"
        system.export_data(str(export_path))

        assert export_path.exists()

        # 새 시스템에서 가져오기
        new_db = tmp_path / "new.db"
        new_system = LearningSystem(str(new_db))
        new_system.import_data(str(export_path))

        patterns = new_system.find_similar("input", top_k=1)
        assert len(patterns) == 1
