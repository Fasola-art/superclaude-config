#!/usr/bin/env python3
"""
SuperClaude integration test (Windows-safe)
- Verifies folder/config/hooks/module syntax
- Uses active hook commands from settings.json
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CLAUDE_DIR = Path.home() / ".claude"
PYTHON = sys.executable

results = {
    "timestamp": datetime.now().isoformat(),
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "tests": [],
}


def log_test(name: str, passed: bool, message: str = "", skip: bool = False) -> None:
    status = "SKIP" if skip else ("PASS" if passed else "FAIL")
    icon = "[SKIP]" if skip else ("[PASS]" if passed else "[FAIL]")
    print(f"  {icon} {name}: {message}")

    if skip:
        results["skipped"] += 1
    elif passed:
        results["passed"] += 1
    else:
        results["failed"] += 1

    results["tests"].append({"name": name, "status": status, "message": message})


def test_folder_structure() -> bool:
    print("\n[1] Folder structure")
    print("-" * 40)

    required = [
        "agents", "commands", "docs", "hooks", "jarvis", "mcp-router", "modules",
        "patterns", "personas", "scripts", "skills", "templates",
    ]

    ok = True
    for folder in required:
        exists = (CLAUDE_DIR / folder).is_dir()
        log_test(f"folder:{folder}", exists, "OK" if exists else "missing")
        ok = ok and exists
    return ok


def test_config_files() -> bool:
    print("\n[2] Config files")
    print("-" * 40)

    files = [
        ("settings.json", True),
        ("mcp.json", True),
        ("VERSION", True),
        ("CLAUDE.md", True),
        ("superclaude-metadata.json", False),
    ]

    ok = True
    for name, required in files:
        p = CLAUDE_DIR / name
        if not p.exists():
            if required:
                log_test(f"file:{name}", False, "missing")
                ok = False
            else:
                log_test(f"file:{name}", True, "optional-missing", skip=True)
            continue

        if name.endswith(".json"):
            try:
                json.loads(p.read_text(encoding="utf-8"))
                log_test(f"file:{name}", True, "valid json")
            except Exception as exc:
                log_test(f"file:{name}", False, f"invalid json: {exc}")
                ok = False
        else:
            log_test(f"file:{name}", True, "OK")

    return ok


def _extract_hook_command_paths() -> List[Path]:
    settings_path = CLAUDE_DIR / "settings.json"
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    paths: List[Path] = []

    hooks = data.get("hooks", {})
    for trigger_items in hooks.values():
        for item in trigger_items:
            for hk in item.get("hooks", []):
                cmd = hk.get("command", "").strip()
                if not cmd:
                    continue
                if cmd.startswith("python "):
                    path_str = cmd[len("python "):].strip().strip('"')
                    paths.append(Path(path_str).expanduser())
                elif cmd.startswith("python3 "):
                    path_str = cmd[len("python3 "):].strip().strip('"')
                    paths.append(Path(path_str).expanduser())
    return paths


def test_hooks() -> bool:
    print("\n[3] Hooks (from settings.json)")
    print("-" * 40)

    ok = True
    hook_paths = _extract_hook_command_paths()
    if not hook_paths:
        log_test("hooks:discovery", False, "no hook commands found")
        return False

    for hp in hook_paths:
        exists = hp.exists()
        log_test(f"hook:{hp}", exists, "OK" if exists else "missing")
        ok = ok and exists

    log_test("hooks:count", True, f"{len(hook_paths)} commands discovered")
    return ok


def _py_compile(path: Path) -> tuple[bool, str]:
    result = subprocess.run([PYTHON, "-m", "py_compile", str(path)], capture_output=True, text=True)
    if result.returncode == 0:
        return True, "syntax OK"
    return False, (result.stderr or result.stdout).strip()[:200]


def test_mcp_router() -> bool:
    print("\n[4] MCP router")
    print("-" * 40)

    ok = True
    for name in ["server.py", "client.py", "README.md"]:
        p = CLAUDE_DIR / "mcp-router" / name
        exists = p.exists()
        log_test(f"mcp-router:{name}", exists, "OK" if exists else "missing")
        ok = ok and exists

    server_py = CLAUDE_DIR / "mcp-router" / "server.py"
    if server_py.exists():
        passed, msg = _py_compile(server_py)
        log_test("mcp-router:py_compile", passed, msg)
        ok = ok and passed

    return ok


def test_modules() -> bool:
    print("\n[5] Modules")
    print("-" * 40)

    module_specs = {
        "trading": ["trading_module.py", "config.json", "TRADING.md"],
        "news-collector": ["news_module.py", "config.json", "NEWS.md"],
        "realtime-analysis": ["realtime_module.py", "config.json", "REALTIME.md"],
    }

    ok = True
    for mod, names in module_specs.items():
        for name in names:
            p = CLAUDE_DIR / "modules" / mod / name
            exists = p.exists()
            log_test(f"module:{mod}/{name}", exists, "OK" if exists else "missing")
            ok = ok and exists

        mod_py = CLAUDE_DIR / "modules" / mod / f"{mod.replace('-', '_')}_module.py"
        if not mod_py.exists():
            candidates = list((CLAUDE_DIR / "modules" / mod).glob("*_module.py"))
            mod_py = candidates[0] if candidates else Path()

        if mod_py and mod_py.exists():
            passed, msg = _py_compile(mod_py)
            log_test(f"module:{mod}/py_compile", passed, msg)
            ok = ok and passed

    return ok


def test_docs() -> bool:
    print("\n[6] Docs")
    print("-" * 40)

    docs = [
        "ARCH-PRINCIPLES.md", "QUALITY-GATES.md", "HOOKS-SYSTEM.md",
        "PERSONAS.md", "PLAN-MODE.md", "PROJECT-PLANNING.md", "VIBE-WORKFLOW.md",
    ]

    ok = True
    for doc in docs:
        primary = CLAUDE_DIR / "docs" / doc
        archived = CLAUDE_DIR / "docs" / "archive" / doc
        exists = primary.exists() or archived.exists()
        msg = "OK (docs)" if primary.exists() else ("OK (docs/archive)" if archived.exists() else "missing")
        log_test(f"doc:{doc}", exists, msg)
        ok = ok and exists

    return ok


def run_all_tests() -> int:
    print("=" * 56)
    print("SuperClaude v2.0.9 integration test")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 56)

    tests: List[tuple[str, Callable[[], bool]]] = [
        ("folder", test_folder_structure),
        ("config", test_config_files),
        ("hooks", test_hooks),
        ("mcp-router", test_mcp_router),
        ("modules", test_modules),
        ("docs", test_docs),
    ]

    for name, fn in tests:
        try:
            fn()
        except Exception as exc:
            log_test(f"test:{name}", False, f"exception: {exc}")

    print("\n" + "=" * 56)
    total = results["passed"] + results["failed"] + results["skipped"]
    effective = max(1, total - results["skipped"])
    rate = (results["passed"] / effective) * 100
    print(f"passed={results['passed']} failed={results['failed']} skipped={results['skipped']} total={total}")
    print(f"pass_rate={rate:.1f}%")

    out = CLAUDE_DIR / "logs" / "test_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"saved: {out}")

    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run_all_tests())
