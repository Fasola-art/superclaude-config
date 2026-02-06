#!/usr/bin/env python3
"""
파일 타입별 Quality Gate 실행기

지원 파일 타입: Python, TypeScript, Go
각 타입별 syntax + type check 실행 후 점수 계산
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from .types import CheckResult, GateResult, GateStatus

# 파일 타입별 게이트 정의
_GATE_COMMANDS: dict[str, list[dict[str, str]]] = {
    "python": [
        {"name": "syntax", "cmd": "python3 -m py_compile {file}", "weight": "0.50"},
        {"name": "type", "cmd": "python3 -m mypy --ignore-missing-imports {file}", "weight": "0.30"},
        {"name": "lint", "cmd": "python3 -m ruff check {file}", "weight": "0.20"},
    ],
    "typescript": [
        {"name": "syntax", "cmd": "npx tsc --noEmit --allowJs {file}", "weight": "0.50"},
        {"name": "lint", "cmd": "npx eslint {file}", "weight": "0.30"},
    ],
    "go": [
        {"name": "syntax", "cmd": "go vet {file}", "weight": "0.50"},
        {"name": "lint", "cmd": "golangci-lint run {file}", "weight": "0.30"},
    ],
}

# 확장자 → 파일 타입 매핑
_EXT_MAP: dict[str, str] = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "typescript",
    ".jsx": "typescript",
    ".go": "go",
}

# 스킵할 패턴
_SKIP_EXTENSIONS = frozenset([".json", ".md", ".env", ".yaml", ".yml", ".toml", ".txt", ".css", ".html"])


def _detect_file_type(file_path: str) -> str:
    """파일 확장자로 타입 감지"""
    ext = Path(file_path).suffix.lower()
    return _EXT_MAP.get(ext, "unknown")


def _run_command(cmd: str, timeout: int = 30) -> tuple[bool, str]:
    """명령어 실행 후 (성공여부, 출력) 반환"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout,
        )
        output = (result.stdout + result.stderr).strip()
        return result.returncode == 0, output[:500]  # 출력 500자 제한
    except subprocess.TimeoutExpired:
        return False, "타임아웃 (30초 초과)"
    except FileNotFoundError:
        return False, "명령어를 찾을 수 없음"
    except Exception as e:
        return False, str(e)[:200]


def get_gates_for_file(file_path: str) -> list[dict[str, str]]:
    """파일에 적용할 게이트 목록 반환"""
    file_type = _detect_file_type(file_path)
    return _GATE_COMMANDS.get(file_type, [])


def run_gates(file_path: str) -> GateResult:
    """
    파일에 대한 모든 Quality Gate 실행

    Args:
        file_path: 검사할 파일 경로

    Returns:
        GateResult (checks + score)
    """
    file_type = _detect_file_type(file_path)
    ext = Path(file_path).suffix.lower()

    # 스킵할 파일
    if ext in _SKIP_EXTENSIONS or file_type == "unknown":
        return GateResult(
            file_path=file_path, file_type=file_type,
            checks=[CheckResult(name="skip", status=GateStatus.SKIP, message="검사 대상 아님")],
            score=1.0,
        )

    gates = _GATE_COMMANDS.get(file_type, [])
    if not gates:
        return GateResult(file_path=file_path, file_type=file_type, score=1.0)

    checks: list[CheckResult] = []
    total_weight = 0.0
    passed_weight = 0.0

    for gate in gates:
        cmd = gate["cmd"].format(file=file_path)
        weight = float(gate["weight"])
        total_weight += weight

        success, output = _run_command(cmd)

        if success:
            checks.append(CheckResult(
                name=gate["name"], status=GateStatus.PASS, message="통과",
            ))
            passed_weight += weight
        else:
            checks.append(CheckResult(
                name=gate["name"], status=GateStatus.FAIL,
                message=f"{gate['name']} 실패", output=output,
            ))

    score = round(passed_weight / total_weight, 2) if total_weight > 0 else 1.0

    return GateResult(
        file_path=file_path, file_type=file_type,
        checks=checks, score=score,
    )
