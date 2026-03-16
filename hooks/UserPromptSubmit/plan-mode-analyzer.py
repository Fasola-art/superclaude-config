#!/usr/bin/env python3
"""
plan-mode-analyzer.py
PRD detection and plan mode entry hook

Trigger: UserPromptSubmit
Timeout: 3000ms
"""

import json
import sys
import re

PRD_KEYWORDS = [
    'PRD', 'prd', 'requirements', 'spec', 'specification',
    'create project', 'create app', 'create service',
    'build', 'develop', 'implement'
]

PRD_FILE_PATTERNS = [
    r'.*\.prd\.md$',
    r'.*PRD\.md$',
    r'.*requirements\.md$',
    r'.*spec\.md$'
]

FEATURE_COUNT_THRESHOLD = 3

def detect_prd_document(prompt: str) -> dict:
    """Detect PRD document or related keywords"""
    result = {
        'detected': False,
        'type': None,
        'confidence': 0,
        'features_count': 0
    }

    prompt_lower = prompt.lower()

    # Keyword detection
    keyword_matches = sum(1 for kw in PRD_KEYWORDS if kw.lower() in prompt_lower)
    if keyword_matches > 0:
        result['detected'] = True
        result['type'] = 'keyword'
        result['confidence'] = min(keyword_matches * 0.25, 1.0)

    # File pattern detection
    for pattern in PRD_FILE_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            result['detected'] = True
            result['type'] = 'file'
            result['confidence'] = 0.9
            break

    # Feature list detection (numbered pattern)
    feature_patterns = [
        r'\d+\.\s+\w+',  # 1. Feature name
        r'-\s+\w+',       # - Feature name
        r'•\s+\w+',       # - Feature name
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
    """Determine analysis depth"""
    prompt_lower = prompt.lower()

    # Quick analysis if 'quick' keyword present
    if any(kw in prompt_lower for kw in ['quick', 'qk', 'fast']):
        return 'quick'

    # Deep analysis for PRD documents
    if detection['type'] in ['file', 'feature_list']:
        return 'think-hard'

    # Default analysis
    return 'think'


def main():
    try:
        import os
        prompt = os.environ.get('PROMPT', '')
        if not prompt and not sys.stdin.isatty():
            prompt = sys.stdin.read()

        detection = detect_prd_document(prompt)

        if not detection['detected']:
            output = {
                'status': 'none',
                'message': 'No PRD detected'
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
                'message': f"PRD detected (confidence: {detection['confidence']:.0%}) - plan mode recommended"
            }

        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
