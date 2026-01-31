#!/usr/bin/env python3
"""
페르소나 로더 및 활성화 유틸리티
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional

PERSONAS_DIR = Path.home() / ".claude" / "personas"

def load_dev_persona(persona_id: str) -> Optional[Dict]:
    """개발 페르소나 로드"""
    file_path = PERSONAS_DIR / "dev" / f"{persona_id}.json"
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return None

def load_ideation_personas(category: str) -> List[Dict]:
    """Ideation 페르소나 카테고리 로드"""
    file_path = PERSONAS_DIR / "ideation" / f"{category}.json"
    if file_path.exists():
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("personas", [])
    return []

def get_all_dev_personas() -> List[str]:
    """모든 개발 페르소나 ID 목록"""
    dev_dir = PERSONAS_DIR / "dev"
    if dev_dir.exists():
        return [f.stem for f in dev_dir.glob("*.json")]
    return []

def get_persona_by_keyword(keyword: str) -> List[Dict]:
    """키워드로 페르소나 검색"""
    matches = []
    keyword_lower = keyword.lower()

    # 개발 페르소나 검색
    for persona_id in get_all_dev_personas():
        persona = load_dev_persona(persona_id)
        if persona:
            keywords = [k.lower() for k in persona.get("keywords", [])]
            if any(keyword_lower in k or k in keyword_lower for k in keywords):
                matches.append(persona)

    return matches

def activate_personas(context: str, file_path: str = None) -> List[Dict]:
    """컨텍스트 기반 페르소나 활성화"""
    activated = []

    # 인덱스 로드
    index_file = PERSONAS_DIR / "index.json"
    if not index_file.exists():
        return activated

    with open(index_file, 'r') as f:
        index = json.load(f)

    rules = index.get("activation_rules", {})
    max_concurrent = rules.get("max_concurrent", 3)

    # 강제 활성화 체크
    forced = rules.get("forced_activation", {})
    for persona_id, config in forced.items():
        keywords = config.get("keywords", [])
        if any(kw in context.lower() for kw in keywords):
            persona = load_dev_persona(persona_id)
            if persona and persona not in activated:
                activated.append(persona)

    # 컨텍스트 기반 활성화
    if file_path:
        context_rules = rules.get("context_based", [])
        for rule in context_rules:
            pattern = rule.get("pattern", "")
            if pattern in file_path or file_path.endswith(pattern.replace("*", "")):
                for persona_id in rule.get("personas", []):
                    if len(activated) >= max_concurrent:
                        break
                    persona = load_dev_persona(persona_id)
                    if persona and persona not in activated:
                        activated.append(persona)

    # 키워드 기반 활성화
    keyword_matches = get_persona_by_keyword(context)
    for persona in keyword_matches:
        if len(activated) >= max_concurrent:
            break
        if persona not in activated:
            activated.append(persona)

    return activated[:max_concurrent]

def print_persona_info(persona: Dict):
    """페르소나 정보 출력"""
    print(f"🎭 {persona.get('name', 'Unknown')} ({persona.get('id', '')})")
    print(f"   역할: {persona.get('role', '')}")
    if persona.get('skills'):
        print(f"   스킬: {', '.join(persona['skills'][:3])}")

def list_all_personas():
    """모든 페르소나 목록 출력"""
    print("=== 개발 페르소나 (14개) ===")
    for persona_id in sorted(get_all_dev_personas()):
        persona = load_dev_persona(persona_id)
        if persona:
            print(f"  • {persona_id}: {persona.get('name', '')}")

    print("\n=== Ideation 페르소나 (27개) ===")
    categories = ["business", "marketing", "innovation", "design", "validation", "research", "special"]
    for cat in categories:
        personas = load_ideation_personas(cat)
        if personas:
            print(f"  [{cat}]")
            for p in personas:
                print(f"    • {p.get('id', '')}: {p.get('name', '')}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            list_all_personas()
        elif cmd == "get" and len(sys.argv) > 2:
            persona = load_dev_persona(sys.argv[2])
            if persona:
                print_persona_info(persona)
            else:
                print(f"페르소나 '{sys.argv[2]}' 없음")
        elif cmd == "activate" and len(sys.argv) > 2:
            context = " ".join(sys.argv[2:])
            activated = activate_personas(context)
            print(f"활성화된 페르소나: {len(activated)}개")
            for p in activated:
                print_persona_info(p)
    else:
        print("사용법:")
        print("  python loader.py list              - 모든 페르소나 목록")
        print("  python loader.py get <id>          - 특정 페르소나 정보")
        print("  python loader.py activate <context> - 컨텍스트 기반 활성화")
