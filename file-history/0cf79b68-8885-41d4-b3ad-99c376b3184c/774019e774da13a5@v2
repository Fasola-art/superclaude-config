#!/usr/bin/env python3
"""
plan-mode-analyzer.py
PRD 감지 및 플랜 모드 진입 훅

트리거: UserPromptSubmit
타임아웃: 3000ms
"""

import json
import sys
import re

PRD_KEYWORDS = [
    'PRD', 'prd', '요구사항', '기획서', '스펙', 'spec',
    '프로젝트 만들어', '앱 만들어', '서비스 만들어',
    '개발해줘', '구현해줘'
]

PRD_FILE_PATTERNS = [
    r'.*\.prd\.md$',
    r'.*PRD\.md$',
    r'.*requirements\.md$',
    r'.*기획서\.md$'
]

FEATURE_COUNT_THRESHOLD = 3

def detect_prd_document(prompt: str) -> dict:
    """PRD 문서 또는 관련 키워드 감지"""
    result = {
        'detected': False,
        'type': None,
        'confidence': 0,
        'features_count': 0
    }

    prompt_lower = prompt.lower()

    # 키워드 감지
    keyword_matches = sum(1 for kw in PRD_KEYWORDS if kw.lower() in prompt_lower)
    if keyword_matches > 0:
        result['detected'] = True
        result['type'] = 'keyword'
        result['confidence'] = min(keyword_matches * 0.25, 1.0)

    # 파일 패턴 감지
    for pattern in PRD_FILE_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            result['detected'] = True
            result['type'] = 'file'
            result['confidence'] = 0.9
            break

    # 기능 목록 감지 (번호 매기기 패턴)
    feature_patterns = [
        r'\d+\.\s+\w+',  # 1. 기능명
        r'-\s+\w+',       # - 기능명
        r'•\s+\w+',       # • 기능명
    ]
    for pattern in feature_patterns:
        matches = re.findall(pattern, prompt)
        result['features_count'] = max(result['features_count'], len(matches))

    if result['features_count'] >= FEATURE_COUNT_THRESHOLD:
        result['detected'] = True
        result['type'] = 'feature_list'
        result['confidence'] = max(result['confidence'], 0.7)

    return result


def determine_analysis_depth(prompt: str, detection: dict) -> str:
    """분석 깊이 결정"""
    prompt_lower = prompt.lower()

    # 빠르게 키워드가 있으면 간단 분석
    if any(kw in prompt_lower for kw in ['빠르게', 'qk', 'quick']):
        return 'quick'

    # PRD 문서면 깊은 분석
    if detection['type'] in ['file', 'feature_list']:
        return 'think-hard'

    # 기본 분석
    return 'think'


def main():
    try:
        input_data = sys.stdin.read()
        data = json.loads(input_data) if input_data.strip() else {}
        prompt = data.get('prompt', data.get('message', ''))

        detection = detect_prd_document(prompt)

        if not detection['detected']:
            output = {
                'status': 'none',
                'message': 'PRD 감지 안됨'
            }
        else:
            depth = determine_analysis_depth(prompt, detection)
            output = {
                'status': 'detected',
                'type': detection['type'],
                'confidence': detection['confidence'],
                'features_count': detection['features_count'],
                'analysis_depth': depth,
                'action': 'enter_plan_mode',
                'message': f"PRD 감지됨 (신뢰도: {detection['confidence']:.0%}) - 플랜 모드 진입 권장"
            }

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
