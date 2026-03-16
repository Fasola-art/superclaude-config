#!/usr/bin/env python3
"""
지침 파일 동기화 스크립트
영어 지침 → 한글 사용자 가이드 자동 생성

사용법:
    python sync_user_guide.py              # 전체 동기화
    python sync_user_guide.py --file FILE  # 개별 파일 동기화
    python sync_user_guide.py --dry-run    # 미리보기 (실행 안 함)
"""

import argparse
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime


CLAUDE_DIR = Path.home() / ".claude"
USER_GUIDE_DIR = CLAUDE_DIR / "user-guide"
CREDENTIALS_FILE = CLAUDE_DIR / "credentials" / "api-keys.json"

# 동기화 대상 패턴
SYNC_PATTERNS = [
    "CLAUDE.md",
    "docs/*.md",
    "rules/**/*.md",
]

# 제외 패턴
EXCLUDE_PATTERNS = [
    "user-guide",
    "USER-GUIDE",
    "CHANGELOG",
]


def load_api_key() -> str:
    """API 키 로드"""
    with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
        keys = json.load(f)
    return keys['anthropic']['api_key']


def translate_to_korean(content: str, filename: str, api_key: str) -> str:
    """Claude Haiku로 한글 번역"""

    prompt = f"""Translate this Claude Code instruction file to Korean.

RULES:
1. Translate ALL text to Korean (including headers, descriptions, comments)
2. Keep code syntax, commands, filenames, technical terms in original
3. Keep markdown formatting intact
4. Keep the same structure and sections
5. Make it readable for Korean users

File: {filename}

Content:
{content}

Translate to Korean:"""

    payload = {
        "model": "claude-3-5-haiku-20241022",
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": prompt}]
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers=headers
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))

    return result['content'][0]['text']


def get_files_to_sync() -> list[Path]:
    """동기화할 파일 목록"""
    files = []

    # CLAUDE.md
    claude_md = CLAUDE_DIR / "CLAUDE.md"
    if claude_md.exists():
        files.append(claude_md)

    # docs/*.md
    docs_dir = CLAUDE_DIR / "docs"
    if docs_dir.exists():
        files.extend(docs_dir.glob("*.md"))

    # rules/**/*.md
    rules_dir = CLAUDE_DIR / "rules"
    if rules_dir.exists():
        files.extend(rules_dir.glob("**/*.md"))

    # 제외 필터
    filtered = []
    for f in files:
        skip = False
        for pattern in EXCLUDE_PATTERNS:
            if pattern.lower() in str(f).lower():
                skip = True
                break
        if not skip:
            filtered.append(f)

    return sorted(filtered)


def get_output_path(source: Path) -> Path:
    """출력 경로 계산"""
    relative = source.relative_to(CLAUDE_DIR)
    return USER_GUIDE_DIR / relative


def sync_file(source: Path, api_key: str, dry_run: bool = False) -> dict:
    """단일 파일 동기화"""
    output = get_output_path(source)

    result = {
        "source": str(source),
        "output": str(output),
        "status": "pending",
        "tokens": 0,
    }

    if dry_run:
        result["status"] = "dry-run"
        return result

    try:
        content = source.read_text(encoding='utf-8')
        translated = translate_to_korean(content, source.name, api_key)

        # 출력 디렉토리 생성
        output.parent.mkdir(parents=True, exist_ok=True)

        # 헤더 추가
        header = f"""<!--
  Auto-generated Korean translation
  Source: {source.relative_to(CLAUDE_DIR)}
  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
  DO NOT EDIT - Changes will be overwritten
-->

"""
        output.write_text(header + translated, encoding='utf-8')

        result["status"] = "success"
        result["tokens"] = len(content.split())

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def sync_all(dry_run: bool = False) -> list[dict]:
    """전체 동기화"""
    api_key = load_api_key()
    files = get_files_to_sync()
    results = []

    print(f"동기화 대상: {len(files)}개 파일")
    print(f"출력 경로: {USER_GUIDE_DIR}")
    print()

    for i, f in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {f.name}...", end=" ", flush=True)
        result = sync_file(f, api_key, dry_run)
        results.append(result)
        print(result["status"])

    return results


def main():
    parser = argparse.ArgumentParser(description="지침 파일 동기화")
    parser.add_argument("--file", "-f", help="개별 파일 동기화")
    parser.add_argument("--dry-run", "-n", action="store_true", help="미리보기")
    parser.add_argument("--list", "-l", action="store_true", help="파일 목록만 표시")
    args = parser.parse_args()

    if args.list:
        files = get_files_to_sync()
        print(f"동기화 대상 파일 ({len(files)}개):\n")
        for f in files:
            print(f"  {f.relative_to(CLAUDE_DIR)}")
        return

    if args.file:
        api_key = load_api_key()
        source = Path(args.file).expanduser().resolve()
        print(f"파일 동기화: {source.name}")
        result = sync_file(source, api_key, args.dry_run)
        print(f"결과: {result['status']}")
        if result.get('error'):
            print(f"에러: {result['error']}")
    else:
        results = sync_all(args.dry_run)

        success = sum(1 for r in results if r['status'] == 'success')
        errors = sum(1 for r in results if r['status'] == 'error')

        print()
        print(f"=== 완료 ===")
        print(f"성공: {success}, 실패: {errors}, 총: {len(results)}")


if __name__ == "__main__":
    main()
