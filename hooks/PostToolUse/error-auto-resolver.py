#!/usr/bin/env python3
"""
Error Auto-Resolver + Collector Hook (PostToolUse/Bash)

1. Bash 결과에서 에러 감지 (구체적 패턴 매칭)
2. error-success-map.json 기반 분류
3. pending/ 에 신규 에러 저장
4. resolved/ 에서 유사 에러 검색 → 해결책 제안
5. 최대 10회 자동 재시도 추적
"""

import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

KB_DIR = Path.home() / ".claude" / "error-kb"
PENDING = KB_DIR / "pending"
RESOLVED = KB_DIR / "resolved"
PATTERNS = KB_DIR / "patterns" / "error-success-map.json"
STATE = Path.home() / ".claude" / "cache" / "ralph-state.json"
MAX_RETRIES = 10
SIM_THRESHOLD = 0.70

# 에러 감지 패턴 (광범위한 "error" 대신 구체적 매칭)
ERROR_RE = re.compile(
    r"(?i)(?:^error:|^fatal:|traceback|syntaxerror|typeerror|referenceerror"
    r"|command not found|permission denied|ENOENT|ECONNREFUSED|EACCES"
    r"|Cannot find module|Module not found|TS\d{4}:|Build failed"
    r"|CONFLICT|MCP.*실패|npm ERR!|EPERM|ETIMEDOUT"
    r"|Hydration failed|Invalid hook call|Unhandled Runtime Error)",
    re.MULTILINE
)

# 에러 타입 → KB 카테고리 매핑
CAT_MAP = {
    "typescript_error": "typescript", "react_error": "react",
    "next_error": "nextjs", "mcp_error": "mcp", "git_error": "git",
    "module_not_found": "typescript", "build_error": "nextjs",
    "database_error": "mcp", "network_error": "mcp",
    "permission_error": "git", "lint_error": "typescript",
    "dependency_error": "typescript", "command_error": "git",
    "file_error": "typescript", "test_error": "typescript",
}


def detect_error(output: str) -> str | None:
    """에러 메시지 추출. 없으면 None"""
    m = ERROR_RE.search(output)
    if not m:
        return None
    start = output.rfind('\n', 0, m.start()) + 1
    end = output.find('\n', m.end())
    return output[start:end if end != -1 else len(output)].strip()


def classify(message: str) -> str:
    """에러 메시지 → 타입 분류 (quick_fix 정규식 우선 → 일반 분류)"""
    try:
        data = json.loads(PATTERNS.read_text(encoding='utf-8'))
        # 1차: quick_fixes 정규식 (가장 정확)
        for qf in data.get("quick_fixes", []):
            if re.search(qf.get("regex", ""), message, re.IGNORECASE):
                return qf["category"]
        # 2차: 일반 분류 (기술코드 3x 가중)
        best_type, best_score = "unknown", 0
        msg_lower = message.lower()
        for cls in data.get("error_classifications", []):
            score = sum(
                len(p) * (3 if any(c.isdigit() or c in "!@#" for c in p) else 1)
                for p in cls.get("patterns", []) if p.lower() in msg_lower
            )
            if score > best_score:
                best_type, best_score = cls["type"], score
        return best_type
    except Exception:
        return "unknown"


def save_pending(msg: str, raw: str, etype: str) -> str:
    """신규 에러 → pending/ 저장"""
    PENDING.mkdir(parents=True, exist_ok=True)
    eid = hashlib.md5(f"{etype}:{msg}".encode()).hexdigest()[:12]
    f = PENDING / f"{eid}.json"
    if f.exists() or (RESOLVED / f"{eid}.json").exists():
        return eid
    record = {
        "id": eid, "type": etype, "message": msg,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "raw_log": raw[:500], "created_at": datetime.now().isoformat(),
        "resolved": False, "resolution": None, "context": {}
    }
    f.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding='utf-8')
    return eid


def jaccard(a: str, b: str) -> float:
    """Jaccard 유사도"""
    s1, s2 = set(a.lower().split()), set(b.lower().split())
    return len(s1 & s2) / len(s1 | s2) if s1 and s2 else 0.0


def search_resolved(msg: str) -> list[dict]:
    """resolved/ 에서 유사 에러 검색"""
    if not RESOLVED.exists():
        return []
    hits = []
    for f in RESOLVED.glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding='utf-8'))
            sim = jaccard(msg, d.get("message", ""))
            if sim >= SIM_THRESHOLD:
                hits.append({"resolution": d.get("resolution"), "similarity": sim})
        except Exception:
            continue
    return sorted(hits, key=lambda x: x["similarity"], reverse=True)[:3]


def main():
    output = os.environ.get("CLAUDE_TOOL_OUTPUT", "")
    if not output:
        return

    error_msg = detect_error(output)
    if not error_msg:
        return

    etype = classify(error_msg)
    eid = save_pending(error_msg, output, etype)
    cat = CAT_MAP.get(etype, "unknown")

    # 재시도 추적
    try:
        state = json.loads(STATE.read_text(encoding='utf-8'))
    except Exception:
        state = {"retry_count": 0, "last_error": None}

    ehash = hashlib.md5(error_msg.encode()).hexdigest()[:12]
    if state.get("last_error") == ehash:
        state["retry_count"] += 1
    else:
        state["last_error"] = ehash
        state["retry_count"] = 1

    if state["retry_count"] > MAX_RETRIES:
        print(f"Ralph: {MAX_RETRIES}회 초과 → 수동 처리 필요")
        state["retry_count"] = 0

    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state), encoding='utf-8')

    if state["retry_count"] > MAX_RETRIES:
        return

    similar = search_resolved(error_msg)
    if similar:
        res = similar[0]["resolution"] or "해결 방법 확인 필요"
        print(f"Ralph:{state['retry_count']}/{MAX_RETRIES} [{cat}] sim:{similar[0]['similarity']:.0%} → {res[:60]}")
    else:
        print(f"Ralph:{state['retry_count']}/{MAX_RETRIES} [{cat}] 신규 에러 → pending/{eid}")


if __name__ == "__main__":
    main()
