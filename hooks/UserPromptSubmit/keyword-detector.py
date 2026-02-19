#!/usr/bin/env python3
"""
Vibe/Mode Keyword Detection Hook
- Detect 13 Vibe Keywords
- Detect 4 Mode Keywords
- Trigger corresponding actions
"""

import sys
import json
import re

# Vibe Keywords (13)
VIBE_KEYWORDS = {
    # Execution control
    "quick": {"aliases": ["qk", "fast"], "action": "skip_validation"},
    "experiment": {"aliases": ["exp"], "action": "snapshot_experiment"},
    "parallel": {"aliases": ["para"], "action": "parallel_agents"},
    # Modification/Recovery
    "fix": {"aliases": [], "action": "error_kb_healing"},
    "undo": {"aliases": ["rollback"], "action": "rollback_snapshot"},
    "continue": {"aliases": ["cont"], "action": "continue_state"},
    # Verification
    "verify": {"aliases": ["chk", "check"], "action": "full_validation"},
    "test": {"aliases": ["tst"], "action": "run_tests"},
    # Deploy/Cleanup
    "deploy": {"aliases": ["dep"], "action": "deploy_checklist"},
    "cleanup": {"aliases": ["clean"], "action": "code_cleanup"},
    # Analysis/Planning
    "performance": {"aliases": ["perf"], "action": "performance_analysis"},
    "plan": {"aliases": [], "action": "planning_docs"},
    "analyze": {"aliases": ["map"], "action": "codebase_analysis"},
}

# Mode Keywords (4)
MODE_KEYWORDS = {
    "ultrawork": {"aliases": ["ulw"], "personas": ["explorer", "librarian", "analyzer"]},
    "deepsearch": {"aliases": ["ds"], "personas": ["explorer"]},
    "strategic": {"aliases": ["str"], "personas": ["architect"]},
    "visual": {"aliases": ["vis"], "personas": ["multimodal", "frontend"]},
}

def detect_keywords(prompt: str) -> dict:
    """Detect keywords from prompt"""
    prompt_lower = prompt.lower()
    result = {
        "vibe": [],
        "mode": [],
        "actions": [],
        "personas": []
    }

    # Check Vibe keywords
    for keyword, config in VIBE_KEYWORDS.items():
        all_forms = [keyword] + config.get("aliases", [])
        for form in all_forms:
            if form in prompt_lower:
                result["vibe"].append(keyword)
                result["actions"].append(config["action"])
                break

    # Check Mode keywords
    for keyword, config in MODE_KEYWORDS.items():
        all_forms = [keyword] + config.get("aliases", [])
        for form in all_forms:
            if form in prompt_lower:
                result["mode"].append(keyword)
                result["personas"].extend(config["personas"])
                break

    # Remove duplicates
    result["personas"] = list(set(result["personas"]))

    return result

def main():
    # Get prompt from environment variable
    import os
    prompt = os.environ.get("PROMPT", "")

    if not prompt:
        # Try reading from stdin
        if not sys.stdin.isatty():
            prompt = sys.stdin.read()

    if not prompt:
        return

    detected = detect_keywords(prompt)

    if detected["vibe"] or detected["mode"]:
        parts = []
        if detected["vibe"]:
            parts.append(f"vibe:{','.join(detected['vibe'])}")
        if detected["mode"]:
            parts.append(f"mode:{','.join(detected['mode'])}")
        print(f"Detected: {' | '.join(parts)}")

if __name__ == "__main__":
    main()
