#!/usr/bin/env python3
"""페르소나 로더 및 활성화 유틸리티 (전체 카테고리 지원)"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

PERSONAS_DIR = Path.home() / ".claude" / "personas"
CATEGORIES = ["dev", "education", "finance"]


def load_persona(persona_id: str) -> Optional[Dict]:
    """모든 카테고리에서 페르소나 검색 및 로드"""
    for category in CATEGORIES:
        file_path = PERSONAS_DIR / category / f"{persona_id}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    return None


def get_all_personas() -> Dict[str, List[str]]:
    """모든 카테고리의 페르소나 ID 목록 반환"""
    result: Dict[str, List[str]] = {}
    for category in CATEGORIES:
        cat_dir = PERSONAS_DIR / category
        if cat_dir.exists():
            result[category] = sorted(f.stem for f in cat_dir.glob("*.json"))
    # ideation은 서브카테고리 구조
    ideation_dir = PERSONAS_DIR / "ideation"
    if ideation_dir.exists():
        ids = []
        for f in ideation_dir.glob("*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            ids.extend(p.get("id", "") for p in data.get("personas", []))
        result["ideation"] = sorted(ids)
    return result


def load_ideation_personas(category: str) -> List[Dict]:
    """Ideation 페르소나 카테고리 로드"""
    file_path = PERSONAS_DIR / "ideation" / f"{category}.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f).get("personas", [])
    return []


def get_persona_by_keyword(keyword: str) -> List[Dict]:
    """키워드로 전체 카테고리 페르소나 검색"""
    if not keyword or len(keyword.strip()) < 2:
        return []
    matches = []
    words = [w.lower() for w in keyword.lower().split() if len(w) >= 2]
    if not words:
        return []
    for category in CATEGORIES:
        cat_dir = PERSONAS_DIR / category
        if not cat_dir.exists():
            continue
        for f in cat_dir.glob("*.json"):
            persona = json.loads(f.read_text(encoding="utf-8"))
            keys = [k.lower() for k in persona.get("keywords", [])]
            if any(w in k or k in w for w in words for k in keys if len(k) >= 2):
                matches.append(persona)
    return matches


def activate_personas(context: str, file_path: str = None) -> List[Dict]:
    """컨텍스트 기반 페르소나 활성화 (전체 카테고리)"""
    activated: List[Dict] = []
    index_file = PERSONAS_DIR / "index.json"
    if not index_file.exists():
        return activated

    index = json.loads(index_file.read_text(encoding="utf-8"))
    rules = index.get("activation_rules", {})
    max_concurrent = rules.get("max_concurrent", 3)
    ctx_lower = context.lower()

    # 강제 활성화 (전체 카테고리 검색)
    for pid, cfg in rules.get("forced_activation", {}).items():
        if any(kw in ctx_lower for kw in cfg.get("keywords", [])):
            persona = load_persona(pid)
            if persona and persona not in activated:
                activated.append(persona)

    # 파일 패턴 기반 활성화
    if file_path:
        for rule in rules.get("context_based", []):
            pattern = rule.get("pattern", "")
            if pattern in file_path or file_path.endswith(pattern.replace("*", "")):
                for pid in rule.get("personas", []):
                    if len(activated) >= max_concurrent:
                        break
                    persona = load_persona(pid)
                    if persona and persona not in activated:
                        activated.append(persona)

    # 키워드 기반 활성화
    for persona in get_persona_by_keyword(context):
        if len(activated) >= max_concurrent:
            break
        if persona not in activated:
            activated.append(persona)

    return activated[:max_concurrent]


def print_persona_info(persona: Dict):
    """페르소나 정보 출력"""
    print(f"  {persona.get('name', 'Unknown')} ({persona.get('id', '')})")
    print(f"    역할: {persona.get('role', '')}")
    if persona.get("skills"):
        print(f"    스킬: {', '.join(persona['skills'][:3])}")


def list_all_personas():
    """모든 페르소나 목록 출력"""
    all_personas = get_all_personas()
    for category, ids in all_personas.items():
        print(f"\n=== {category} ({len(ids)}개) ===")
        if category == "ideation":
            subcats = ["business", "marketing", "innovation", "design", "validation", "research", "special"]
            for sub in subcats:
                personas = load_ideation_personas(sub)
                if personas:
                    print(f"  [{sub}]")
                    for p in personas:
                        print(f"    - {p.get('id', '')}: {p.get('name', '')}")
        else:
            for pid in ids:
                persona = load_persona(pid)
                if persona:
                    print(f"  - {pid}: {persona.get('name', '')}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            list_all_personas()
        elif cmd == "get" and len(sys.argv) > 2:
            persona = load_persona(sys.argv[2])
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
