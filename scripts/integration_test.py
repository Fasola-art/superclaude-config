#!/usr/bin/env python3
"""
SuperClaude v2.0.9 통합 테스트
Mac Studio Ultra M2 시스템 검증
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

CLAUDE_DIR = Path.home() / '.claude'

# 테스트 결과
results = {
    'timestamp': datetime.now().isoformat(),
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'tests': []
}


def log_test(name: str, passed: bool, message: str = '', skip: bool = False):
    """테스트 결과 기록"""
    status = 'SKIP' if skip else ('PASS' if passed else 'FAIL')
    icon = '⏭️' if skip else ('✅' if passed else '❌')

    print(f"  {icon} {name}: {message}")

    if skip:
        results['skipped'] += 1
    elif passed:
        results['passed'] += 1
    else:
        results['failed'] += 1

    results['tests'].append({
        'name': name,
        'status': status,
        'message': message
    })


def test_folder_structure() -> bool:
    """폴더 구조 테스트"""
    print("\n📁 폴더 구조 테스트")
    print("-" * 40)

    required_folders = [
        'agents', 'archive', 'backups', 'cache', 'cheatsheets',
        'chrome', 'commands', 'debug', 'docs', 'error-kb',
        'file-history', 'hooks', 'ide', 'jarvis', 'logs',
        'mcp-router', 'output-styles', 'patterns', 'personas',
        'plans', 'plugins', 'profiles', 'projects', 'prompts',
        'references', 'scripts', 'session-env', 'sessions',
        'shell-snapshots', 'skills', 'statsig', 'telemetry',
        'templates', 'todos', 'modules'
    ]

    all_passed = True
    for folder in required_folders:
        path = CLAUDE_DIR / folder
        exists = path.exists() and path.is_dir()
        log_test(f"폴더: {folder}", exists, 'OK' if exists else '없음')
        if not exists:
            all_passed = False

    return all_passed


def test_config_files() -> bool:
    """설정 파일 테스트"""
    print("\n⚙️ 설정 파일 테스트")
    print("-" * 40)

    config_files = [
        ('settings.json', True),
        ('mcp.json', True),
        ('VERSION', True),
        ('CLAUDE.md', True),
        ('superclaude-metadata.json', False),
    ]

    all_passed = True
    for filename, required in config_files:
        path = CLAUDE_DIR / filename
        exists = path.exists()

        if exists:
            # JSON 파일 유효성 검사
            if filename.endswith('.json'):
                try:
                    json.loads(path.read_text())
                    log_test(f"파일: {filename}", True, 'OK (유효한 JSON)')
                except json.JSONDecodeError:
                    log_test(f"파일: {filename}", False, 'JSON 파싱 오류')
                    all_passed = False
            else:
                log_test(f"파일: {filename}", True, 'OK')
        else:
            if required:
                log_test(f"파일: {filename}", False, '필수 파일 없음')
                all_passed = False
            else:
                log_test(f"파일: {filename}", True, '선택적 파일 (없음)', skip=True)

    return all_passed


def test_hooks() -> bool:
    """Hooks 테스트"""
    print("\n🪝 Hooks 테스트")
    print("-" * 40)

    hooks = {
        'UserPromptSubmit': [
            'keyword-detector.js',
            'persona-activator.js',
            'context-cleaner.js',
            'plan-mode-analyzer.py',
            'todo-continuation-enforcer.js',
            'auto-update-checker.js',
            'jarvis-morning-briefing.py'
        ],
        'PreToolUse': [
            'writer-reviewer-hook.py',
            'error-warning-hook.js'
        ],
        'PostToolUse': [
            'error-auto-resolver.js',
            'ralph-loop-checker.js',
            'session-snapshot.js',
            'jarvis-work-tracker.py',
            'jarvis-task-completion.py',
            'quality-gate.js',
            'pattern-tracker.js',
            'background-notification.js'
        ]
    }

    all_passed = True
    total_hooks = 0
    found_hooks = 0

    for trigger, hook_files in hooks.items():
        for hook_file in hook_files:
            total_hooks += 1
            path = CLAUDE_DIR / 'hooks' / trigger / hook_file
            exists = path.exists()
            executable = os.access(path, os.X_OK) if exists else False

            if exists and executable:
                log_test(f"{trigger}/{hook_file}", True, 'OK (실행 가능)')
                found_hooks += 1
            elif exists:
                log_test(f"{trigger}/{hook_file}", False, '실행 권한 없음')
                all_passed = False
            else:
                log_test(f"{trigger}/{hook_file}", False, '파일 없음')
                all_passed = False

    print(f"\n  총 {found_hooks}/{total_hooks} Hooks 확인됨")
    return all_passed


def test_mcp_router() -> bool:
    """MCP Router 테스트"""
    print("\n🔀 MCP Router 테스트")
    print("-" * 40)

    router_files = ['server.py', 'client.py', 'README.md']
    all_passed = True

    for filename in router_files:
        path = CLAUDE_DIR / 'mcp-router' / filename
        exists = path.exists()
        log_test(f"MCP Router: {filename}", exists, 'OK' if exists else '없음')
        if not exists:
            all_passed = False

    # Python 문법 검사
    server_path = CLAUDE_DIR / 'mcp-router' / 'server.py'
    if server_path.exists():
        try:
            result = subprocess.run(
                ['python3', '-m', 'py_compile', str(server_path)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                log_test("MCP Router: 문법 검사", True, 'Python 문법 OK')
            else:
                log_test("MCP Router: 문법 검사", False, result.stderr[:100])
                all_passed = False
        except Exception as e:
            log_test("MCP Router: 문법 검사", False, str(e)[:100])

    return all_passed


def test_modules() -> bool:
    """모듈 테스트"""
    print("\n📦 모듈 테스트")
    print("-" * 40)

    modules = {
        'trading': ['trading_module.py', 'config.json', 'TRADING.md'],
        'news-collector': ['news_module.py', 'config.json', 'NEWS.md'],
        'realtime-analysis': ['realtime_module.py', 'config.json', 'REALTIME.md']
    }

    all_passed = True

    for module_name, files in modules.items():
        print(f"\n  [{module_name}]")
        for filename in files:
            path = CLAUDE_DIR / 'modules' / module_name / filename
            exists = path.exists()
            log_test(f"  {filename}", exists, 'OK' if exists else '없음')
            if not exists:
                all_passed = False

        # Python 모듈 문법 검사
        module_path = CLAUDE_DIR / 'modules' / module_name / f"{module_name.replace('-', '_')}_module.py"
        if not module_path.exists():
            # Alternative naming
            for f in (CLAUDE_DIR / 'modules' / module_name).glob('*_module.py'):
                module_path = f
                break

        if module_path.exists():
            try:
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', str(module_path)],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    log_test(f"  문법 검사", True, 'Python 문법 OK')
                else:
                    log_test(f"  문법 검사", False, result.stderr[:100])
                    all_passed = False
            except Exception as e:
                log_test(f"  문법 검사", False, str(e)[:100])

    return all_passed


def test_docs() -> bool:
    """문서 테스트"""
    print("\n📄 문서 테스트")
    print("-" * 40)

    docs = [
        'ARCH-PRINCIPLES.md',
        'QUALITY-GATES.md',
        'HOOKS-SYSTEM.md',
        'PERSONAS.md',
        'PLAN-MODE.md',
        'PROJECT-PLANNING.md',
        'VIBE-WORKFLOW.md',
        'SETTINGS-GUIDE.md'
    ]

    all_passed = True
    for doc in docs:
        path = CLAUDE_DIR / 'docs' / doc
        exists = path.exists()
        log_test(f"문서: {doc}", exists, 'OK' if exists else '없음')
        if not exists:
            all_passed = False

    return all_passed


def test_trading_module() -> bool:
    """Trading 모듈 기능 테스트"""
    print("\n📈 Trading 모듈 기능 테스트")
    print("-" * 40)

    try:
        sys.path.insert(0, str(CLAUDE_DIR / 'modules' / 'trading'))
        from trading_module import Indicators, analyze_market
        import random
        from datetime import timedelta

        # 지표 계산 테스트
        prices = [100 + random.uniform(-5, 5) for _ in range(50)]

        sma = Indicators.sma(prices, 20)
        log_test("SMA 계산", len(sma) > 0, f'{len(sma)}개 값 생성')

        rsi = Indicators.rsi(prices, 14)
        log_test("RSI 계산", len(rsi) > 0 and all(0 <= r <= 100 for r in rsi),
                f'{len(rsi)}개 값 생성')

        macd_line, signal_line, histogram = Indicators.macd(prices)
        log_test("MACD 계산", len(macd_line) > 0, f'{len(macd_line)}개 값 생성')

        # 시장 분석 테스트
        test_candles = []
        base_price = 100
        for i in range(100):
            change = random.uniform(-2, 2)
            test_candles.append({
                'timestamp': (datetime.now() - timedelta(hours=100-i)).isoformat(),
                'open': base_price,
                'high': base_price + abs(change),
                'low': base_price - abs(change),
                'close': base_price + change,
                'volume': random.uniform(1000, 10000)
            })
            base_price += change

        signal = analyze_market('TEST/USD', test_candles)
        log_test("시장 분석", signal is not None and 'signal_type' in signal,
                f"시그널: {signal.get('signal_type', 'N/A')}")

        return True

    except Exception as e:
        log_test("Trading 모듈", False, str(e)[:100])
        return False


def test_news_module() -> bool:
    """News Collector 모듈 기능 테스트"""
    print("\n📰 News Collector 모듈 기능 테스트")
    print("-" * 40)

    try:
        sys.path.insert(0, str(CLAUDE_DIR / 'modules' / 'news-collector'))
        from news_module import NewsCollector, collect_news

        collector = NewsCollector()

        # 키워드 추출 테스트
        keywords = collector.extract_keywords("OpenAI announces GPT-5 with breakthrough capabilities in AI")
        log_test("키워드 추출", len(keywords) > 0, f'{len(keywords)}개 키워드')

        # 카테고리 감지 테스트
        category = collector.detect_category("Bitcoin surges above $100,000")
        log_test("카테고리 감지", category is not None, f'카테고리: {category.value}')

        # 감성 분석 테스트
        sentiment = collector.simple_sentiment("Great success and positive growth")
        log_test("감성 분석", -1 <= sentiment <= 1, f'감성 점수: {sentiment}')

        # 뉴스 수집 테스트
        test_articles = [{
            'title': 'Test AI Article',
            'url': 'https://example.com/test',
            'source': 'test',
            'summary': 'This is a test article about AI technology.'
        }]
        collected = collect_news(test_articles)
        log_test("뉴스 수집", len(collected) > 0, f'{len(collected)}개 기사 처리')

        return True

    except Exception as e:
        log_test("News 모듈", False, str(e)[:100])
        return False


def test_realtime_module() -> bool:
    """Realtime Analysis 모듈 기능 테스트"""
    print("\n⚡ Realtime Analysis 모듈 기능 테스트")
    print("-" * 40)

    try:
        sys.path.insert(0, str(CLAUDE_DIR / 'modules' / 'realtime-analysis'))
        from realtime_module import process_data, get_analysis, get_dashboard
        import random

        # 데이터 처리 테스트
        test_data = [
            {
                'timestamp': datetime.now().isoformat(),
                'type': 'price',
                'symbol': 'TEST/USD',
                'value': 100 + random.uniform(-5, 5)
            }
            for _ in range(50)
        ]
        processed = process_data(test_data)
        log_test("데이터 처리", len(processed) == 50, f'{len(processed)}개 처리됨')

        # 분석 테스트
        analysis = get_analysis('TEST/USD')
        log_test("실시간 분석", 'trend' in analysis and 'confidence' in analysis,
                f"추세: {analysis.get('trend', 'N/A')}")

        # 대시보드 테스트
        dashboard = get_dashboard(['TEST/USD'])
        log_test("대시보드 생성", 'symbols' in dashboard, 'OK')

        return True

    except Exception as e:
        log_test("Realtime 모듈", False, str(e)[:100])
        return False


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 50)
    print("🧪 SuperClaude v2.0.9 통합 테스트")
    print(f"   Mac Studio Ultra M2 시스템 검증")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    tests = [
        ('폴더 구조', test_folder_structure),
        ('설정 파일', test_config_files),
        ('Hooks', test_hooks),
        ('MCP Router', test_mcp_router),
        ('모듈', test_modules),
        ('문서', test_docs),
        ('Trading 기능', test_trading_module),
        ('News 기능', test_news_module),
        ('Realtime 기능', test_realtime_module),
    ]

    for name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"\n❌ {name} 테스트 중 오류: {e}")
            results['failed'] += 1

    # 결과 요약
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)

    total = results['passed'] + results['failed'] + results['skipped']
    print(f"\n  ✅ 통과: {results['passed']}")
    print(f"  ❌ 실패: {results['failed']}")
    print(f"  ⏭️ 스킵: {results['skipped']}")
    print(f"  📋 총계: {total}")

    pass_rate = (results['passed'] / (total - results['skipped']) * 100) if (total - results['skipped']) > 0 else 0
    print(f"\n  📈 통과율: {pass_rate:.1f}%")

    # 결과 저장
    results_path = CLAUDE_DIR / 'logs' / 'test_results.json'
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n  💾 결과 저장: {results_path}")

    if results['failed'] == 0:
        print("\n🎉 모든 테스트 통과!")
        return 0
    else:
        print(f"\n⚠️ {results['failed']}개 테스트 실패")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
