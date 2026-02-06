"""모델 관리자 테스트."""
import sys
sys.path.insert(0, str(__file__).replace("/tests/test_model_manager.py", ""))

import pytest
from unittest.mock import patch, MagicMock

class TestModelManager:
    """ModelManager 테스트 (모델 로딩 없이)."""

    def test_singleton_pattern(self):
        """싱글톤 패턴 확인."""
        from model_manager import ModelManager
        m1 = ModelManager()
        m2 = ModelManager()
        assert m1 is m2

    def test_loaded_models_initially_empty(self):
        """초기 상태에서 로드된 모델 없음."""
        from model_manager import ModelManager
        manager = ModelManager()
        # 새 인스턴스처럼 초기화
        manager._loaded_models = {}
        manager._last_used = {}
        manager._tokenizers = {}
        assert manager.loaded_models == []

    @patch('model_manager.load')
    def test_load_model_caches(self, mock_load):
        """모델 로딩 후 캐시."""
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()
        mock_load.return_value = (mock_model, mock_tokenizer)

        from model_manager import ModelManager
        manager = ModelManager()
        manager._loaded_models = {}
        manager._last_used = {}
        manager._tokenizers = {}

        # 첫 번째 로드
        model1, tok1 = manager.load_model("qwen2.5-3b")
        # 두 번째 로드 (캐시에서)
        model2, tok2 = manager.load_model("qwen2.5-3b")

        assert model1 is model2
        mock_load.assert_called_once()  # 한 번만 호출됨

    def test_unload_model(self):
        """모델 언로드."""
        from model_manager import ModelManager
        manager = ModelManager()
        manager._loaded_models = {"test": MagicMock()}
        manager._tokenizers = {"test": MagicMock()}
        manager._last_used = {"test": 0}

        manager.unload_model("test")
        assert "test" not in manager._loaded_models


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
