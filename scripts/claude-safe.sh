#!/bin/bash
# claude-safe: Git 스냅샷 기반 안전한 --dangerously-skip-permissions 래퍼
# 사용: claude-safe "프롬프트" [옵션...]
# 롤백: claude-safe --rollback

set -euo pipefail

SNAPSHOT_LOG="$HOME/.claude/rollback/sessions.jsonl"
ROLLBACK_DIR="$HOME/.claude/rollback"
mkdir -p "$ROLLBACK_DIR"

# 색상 정의
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; NC='\033[0m'
AUTO_YES=false

# -y 플래그 파싱
for arg in "$@"; do
    [ "$arg" = "-y" ] || [ "$arg" = "--yes" ] && AUTO_YES=true
done

confirm_action() {
    if $AUTO_YES; then return 0; fi
    [ -r /dev/tty ] || return 1
    local confirm=""
    read -p "$1 (y/N) " confirm < /dev/tty || return 1
    [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]
}

show_help() {
    echo "Usage: claude-safe [OPTIONS] \"prompt\""
    echo ""
    echo "Options:"
    echo "  --rollback         최근 세션으로 롤백"
    echo "  --rollback-list    롤백 가능한 세션 목록"
    echo "  --rollback-to ID   특정 세션으로 롤백"
    echo "  --interactive      대화형 모드 (-p 없이)"
    echo "  -y, --yes          확인 프롬프트 건너뛰기"
    echo "  -h, --help         도움말"
}

get_git_root() {
    git rev-parse --show-toplevel 2>/dev/null
}

create_snapshot() {
    local git_root session_id tag_name commit_hash
    git_root=$(get_git_root)
    if [ -z "$git_root" ]; then
        echo -e "${YELLOW}[WARN] Git 저장소가 아닙니다. 파일 백업 모드로 전환${NC}"
        return 1
    fi

    session_id="claude-safe-$(date +%Y%m%d-%H%M%S)"
    tag_name="rollback/${session_id}"

    # 변경사항이 있으면 임시 커밋
    cd "$git_root"
    if ! git diff --quiet HEAD 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
        git stash push -m "$session_id" --include-untracked 2>/dev/null
        git stash pop 2>/dev/null
    fi

    # 현재 상태에 태그
    commit_hash=$(git rev-parse HEAD)
    git tag "$tag_name" "$commit_hash" 2>/dev/null || true

    # 세션 기록 저장
    local entry
    entry=$(printf '{"id":"%s","tag":"%s","commit":"%s","cwd":"%s","time":"%s","prompt":"%s"}' \
        "$session_id" "$tag_name" "$commit_hash" "$PWD" "$(date -u +%FT%TZ)" "${1:-unknown}")
    echo "$entry" >> "$SNAPSHOT_LOG"

    echo -e "${GREEN}[SNAPSHOT] ${tag_name} (${commit_hash:0:8})${NC}"
    echo "$session_id"
}

do_rollback() {
    local target_tag git_root
    if [ ! -f "$SNAPSHOT_LOG" ]; then
        echo -e "${RED}[ERROR] 롤백 기록이 없습니다${NC}"; exit 1
    fi

    if [ -n "${1:-}" ]; then
        target_tag=$(grep "\"id\":\"$1\"" "$SNAPSHOT_LOG" | tail -1 | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['tag'])")
    else
        target_tag=$(tail -1 "$SNAPSHOT_LOG" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['tag'])")
    fi

    if [ -z "$target_tag" ]; then
        echo -e "${RED}[ERROR] 롤백 대상을 찾을 수 없습니다${NC}"; exit 1
    fi

    git_root=$(get_git_root)
    if [ -z "$git_root" ]; then
        echo -e "${RED}[ERROR] Git 저장소가 아닙니다${NC}"; exit 1
    fi

    cd "$git_root"
    echo -e "${YELLOW}[ROLLBACK] → ${target_tag}${NC}"
    echo -e "${YELLOW}변경될 파일:${NC}"
    git diff --stat "${target_tag}..HEAD" 2>/dev/null || true

    if confirm_action "롤백을 진행하시겠습니까?"; then
        # 스냅샷 시점 파일 목록 비교
        local tag_files current_files added_files
        tag_files=$(git ls-tree -r --name-only "$target_tag" 2>/dev/null | sort)
        current_files=$(git ls-tree -r --name-only HEAD 2>/dev/null | sort)

        git checkout "$target_tag" -- . 2>/dev/null

        # 스냅샷 이후 추가된 파일 삭제
        added_files=$(comm -13 <(echo "$tag_files") <(echo "$current_files"))
        if [ -n "$added_files" ]; then
            echo -e "${YELLOW}[CLEAN] 추가된 파일 삭제:${NC}"
            echo "$added_files" | while read -r f; do
                [ -f "$git_root/$f" ] && rm "$git_root/$f" && echo "  - $f"
            done
        fi
        echo -e "${GREEN}[DONE] 롤백 완료${NC}"
    else
        echo -e "${BLUE}[CANCEL] 롤백 취소${NC}"
    fi
}

list_rollbacks() {
    if [ ! -f "$SNAPSHOT_LOG" ]; then
        echo "롤백 기록이 없습니다"; exit 0
    fi
    echo -e "${BLUE}=== 롤백 가능한 세션 ===${NC}"
    tail -20 "$SNAPSHOT_LOG" | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line.strip())
    print(f\"  {d['time'][:19]}  {d['id']}  {d['commit'][:8]}  {d.get('prompt','')[:40]}\")
"
}

# 메인 로직
case "${1:-}" in
    --rollback)
        # ${2:-}가 -y/--yes이면 세션 ID가 아닌 플래그이므로 무시
        _rb_target="${2:-}"
        [[ "$_rb_target" == "-y" || "$_rb_target" == "--yes" ]] && _rb_target=""
        do_rollback "$_rb_target"; exit 0 ;;
    --rollback-list) list_rollbacks; exit 0 ;;
    --rollback-to)  do_rollback "$2"; exit 0 ;;
    -h|--help)      show_help; exit 0 ;;
esac

PROMPT="${1:?프롬프트를 입력하세요}"
shift
MODE="-p"
CLAUDE_ARGS=()
for arg in "$@"; do
    case "$arg" in
        -y|--yes) continue ;;           # claude에 전달하지 않음
        --interactive) MODE="" ;;
        *) CLAUDE_ARGS+=("$arg") ;;
    esac
done

# 1. 스냅샷 생성
SESSION_ID=$(create_snapshot "$PROMPT" 2>/dev/null || echo "no-git")

# 2. Claude 실행
echo -e "${BLUE}[RUN] claude --dangerously-skip-permissions ${MODE} ...${NC}"
set +e
claude --dangerously-skip-permissions $MODE "$PROMPT" ${CLAUDE_ARGS[@]+"${CLAUDE_ARGS[@]}"}
EXIT_CODE=$?
set -e

# 3. 결과 요약
if [ "$EXIT_CODE" -eq 0 ]; then
    echo -e "${GREEN}[DONE] 세션 완료${NC}"
else
    echo -e "${RED}[FAIL] 종료코드: ${EXIT_CODE}${NC}"
fi

git_root=$(get_git_root 2>/dev/null)
if [ -n "$git_root" ]; then
    cd "$git_root"
    changed=$(git diff --stat HEAD 2>/dev/null | tail -1)
    if [ -n "$changed" ]; then
        echo -e "${YELLOW}[CHANGES] ${changed}${NC}"
        echo -e "${YELLOW}롤백: claude-safe --rollback${NC}"
    fi
fi

exit $EXIT_CODE
