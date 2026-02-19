#!/usr/bin/env python3
"""
Context Handlers - 컨텍스트 관리 핸들러
"""

from typing import Dict, Any
from pathlib import Path
import sys

jarvis_root = Path(__file__).parent.parent
sys.path.insert(0, str(jarvis_root))

from jarvis.memory.manager import ContextManager


def handle_remember(command: str) -> Dict[str, Any]:
    """컨텍스트 저장"""
    ContextManager.save_context(
        project_path=".",
        last_file="",
        last_action="remember",
        summary=command
    )
    return {'success': True, 'action': 'remember', 'message': '컨텍스트가 저장되었습니다'}


def handle_recall(command: str) -> Dict[str, Any]:
    """컨텍스트 불러오기"""
    context = ContextManager.get_last_context()
    return {'success': True, 'action': 'recall', 'context': context}
