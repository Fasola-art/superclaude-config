#!/usr/bin/env python3
"""
writer-reviewer-hook.py
Writer-Reviewer Loop 활성화 훅

트리거: PreToolUse
매처: Edit|Write|MultiEdit
타임아웃: 30000ms
"""

import json
import sys
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

CLAUDE_DIR = Path.home() / '.claude'
SETTINGS_FILE = CLAUDE_DIR / 'settings.json'

# 기본 설정
DEFAULT_CONFIG = {
    'targetScore': 0.85,
    'maxIterations': 10,
    'convergenceThreshold': 0.015,
    'agents': {
        'quality': {'weight': 0.30},
        'security': {'weight': 0.30, 'minScore': 0.85},
        'performance': {'weight': 0.20},
        'accessibility': {'weight': 0.20}
    }
}

# 코드 타입 감지 패턴
CODE_TYPE_PATTERNS = {
    'frontend': {
        'keywords': ['component', 'tsx', 'jsx', 'ui', 'form', 'button', 'modal'],
        'file_patterns': [r'\.tsx$', r'\.jsx$', r'components/'],
        'weights': {'quality': 0.25, 'security': 0.25, 'performance': 0.20, 'accessibility': 0.30}
    },
    'backend': {
        'keywords': ['api', 'route', 'endpoint', 'controller', 'service', 'handler'],
        'file_patterns': [r'/api/', r'/routes/', r'\.controller\.ts$'],
        'weights': {'quality': 0.25, 'security': 0.40, 'performance': 0.25, 'accessibility': 0.10}
    },
    'utility': {
        'keywords': ['util', 'helper', 'lib', 'function', 'hook'],
        'file_patterns': [r'/utils/', r'/lib/', r'/hooks/'],
        'weights': {'quality': 0.35, 'security': 0.25, 'performance': 0.30, 'accessibility': 0.10}
    },
    'database': {
        'keywords': ['query', 'sql', 'database', 'migration', 'schema'],
        'file_patterns': [r'/db/', r'/migrations/', r'\.sql$'],
        'weights': {'quality': 0.20, 'security': 0.40, 'performance': 0.35, 'accessibility': 0.05}
    }
}

# 스킵 조건
SKIP_CONDITIONS = [
    'git', 'config', '.md', '.json', '.env', 'package.json',
    'tsconfig', 'eslint', 'prettier', '.lock'
]


def load_settings() -> dict:
    """설정 로드"""
    try:
        if SETTINGS_FILE.exists():
            data = json.loads(SETTINGS_FILE.read_text())
            return data.get('writerReviewer', DEFAULT_CONFIG)
    except Exception:
        pass
    return DEFAULT_CONFIG


def detect_code_type(file_path: str, content: str = '') -> str:
    """코드 타입 감지"""
    combined = f"{file_path} {content}".lower()

    for code_type, patterns in CODE_TYPE_PATTERNS.items():
        # 키워드 매칭
        if any(kw in combined for kw in patterns['keywords']):
            return code_type
        # 파일 패턴 매칭
        if any(re.search(p, file_path) for p in patterns['file_patterns']):
            return code_type

    return 'utility'  # 기본값


def should_skip_review(file_path: str, tool_name: str) -> bool:
    """리뷰 스킵 여부 결정"""
    # 특정 파일 유형 스킵
    if any(skip in file_path.lower() for skip in SKIP_CONDITIONS):
        return True

    # 단일 라인 수정은 스킵 (실제 구현에서 확인)
    return False


def get_weights_for_type(code_type: str) -> dict:
    """코드 타입에 따른 가중치 반환"""
    if code_type in CODE_TYPE_PATTERNS:
        return CODE_TYPE_PATTERNS[code_type]['weights']
    return DEFAULT_CONFIG['agents']


@dataclass
class ReviewConfig:
    enabled: bool
    codeType: str
    weights: Dict[str, float]
    targetScore: float
    maxIterations: int
    message: str


def analyze_tool_call(data: dict) -> ReviewConfig:
    """도구 호출 분석 및 리뷰 설정 결정"""
    tool_name = data.get('tool', '')
    file_path = data.get('file_path', data.get('path', ''))
    content = data.get('content', data.get('new_string', ''))

    # 스킵 여부 확인
    if should_skip_review(file_path, tool_name):
        return ReviewConfig(
            enabled=False,
            codeType='skip',
            weights={},
            targetScore=0,
            maxIterations=0,
            message='리뷰 스킵 (설정/문서 파일)'
        )

    settings = load_settings()
    code_type = detect_code_type(file_path, content)
    weights = get_weights_for_type(code_type)

    return ReviewConfig(
        enabled=True,
        codeType=code_type,
        weights=weights,
        targetScore=settings.get('targetScore', 0.85),
        maxIterations=settings.get('maxIterations', 10),
        message=f'Writer-Reviewer 활성화: {code_type} 타입'
    )


def main():
    try:
        input_data = sys.stdin.read()
        data = json.loads(input_data) if input_data.strip() else {}

        config = analyze_tool_call(data)

        output = {
            'status': 'enabled' if config.enabled else 'skipped',
            **asdict(config)
        }

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
