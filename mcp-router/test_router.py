#!/usr/bin/env python3
"""MCP 라우터 전체 테스트"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from server import MCPRouter

async def test_router():
    """라우터 전체 테스트"""
    print("=" * 50)
    print("MCP Router 전체 테스트")
    print("=" * 50)

    router = MCPRouter()

    print("\n[1] 라우터 시작...")
    await router.start()

    print("\n[2] 상태 리포트:")
    report = router.get_status_report()
    print(f"  - 총 서버: {report['totalServers']}")
    print(f"  - 정상 서버: {report['healthyServers']}")
    print(f"  - 총 도구: {report['totalTools']}")

    for name, server in report['servers'].items():
        print(f"\n  [{name}]")
        print(f"    상태: {server['status']}")
        print(f"    도구: {len(server['tools'])}개")
        if server['tools']:
            print(f"    목록: {', '.join(server['tools'][:5])}...")

    print("\n[3] 도구 호출 테스트...")

    # list_directory 테스트
    print("\n  >> list_directory('/Users/reim/.claude')")
    result = await router.call_tool('list_directory', {'path': '/Users/reim/.claude'})
    if result['success']:
        content = result['result'].get('content', [])
        if content:
            text = content[0].get('text', '')[:500]
            print(f"  결과: {text[:300]}...")
    else:
        print(f"  오류: {result.get('error')}")

    # read_file 테스트
    print("\n  >> read_file('/Users/reim/.claude/VERSION')")
    result = await router.call_tool('read_file', {'path': '/Users/reim/.claude/VERSION'})
    if result['success']:
        content = result['result'].get('content', [])
        if content:
            text = content[0].get('text', '')
            print(f"  결과: {text}")
    else:
        print(f"  오류: {result.get('error')}")

    print("\n[4] 헬스체크...")
    await router.check_all_servers()
    report = router.get_status_report()
    print(f"  정상: {report['healthyServers']}/{report['totalServers']}")

    print("\n[5] 라우터 종료...")
    await router.stop()

    print("\n" + "=" * 50)
    print("✅ MCP Router 테스트 완료!")
    print("=" * 50)

    return True

if __name__ == '__main__':
    try:
        asyncio.run(test_router())
    except KeyboardInterrupt:
        print("\n중단됨")
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
