"""
JARVIS 모듈 간 통합 테스트 (E2E)

실제 모듈 인터페이스 기반 테스트
"""
import pytest
import sys
from pathlib import Path

# 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestLearningIntegration:
    """학습 시스템 통합 테스트"""

    @pytest.fixture
    def learning(self, tmp_path):
        from modules.learning import LearningSystem
        return LearningSystem(str(tmp_path / "learning.db"))

    def test_pattern_learning_cycle(self, learning):
        """패턴 학습 → 검색 → 피드백 사이클"""
        # 패턴 학습
        p1 = learning.record_pattern("cmd", "브리핑 해줘", "briefing")
        p2 = learning.record_pattern("cmd", "할일 보여줘", "show_todo")
        p3 = learning.record_pattern("cmd", "오늘 브리핑", "briefing")

        # 유사 패턴 검색
        results = learning.find_similar("브리핑 부탁", top_k=2)
        assert len(results) >= 1
        assert results[0].output_action == "briefing"

        # 피드백으로 신뢰도 조정
        learning.record_feedback(p1.id, positive=True)
        updated = learning.get_pattern(p1.id)
        assert updated.confidence > 1.0


class TestHabitCoachIntegration:
    """습관 + 코치 시스템 통합"""

    @pytest.fixture
    def habit(self):
        from modules.habit.tracker import HabitTracker
        return HabitTracker()

    @pytest.fixture
    def coaches(self, tmp_path):
        from modules.coach.pt_coach import PTCoach
        from modules.coach.diet_coach import DietCoach
        return PTCoach(tmp_path / "pt"), DietCoach(tmp_path / "diet")

    def test_habit_with_pt_coach(self, habit, coaches):
        """습관 기록 → PT 코치 운동 제안"""
        pt, _ = coaches

        # 운동 습관 추가
        habit_id = habit.add_habit("exercise", "매일 운동")
        assert habit_id > 0

        # PT 코치 운동 기록 및 제안
        pt.log_workout("squat", sets=3, reps=10, weight=60.0)
        suggestion = pt.suggest()
        assert suggestion is not None

    def test_habit_with_diet_coach(self, habit, coaches):
        """습관 기록 → 다이어트 코치 식단 제안"""
        _, diet = coaches

        # 식단 습관
        habit_id = habit.add_habit("healthy_eating", "건강한 식사")
        assert habit_id > 0

        # 다이어트 코치 식사 기록 및 제안
        diet.log_meal("breakfast", ["eggs", "toast"], calories=400)
        suggestion = diet.suggest()
        assert suggestion is not None


class TestClientProjectIntegration:
    """클라이언트 + 프로젝트 통합"""

    @pytest.fixture
    def client(self, tmp_path):
        from modules.client.tracker import ClientTracker
        return ClientTracker(str(tmp_path / "client.db"))

    @pytest.fixture
    def project(self):
        from modules.project.monitor import ProjectMonitor
        return ProjectMonitor()

    def test_client_project_workflow(self, client, project, tmp_path):
        """클라이언트 등록 → 프로젝트 작업 → 기록"""
        # 클라이언트 등록
        client_id = client.add_client("TestCorp", "웹사이트 개발")
        assert client_id > 0

        # 프로젝트 폴더 생성 및 스캔
        proj_dir = tmp_path / "testcorp"
        proj_dir.mkdir()
        (proj_dir / "main.py").write_text("# TestCorp Project")

        scan_result = project.scan_project(str(proj_dir))
        assert scan_result is not None

        # 작업 시간 기록
        client.log_work(client_id, 2.5, "초기 설정")
        summary = client.get_summary(client_id)
        assert summary["total_hours"] == 2.5


class TestGitHubProjectIntegration:
    """GitHub + 프로젝트 모니터 통합"""

    @pytest.fixture
    def github(self):
        from modules.github.monitor import GitHubMonitor
        return GitHubMonitor()

    @pytest.fixture
    def project(self):
        from modules.project.monitor import ProjectMonitor
        return ProjectMonitor()

    def test_github_project_sync(self, github, project, tmp_path):
        """프로젝트 스캔 → GitHub 상태 확인"""
        # Git 프로젝트 시뮬레이션
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        proj_dir = tmp_path
        (proj_dir / "README.md").write_text("# Test Project")

        # 프로젝트 스캔
        result = project.scan_project(str(proj_dir))
        assert result is not None


class TestEndToEndWorkflow:
    """전체 E2E 워크플로우"""

    @pytest.fixture
    def systems(self, tmp_path):
        from modules.learning import LearningSystem
        from modules.habit.tracker import HabitTracker
        from modules.client.tracker import ClientTracker

        return {
            "learning": LearningSystem(str(tmp_path / "learning.db")),
            "habit": HabitTracker(),
            "client": ClientTracker(str(tmp_path / "client.db")),
        }

    def test_daily_workflow(self, systems):
        """일일 워크플로우 E2E"""
        learn = systems["learning"]
        habit = systems["habit"]
        client = systems["client"]

        # 1. 아침 루틴 패턴 학습
        learn.record_pattern("morning", "아침 브리핑", "briefing")

        # 2. 습관 체크
        habit.add_habit("morning_routine", "아침 루틴")

        # 3. 클라이언트 작업
        client_id = client.add_client("ACME", "프로젝트 A")
        client.log_work(client_id, 4.0, "개발 작업")

        # 4. 검증
        results = learn.find_similar("브리핑", top_k=1)
        assert len(results) >= 1

        summary = client.get_summary(client_id)
        assert summary["total_hours"] == 4.0

    def test_learning_improvement(self, systems):
        """학습 시스템 개선 테스트"""
        learn = systems["learning"]

        # 여러 패턴 학습
        p1 = learn.record_pattern("cmd", "할일 보여줘", "todo")
        p2 = learn.record_pattern("cmd", "투두 리스트", "todo")

        # 피드백으로 p1 강화
        learn.record_feedback(p1.id, positive=True)
        learn.record_feedback(p1.id, positive=True)

        # p1의 신뢰도가 증가했는지 확인
        updated_p1 = learn.get_pattern(p1.id)
        assert updated_p1.confidence > 1.0

        # 유사 검색 결과 확인
        results = learn.find_similar("할일 리스트", top_k=2)
        assert len(results) == 2
        assert all(r.output_action == "todo" for r in results)
