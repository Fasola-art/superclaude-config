#!/usr/bin/env python3
"""
JARVIS Test Suite - 래퍼

원본은 tests/archive/test_jarvis_v1.py로 아카이브됨.
실제 테스트는 test_comprehensive.py에서 실행.
"""

import sys
import subprocess
from pathlib import Path


def main() -> int:
    """test_comprehensive.py로 테스트 위임"""
    test_file = Path(__file__).parent / "test_comprehensive.py"

    if not test_file.exists():
        print("test_comprehensive.py not found")
        return 1

    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(test_file)],
        cwd=str(test_file.parent),
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
