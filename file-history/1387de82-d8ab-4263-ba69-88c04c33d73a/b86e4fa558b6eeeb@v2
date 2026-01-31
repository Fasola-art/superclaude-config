#!/usr/bin/env python3
"""
페르소나 자동 활성화 Hook
- 컨텍스트 분석으로 적절한 페르소나 선택
- 최대 3개 동시 활성화
"""

import os
import sys
import re

# 페르소나 키워드 매핑
PERSONA_KEYWORDS = {
    "security": {
        "keywords": ["auth", "login", "password", "token", "jwt", "oauth", "보안", "인증", "권한"],
        "priority": 1
    },
    "architect": {
        "keywords": ["설계", "아키텍처", "구조", "패턴", "design", "architecture", "structure"],
        "priority": 2
    },
    "frontend": {
        "keywords": ["react", "vue", "css", "html", "컴포넌트", "ui", "ux", "스타일"],
        "priority": 3
    },
    "backend": {
        "keywords": ["api", "서버", "database", "db", "쿼리", "rest", "graphql"],
        "priority": 3
    },
    "devops": {
        "keywords": ["docker", "k8s", "kubernetes", "ci", "cd", "배포", "deploy", "aws", "gcp"],
        "priority": 4
    },
    "performance": {
        "keywords": ["성능", "최적화", "optimize", "performance", "속도", "메모리"],
        "priority": 3
    },
    "tester": {
        "keywords": ["테스트", "test", "jest", "vitest", "cypress", "e2e", "unit"],
        "priority": 4
    },
    "analyzer": {
        "keywords": ["분석", "analyze", "리뷰", "review", "검토"],
        "priority": 5
    },
    "explorer": {
        "keywords": ["찾아", "검색", "search", "find", "어디", "where"],
        "priority": 5
    }
}

MAX_CONCURRENT = 3

def detect_personas(prompt: str) -> list:
    """프롬프트에서 적절한 페르소나 감지"""
    prompt_lower = prompt.lower()
    detected = []

    for persona, config in PERSONA_KEYWORDS.items():
        for keyword in config["keywords"]:
            if keyword in prompt_lower:
                detected.append({
                    "name": persona,
                    "priority": config["priority"],
                    "matched": keyword
                })
                break

    # 우선순위로 정렬 후 상위 3개 선택
    detected.sort(key=lambda x: x["priority"])
    return detected[:MAX_CONCURRENT]

def main():
    prompt = os.environ.get("PROMPT", "")

    if not prompt and not sys.stdin.isatty():
        prompt = sys.stdin.read()

    if not prompt:
        return

    personas = detect_personas(prompt)

    if personas:
        names = [p['name'] for p in personas]
        print(f"🎭 {','.join(names)}")

if __name__ == "__main__":
    main()
