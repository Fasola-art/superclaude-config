#!/usr/bin/env python3
"""
Persona Auto-Activation Hook
- Select appropriate persona through context analysis
- Activate up to 3 simultaneously
"""

import os
import sys
import re

# Persona keyword mapping
PERSONA_KEYWORDS = {
    "security": {
        "keywords": ["auth", "login", "password", "token", "jwt", "oauth", "security", "authentication", "permission"],
        "priority": 1
    },
    "architect": {
        "keywords": ["design", "architecture", "structure", "pattern", "system"],
        "priority": 2
    },
    "frontend": {
        "keywords": ["react", "vue", "css", "html", "component", "ui", "ux", "style"],
        "priority": 3
    },
    "backend": {
        "keywords": ["api", "server", "database", "db", "query", "rest", "graphql"],
        "priority": 3
    },
    "devops": {
        "keywords": ["docker", "k8s", "kubernetes", "ci", "cd", "deploy", "aws", "gcp"],
        "priority": 4
    },
    "performance": {
        "keywords": ["performance", "optimize", "speed", "memory"],
        "priority": 3
    },
    "tester": {
        "keywords": ["test", "jest", "vitest", "cypress", "e2e", "unit"],
        "priority": 4
    },
    "analyzer": {
        "keywords": ["analyze", "review", "examine"],
        "priority": 5
    },
    "explorer": {
        "keywords": ["find", "search", "where", "locate"],
        "priority": 5
    }
}

MAX_CONCURRENT = 3

def detect_personas(prompt: str) -> list:
    """Detect appropriate personas from prompt"""
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

    # Sort by priority and select top 3
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
        print(f"Personas: {','.join(names)}")

if __name__ == "__main__":
    main()
