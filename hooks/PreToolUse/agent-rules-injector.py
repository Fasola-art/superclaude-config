#!/usr/bin/env python3
"""Task tool 호출 시 에이전트에 필수 규칙 자동 주입

Hook Type: PreToolUse
Matcher: Task
목적: 서브 에이전트가 CLAUDE.md 규칙을 준수하도록 강제

출력: Plain text (exit 0) → 컨텍스트에 자동 주입됨
"""

import json
import sys


def get_module_rules(prompt: str) -> str:
    """프롬프트에서 모듈 키워드 감지 후 관련 규칙 반환"""
    prompt_lower = prompt.lower()
    rules = []

    # trading 모듈 관련 키워드
    trading_keywords = ['trading', 'trade', '트레이딩', '매매', 'strategy', '전략',
                        'indicator', '지표', 'backtest', '백테스트']
    if any(kw in prompt_lower for kw in trading_keywords):
        rules.append("""
[TRADING MODULE]
- 기존 구조: C:/Users/MSI/.claude/modules/trading/
  - strategies/: 전략 파일 (base_strategy.py 상속 필수)
  - indicators/: 기술 지표
  - data_sources/: 데이터 소스
- 설정: config.py, config.json 참조""")

    # sql-trading 모듈 관련 키워드
    sql_keywords = ['sql', 'database', 'db', '쿼리', 'query', 'schema',
                    'postgresql', 'postgres', 'dashboard', '대시보드']
    if any(kw in prompt_lower for kw in sql_keywords):
        rules.append("""
[SQL-TRADING MODULE]
- DB: claude_mcp (PostgreSQL)
- 스키마: C:/Users/MSI/.claude/modules/sql-trading/schema.sql
- 쿼리: queries/ 폴더, 대시보드: dashboard/ 폴더""")

    return '\n'.join(rules)


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, Exception):
        sys.exit(0)  # 파싱 실패 시 조용히 종료

    tool_name = input_data.get("tool_name", "")

    # Task tool일 때만 실행
    if tool_name != "Task":
        sys.exit(0)

    # 에이전트 프롬프트 추출
    tool_input = input_data.get("tool_input", {})
    prompt = tool_input.get("prompt", "")

    # 기본 규칙 (Plain text로 출력 → 컨텍스트 주입)
    base_rules = """
═══════════════════════════════════════════════════════
[MANDATORY RULES - 이 에이전트는 반드시 준수]
═══════════════════════════════════════════════════════
1. 파일 생성 시 50~120줄 범위 유지 (초과 시 분할, 미달 시 병합)
2. Python: 타입 힌트 필수, docstring 필수
3. 기존 코드 참조: C:/Users/MSI/.claude/modules/
4. 응답 언어: 한국어
5. No stub/placeholder code - 완전한 구현만
═══════════════════════════════════════════════════════"""

    # 모듈별 추가 규칙
    module_rules = get_module_rules(prompt)

    # Plain text 출력 (stdout → 컨텍스트에 주입됨)
    output = base_rules
    if module_rules:
        output += module_rules

    print(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
