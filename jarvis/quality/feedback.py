#!/usr/bin/env python3
"""
실패한 Quality Gate에 대한 피드백 생성

Claude가 자동 수정할 수 있도록 구조화된 피드백 출력
"""

from __future__ import annotations

from .types import GateResult, GateStatus


def generate_feedback(result: GateResult, attempt: int, max_retries: int) -> str:
    """
    실패한 게이트에 대한 수정 피드백 생성

    Args:
        result: 게이트 실행 결과
        attempt: 현재 시도 횟수
        max_retries: 최대 재시도 횟수

    Returns:
        Claude에게 전달할 피드백 문자열
    """
    if result.passed:
        return f"✅ Quality Gate 통과 (점수: {result.score:.0%})"

    failed = result.failed_checks
    if not failed:
        return ""

    lines: list[str] = [
        f"⚠️ Quality Gate 실패 [{attempt}/{max_retries}] (점수: {result.score:.0%})",
        f"   파일: {result.file_path} ({result.file_type})",
    ]

    for check in failed:
        lines.append(f"   ❌ {check.name}: {check.message}")
        if check.output:
            # 출력에서 핵심 에러 라인만 추출 (최대 3줄)
            error_lines = _extract_error_lines(check.output, max_lines=3)
            for line in error_lines:
                lines.append(f"      {line}")

    # 수정 지시
    if attempt < max_retries:
        lines.append(f"   → 위 오류를 수정해주세요 (잔여 시도: {max_retries - attempt}회)")
    else:
        lines.append("   → 최대 재시도 횟수 도달. 수동 확인 필요.")

    return "\n".join(lines)


def _extract_error_lines(output: str, max_lines: int = 3) -> list[str]:
    """출력에서 핵심 에러 라인 추출"""
    if not output:
        return []

    lines = output.strip().split("\n")

    # Error/error/실패 키워드 포함 라인 우선
    error_lines = [
        line.strip() for line in lines
        if any(kw in line.lower() for kw in ["error", "err", "fail", "실패", "invalid"])
    ]

    if error_lines:
        return error_lines[:max_lines]

    # 키워드 없으면 처음 N줄 반환
    return [line.strip() for line in lines[:max_lines]]


def format_summary(result: GateResult) -> str:
    """간단한 1줄 요약 (hook 출력용)"""
    if result.passed:
        return f"QG:✅ {result.file_type} ({result.score:.0%})"

    failed_names = [c.name for c in result.failed_checks]
    return f"QG:❌ {result.file_type} ({result.score:.0%}) 실패: {','.join(failed_names)}"
