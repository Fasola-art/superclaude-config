#!/usr/bin/env python3
"""
SuperClaude v2.0.9 Windows 설정 패치 스크립트
대상: Windows 노트북 (RTX 4090 Laptop 16GB VRAM, RAM 32GB)

실행: python setup-windows.py
롤백: python setup-windows.py --rollback
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
BACKUP_SUFFIX = ".mac-backup"


def is_windows() -> bool:
    return platform.system() == "Windows"


def get_username() -> str:
    return os.environ.get("USERNAME", os.environ.get("USER", "user"))


def get_home() -> str:
    return str(Path.home()).replace("\\", "/")


def backup_file(path: Path) -> None:
    """원본 파일 백업 (롤백용)"""
    backup = path.with_suffix(path.suffix + BACKUP_SUFFIX)
    if path.exists() and not backup.exists():
        shutil.copy2(path, backup)
        print(f"  [BACKUP] {path.name} → {backup.name}")


def restore_file(path: Path) -> None:
    """백업에서 복원"""
    backup = path.with_suffix(path.suffix + BACKUP_SUFFIX)
    if backup.exists():
        shutil.copy2(backup, path)
        backup.unlink()
        print(f"  [RESTORE] {backup.name} → {path.name}")


# ─────────────────────────────────────────────
# 1. settings.json 패치
# ─────────────────────────────────────────────
def patch_settings() -> None:
    """python3 → python, macOS 명령어 제거, Windows 명령어 추가"""
    path = CLAUDE_DIR / "settings.json"
    backup_file(path)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # python3 → python (hooks 전체)
    if "hooks" in data:
        for event_type, hook_list in data["hooks"].items():
            for entry in hook_list:
                for hook in entry.get("hooks", []):
                    cmd = hook.get("command", "")
                    hook["command"] = cmd.replace("python3 ", "python ")

    # permissions: macOS 전용 제거, Windows 추가
    if "permissions" in data and "allow" in data["permissions"]:
        allows = data["permissions"]["allow"]

        # macOS 전용 제거
        mac_only = [
            "Bash(open *)",
            "Bash(chmod*)",
            "Bash(ln *)",
            "Bash(source*)",
            "Bash(launchctl*)",
            "Bash(brew install*)",
            "Bash(brew update*)",
        ]
        allows = [a for a in allows if a not in mac_only]

        # Windows 추가
        win_additions = [
            "Bash(explorer *)",
            "Bash(start *)",
            "Bash(choco *)",
            "Bash(winget *)",
            "Bash(wsl *)",
        ]
        for item in win_additions:
            if item not in allows:
                allows.append(item)

        data["permissions"]["allow"] = allows

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("[OK] settings.json 패치 완료")


# ─────────────────────────────────────────────
# 2. mcp.json 패치
# ─────────────────────────────────────────────
def patch_mcp() -> None:
    """경로 치환, python3→python, macOS 전용 제거"""
    path = CLAUDE_DIR / "mcp.json"
    backup_file(path)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    home = get_home()

    # 경로 치환
    content = content.replace("/Users/reim", home)
    content = content.replace("~/.claude", f"{home}/.claude")

    # python3 → python
    content = content.replace('"python3"', '"python"')

    data = json.loads(content)

    # PostgreSQL 연결 문자열: 사용자명 치환
    servers = data.get("mcpServers", {})
    if "postgres" in servers:
        args = servers["postgres"].get("args", [])
        for i, arg in enumerate(args):
            if "postgresql://" in arg:
                user = get_username()
                args[i] = f"postgresql://{user}@localhost:5432/claude_mcp"

    # gdrive: Windows 경로로 변환
    if "gdrive" in servers:
        env = servers["gdrive"].get("env", {})
        cred_key = "GOOGLE_APPLICATION_CREDENTIALS"
        if cred_key in env:
            env[cred_key] = str(
                CLAUDE_DIR / "credentials" / "gcp-oauth.keys.json"
            )

    # kie-ai: python 경로 수정
    if "kie-ai" in servers:
        args = servers["kie-ai"].get("args", [])
        for i, arg in enumerate(args):
            if "/Users/reim" in arg:
                args[i] = str(CLAUDE_DIR / "mcp-servers" / "kie-ai" / "server.py")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("[OK] mcp.json 패치 완료")


# ─────────────────────────────────────────────
# 3. mcp-router/servers.json 패치
# ─────────────────────────────────────────────
def patch_mcp_router() -> None:
    """MLX → CUDA/Ollama, 경로 치환"""
    path = CLAUDE_DIR / "mcp-router" / "servers.json"
    backup_file(path)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    home = get_home()
    servers = data.get("mcpServers", {})

    # PostgreSQL: 사용자명 치환
    if "postgresql" in servers:
        env = servers["postgresql"].get("env", {})
        if "POSTGRES_CONNECTION_STRING" in env:
            user = get_username()
            env["POSTGRES_CONNECTION_STRING"] = (
                f"postgresql://{user}@localhost:5432/claude_mcp"
            )

    # local-llm: MLX → CUDA (4090 Laptop 16GB VRAM)
    if "local-llm" in servers:
        servers["local-llm"].update({
            "command": "python",
            "description": "로컬 LLM 서브에이전트 (CUDA/Ollama)",
        })
        env = servers["local-llm"].get("env", {})
        env["PYTHONPATH"] = f"{home}/.claude/modules/local-llm"

        # MLX 경로 제거, CUDA 설정 추가
        env.pop("MLX_MODEL_PATH", None)
        env["CUDA_VISIBLE_DEVICES"] = "0"
        env["LLM_BACKEND"] = "ollama"  # 4090 Laptop 16GB → Ollama 권장
        env["DEFAULT_MODEL"] = "qwen2.5:7b-instruct-q5_K_M"
        env["MAX_GPU_MEMORY_GB"] = "14"  # 16GB 중 14GB 할당 (OS용 2GB)
        servers["local-llm"]["env"] = env

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("[OK] mcp-router/servers.json 패치 완료")


# ─────────────────────────────────────────────
# 4. macOS 전용 hook 비활성화
# ─────────────────────────────────────────────
def patch_macos_hooks() -> None:
    """osascript 등 macOS 전용 코드가 있는 hook 패치"""
    notification_hook = (
        CLAUDE_DIR / "hooks" / "PostToolUse" / "background-notification.py"
    )
    if notification_hook.exists():
        backup_file(notification_hook)

        with open(notification_hook, "r", encoding="utf-8") as f:
            content = f.read()

        # osascript → Windows toast 알림으로 교체
        old_func = '''def send_notification(title: str, message: str):
    """Send macOS notification"""
    try:
        script = f\'\'\'
        display notification "{message}" with title "{title}" sound name "Glass"
        \'\'\'
        subprocess.run(["osascript", "-e", script], capture_output=True)
    except:
        pass'''

        new_func = '''def send_notification(title: str, message: str):
    """Send Windows toast notification"""
    try:
        import platform
        if platform.system() == "Windows":
            ps_cmd = (
                f'[Windows.UI.Notifications.ToastNotificationManager,'
                f' Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null;'
                f' $t = [Windows.UI.Notifications.ToastNotification]::new('
                f' ([Windows.Data.Xml.Dom.XmlDocument]::new()));'
            )
            subprocess.run(
                ["powershell", "-Command",
                 f'Add-Type -AssemblyName System.Windows.Forms;'
                 f'[System.Windows.Forms.MessageBox]::Show("{message}", "{title}")'],
                capture_output=True, timeout=5
            )
        else:
            script = f\\'\\'\\'\\'\n        display notification "{message}" with title "{title}" sound name "Glass"\n        \\'\\'\\'\\'\n            subprocess.run(["osascript", "-e", script], capture_output=True)
    except:
        pass'''

        # 간단하게: 플랫폼 감지 래퍼로 교체
        content = content.replace(
            'subprocess.run(["osascript", "-e", script], capture_output=True)',
            (
                'import platform\n'
                '        if platform.system() == "Darwin":\n'
                '            subprocess.run(["osascript", "-e", script], capture_output=True)\n'
                '        # Windows: 알림 생략 (또는 toast 구현)'
            ),
        )

        with open(notification_hook, "w", encoding="utf-8") as f:
            f.write(content)

    print("[OK] macOS 전용 hook 패치 완료")


# ─────────────────────────────────────────────
# 5. CLAUDE.md 환경 정보 업데이트
# ─────────────────────────────────────────────
def patch_claude_md() -> None:
    """플랫폼 정보 업데이트"""
    path = CLAUDE_DIR / "CLAUDE.md"
    backup_file(path)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(
        "Mac Studio Ultra M2",
        "Windows Laptop RTX 4090",
    )
    content = content.replace(
        "macOS (Mac Studio Ultra M2)",
        "Windows (RTX 4090 Laptop, 32GB RAM, 16GB VRAM)",
    )
    content = content.replace(
        "**Environment**: macOS (Mac Studio Ultra M2)",
        "**Environment**: Windows (RTX 4090 Laptop)",
    )

    # open -R → explorer
    content = content.replace("open -R <path>", "explorer <path>")
    content = content.replace("run `open -R", "run `explorer")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print("[OK] CLAUDE.md 플랫폼 정보 업데이트 완료")


# ─────────────────────────────────────────────
# 6. 런타임 디렉토리 생성
# ─────────────────────────────────────────────
def create_runtime_dirs() -> None:
    """런타임에 필요한 디렉토리 생성"""
    dirs = [
        "cache", "debug", "logs", "file-history", "session-env",
        "shell-snapshots", "paste-cache", "statsig", "telemetry",
        "sessions", "todos", "tasks", "backups", "downloads",
        "credentials",
    ]
    for d in dirs:
        (CLAUDE_DIR / d).mkdir(parents=True, exist_ok=True)

    print("[OK] 런타임 디렉토리 생성 완료")


# ─────────────────────────────────────────────
# 7. Windows용 .sh → 안내
# ─────────────────────────────────────────────
def check_shell_scripts() -> None:
    """실행 불가한 .sh 파일 목록 안내"""
    sh_files = list(CLAUDE_DIR.rglob("*.sh"))
    if sh_files:
        print(f"\n[INFO] .sh 파일 {len(sh_files)}개 발견:")
        print("  Git Bash 또는 WSL에서 실행 가능")
        for f in sh_files[:5]:
            print(f"    - {f.relative_to(CLAUDE_DIR)}")
        if len(sh_files) > 5:
            print(f"    ... 외 {len(sh_files) - 5}개")


# ─────────────────────────────────────────────
# 8. 의존성 설치 안내
# ─────────────────────────────────────────────
def print_post_setup() -> None:
    """셋업 후 필수 작업 안내"""
    print("\n" + "=" * 50)
    print("  Windows 셋업 완료!")
    print("=" * 50)

    print("\n[필수] 수동 설정:")
    print("  1. API 키: ~/.claude/credentials/api-keys.json")
    print("  2. PostgreSQL/MySQL 설치 후 연결 정보 확인")
    print("  3. Node.js + pnpm 설치")
    print("     winget install OpenJS.NodeJS.LTS")
    print("     npm install -g pnpm")

    print("\n[GPU] 로컬 LLM 설정 (RTX 4090 16GB VRAM):")
    print("  1. Ollama 설치:")
    print("     winget install Ollama.Ollama")
    print("  2. 추천 모델 (16GB VRAM 기준):")
    print("     ollama pull qwen2.5:7b-instruct-q5_K_M   # 5GB, 빠름")
    print("     ollama pull deepseek-r1:8b                # 5GB, 추론 특화")
    print("     ollama pull codellama:13b-instruct-q4_K_M # 8GB, 코딩")
    print("  [주의] 13B 이상 모델은 VRAM 16GB 한도 주의")
    print("  [주의] RAM 32GB → 동시에 큰 모델 2개 로드 금지")

    print("\n[권장] 추가 도구:")
    print("  winget install Git.Git")
    print("  winget install Python.Python.3.12")
    print("  pip install httpx aiohttp pydantic")

    print("\n[참고] Mac 원본 복원:")
    print("  python setup-windows.py --rollback")


# ─────────────────────────────────────────────
# 롤백
# ─────────────────────────────────────────────
def rollback() -> None:
    """모든 패치 파일을 Mac 원본으로 복원"""
    print("=== 롤백: Mac 원본 복원 ===\n")

    targets = [
        CLAUDE_DIR / "settings.json",
        CLAUDE_DIR / "mcp.json",
        CLAUDE_DIR / "mcp-router" / "servers.json",
        CLAUDE_DIR / "CLAUDE.md",
        CLAUDE_DIR / "hooks" / "PostToolUse" / "background-notification.py",
    ]

    restored = 0
    for path in targets:
        backup = path.with_suffix(path.suffix + BACKUP_SUFFIX)
        if backup.exists():
            restore_file(path)
            restored += 1

    print(f"\n[OK] {restored}개 파일 복원 완료")


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────
def main() -> None:
    if "--rollback" in sys.argv:
        rollback()
        return

    print("=== SuperClaude v2.0.9 Windows 패치 ===")
    print(f"대상: {CLAUDE_DIR}")
    print(f"플랫폼: {platform.system()} ({platform.machine()})")
    print(f"사용자: {get_username()}")
    print(f"홈: {get_home()}")
    print()

    if not CLAUDE_DIR.exists():
        print("[ERROR] ~/.claude 디렉토리가 없습니다.")
        print("먼저 git clone 실행:")
        print("  git clone https://github.com/Fasola-art/superclaude-config.git %USERPROFILE%\\.claude")
        sys.exit(1)

    patch_settings()
    patch_mcp()
    patch_mcp_router()
    patch_macos_hooks()
    patch_claude_md()
    create_runtime_dirs()
    check_shell_scripts()
    print_post_setup()


if __name__ == "__main__":
    main()
