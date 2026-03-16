#!/usr/bin/env python3
"""
롤백 유틸리티
  python rollback.py list [n]       스냅샷 목록 (기본 15개)
  python rollback.py undo [idx|hash]  복구 (기본: 마지막)
  python rollback.py status          현재 롤백 포인트 요약
  python rollback.py clean [days]    오래된 파일 백업 정리 (기본 7일)
"""
import json, sys, os, subprocess, shutil
from datetime import datetime, timedelta

LOG_PATH   = os.path.expanduser('~/.claude/rollback/log.jsonl')
BACKUP_DIR = os.path.expanduser('~/.claude/rollback/backups')


def load_log() -> list:
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


def cmd_list(n: int = 15):
    entries = load_log()
    if not entries:
        print('스냅샷 없음 — 파일 수정 또는 위험 명령 실행 시 자동 생성됩니다')
        return
    print(f"{'#':<5} {'시간':<20} {'타입':<12} {'상태'} 이유")
    print('─' * 72)
    for i, e in enumerate(reversed(entries[-n:])):
        idx  = len(entries) - 1 - i
        stype = e.get('type', '?')
        ok   = '✅' if e.get('committed', stype in ('file','dir')) else '⚪'
        ts   = e['ts'][:19].replace('T', ' ')
        print(f"{idx:<5} {ts:<20} {stype:<12} {ok}  {e['reason']}")


def restore(entry: dict) -> bool:
    stype = entry.get('type')

    if stype == 'git':
        root, h = entry['root'], entry['hash']
        r = subprocess.run(['git', 'reset', '--hard', h], cwd=root, capture_output=True, text=True)
        if r.returncode == 0:
            print(f'✅ git 롤백 완료 → {h[:8]} ({root})')
            return True
        print(f'❌ git 실패: {r.stderr.strip()}')
        return False

    if stype == 'file':
        src, dst = entry['backup'], entry['original']
        if not os.path.exists(src):
            print(f'❌ 백업 없음: {src}')
            return False
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f'✅ 파일 복구: {dst}')
        return True

    if stype == 'dir':
        src, dst = entry['backup'], entry['original']
        if not os.path.exists(src):
            print(f'❌ 백업 없음: {src}')
            return False
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f'✅ 디렉토리 복구: {dst}')
        return True

    if stype == 'dir-skipped':
        print(f'⚠️  크기 초과로 백업 없음: {entry.get("reason")}')
        return False

    print(f'❌ 알 수 없는 타입: {stype}')
    return False


def cmd_undo(target=None):
    entries = load_log()
    if not entries:
        print('롤백 포인트 없음')
        sys.exit(1)

    if target is None:
        idx, entry = len(entries) - 1, entries[-1]
    elif target.isdigit():
        idx = int(target)
        entry = entries[idx] if idx < len(entries) else None
    else:
        entry = next((e for e in reversed(entries) if e.get('hash','').startswith(target)), None)
        idx = entries.index(entry) if entry else -1

    if not entry:
        print(f'찾을 수 없음: {target}')
        sys.exit(1)

    ts = entry['ts'][:19].replace('T', ' ')
    print(f'롤백 대상 [{idx}]: {ts}  [{entry.get("type")}]  {entry["reason"]}')
    if input('진행? (y/N): ').strip().lower() != 'y':
        print('취소')
        return
    restore(entry)


def cmd_status():
    entries = load_log()
    git_n  = sum(1 for e in entries if e.get('type') == 'git')
    file_n = sum(1 for e in entries if e.get('type') == 'file')
    dir_n  = sum(1 for e in entries if e.get('type') == 'dir')
    print(f'총 스냅샷: {len(entries)}개  (git:{git_n}  파일:{file_n}  디렉토리:{dir_n})')
    if entries:
        last = entries[-1]
        print(f'마지막: {last["ts"][:19].replace("T"," ")}  {last["reason"]}')


def cmd_clean(days: int = 7):
    cutoff = datetime.now() - timedelta(days=days)
    removed = 0
    if os.path.exists(BACKUP_DIR):
        for d in os.listdir(BACKUP_DIR):
            try:
                ts = datetime.strptime(d[:15], '%Y%m%d_%H%M%S')
                if ts < cutoff:
                    shutil.rmtree(os.path.join(BACKUP_DIR, d))
                    removed += 1
            except ValueError:
                pass
    print(f'✅ {days}일 이전 백업 {removed}개 삭제')


args = sys.argv[1:]
cmd  = args[0] if args else 'list'

if   cmd == 'list':   cmd_list(int(args[1]) if len(args) > 1 else 15)
elif cmd == 'undo':   cmd_undo(args[1] if len(args) > 1 else None)
elif cmd == 'status': cmd_status()
elif cmd == 'clean':  cmd_clean(int(args[1]) if len(args) > 1 else 7)
else: print(__doc__)
