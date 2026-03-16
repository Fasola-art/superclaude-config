"""
PreToolUse Hook: 위험 작업 전 자동 스냅샷
- git repo  → git commit 스냅샷
- 일반 폴더 → 파일/디렉토리 복사 백업 (~/.claude/rollback/backups/)
"""
import json, sys, os, subprocess, re, shutil
from datetime import datetime, timedelta

DANGEROUS = [
    r'\brm\s+-[rf]', r'\bgit\s+reset\s+--hard',
    r'\bgit\s+clean\s+-[fd]', r'\bDROP\s+(TABLE|DATABASE)\b',
    r'\bTRUNCATE\b', r'\bdd\s+if=', r'\bmkfs\b',
    r'\bdiskpart\b', r'\bformat\s+[A-Z]:\b',
]
LOG_PATH   = os.path.expanduser('~/.claude/rollback/log.jsonl')
BACKUP_DIR = os.path.expanduser('~/.claude/rollback/backups')
THROTTLE_MIN  = 5
MAX_BACKUP_MB = 100
IGNORE_DIRS   = {'.git', 'node_modules', '__pycache__', '.venv', 'dist', 'build'}


def is_dangerous(cmd: str) -> bool:
    return any(re.search(p, cmd, re.IGNORECASE) for p in DANGEROUS)


def recently_snapshotted() -> bool:
    if not os.path.exists(LOG_PATH):
        return False
    with open(LOG_PATH, encoding='utf-8') as f:
        lines = [l for l in f if l.strip()]
    if not lines:
        return False
    last = json.loads(lines[-1])
    return datetime.now() - datetime.fromisoformat(last['ts']) < timedelta(minutes=THROTTLE_MIN)


def git_root(cwd: str):
    r = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                       cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def git_snapshot(reason: str, root: str) -> dict:
    subprocess.run(['git', 'add', '-A'], cwd=root, capture_output=True)
    r = subprocess.run(['git', 'commit', '-m', f'[rollback-point] {reason[:60]}'],
                       cwd=root, capture_output=True, text=True)
    h = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True)
    return {'type': 'git', 'hash': h.stdout.strip(), 'root': root, 'committed': r.returncode == 0}


def ts_key() -> str:
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def safe_name(path: str) -> str:
    return os.path.abspath(path).replace(':', '_drive').replace('\\', '__').replace('/', '__')


def file_snapshot(file_path: str) -> dict | None:
    if not file_path or not os.path.exists(file_path):
        return None
    dst = os.path.join(BACKUP_DIR, ts_key(), safe_name(file_path))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(file_path, dst)
    return {'type': 'file', 'original': os.path.abspath(file_path), 'backup': dst}


def dir_snapshot(cwd: str) -> dict:
    total_mb = sum(
        os.path.getsize(os.path.join(dp, f))
        for dp, dns, files in os.walk(cwd)
        for f in files
        if not any(ig in dp for ig in IGNORE_DIRS)
    ) / 1024 / 1024

    if total_mb > MAX_BACKUP_MB:
        return {'type': 'dir-skipped', 'reason': f'{total_mb:.0f}MB > 한도 {MAX_BACKUP_MB}MB', 'cwd': cwd}

    dst = os.path.join(BACKUP_DIR, ts_key(), 'dir')
    shutil.copytree(cwd, dst, ignore=shutil.ignore_patterns(*IGNORE_DIRS))
    return {'type': 'dir', 'original': cwd, 'backup': dst}


def log_entry(entry: dict):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


# ── Main ──────────────────────────────────────────────────────────────────
data = json.load(sys.stdin)
tool = data.get('tool_name', '')
inp  = data.get('tool_input', {})
cwd  = os.getcwd()

should_snap   = False
reason        = ''
file_path     = None
dangerous_bash = False

if tool == 'Bash':
    cmd = inp.get('command', '')
    if is_dangerous(cmd):
        should_snap = dangerous_bash = True
        reason = f'dangerous: {cmd[:60]}'

elif tool in ('Write', 'Edit', 'MultiEdit', 'NotebookEdit'):
    file_path = inp.get('file_path', inp.get('filePath', ''))
    if not recently_snapshotted():
        should_snap = True
        reason = f'file-write: {os.path.basename(str(file_path))}'

if should_snap:
    root = git_root(cwd)
    if root:
        snap = git_snapshot(reason, root)
    elif dangerous_bash:
        snap = dir_snapshot(cwd)
    else:
        snap = file_snapshot(str(file_path)) if file_path else None

    if snap:
        entry = {'ts': datetime.now().isoformat(), 'reason': reason, 'cwd': cwd, **snap}
        log_entry(entry)

sys.exit(0)
