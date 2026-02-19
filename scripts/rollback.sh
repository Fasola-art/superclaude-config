#!/bin/bash
# rollback.sh: 독립 실행 가능한 롤백 유틸리티
# 사용: rollback.sh [list|last|to <id>|diff <id>|clean] [-y]

set -euo pipefail

SNAPSHOT_LOG="$HOME/.claude/rollback/sessions.jsonl"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; NC='\033[0m'
AUTO_YES=false

# -y 플래그 파싱
for arg in "$@"; do
    [ "$arg" = "-y" ] || [ "$arg" = "--yes" ] && AUTO_YES=true
done

require_log() {
    [ -f "$SNAPSHOT_LOG" ] || { echo -e "${RED}롤백 기록 없음${NC}"; exit 1; }
}

require_git() {
    git rev-parse --show-toplevel >/dev/null 2>&1 || { echo -e "${RED}Git 저장소가 아닙니다${NC}"; exit 1; }
}

confirm_action() {
    if $AUTO_YES; then return 0; fi
    read -p "진행하시겠습니까? (y/N) " confirm </dev/tty
    [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]
}

get_tag() {
    local id="$1"
    grep "\"id\":\"$id\"" "$SNAPSHOT_LOG" | tail -1 | \
        python3 -c "import sys,json; print(json.loads(sys.stdin.read())['tag'])"
}

get_latest_tag() {
    tail -1 "$SNAPSHOT_LOG" | \
        python3 -c "import sys,json; print(json.loads(sys.stdin.read())['tag'])"
}

cmd_list() {
    require_log
    echo -e "${BLUE}=== Claude Safe 롤백 포인트 ===${NC}"
    echo "  시간                 ID                              커밋      프롬프트"
    echo "  ──────────────────── ──────────────────────────────── ──────── ────────────────"
    tail -20 "$SNAPSHOT_LOG" | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line.strip())
    t = d['time'][:19].replace('T',' ')
    print(f\"  {t}  {d['id']:<32} {d['commit'][:8]}  {d.get('prompt','')[:30]}\")"
}

cmd_diff() {
    require_log; require_git
    local tag
    if [ -n "${1:-}" ] && [ "$1" != "-y" ]; then
        tag=$(get_tag "$1")
    else
        tag=$(get_latest_tag)
    fi
    [ -z "$tag" ] && { echo -e "${RED}태그를 찾을 수 없습니다${NC}"; exit 1; }
    echo -e "${BLUE}[DIFF] ${tag} → HEAD${NC}"
    git diff "${tag}..HEAD" --stat
    echo ""
    git diff "${tag}..HEAD"
}

cmd_rollback() {
    require_log; require_git
    local id="${1:-}" tag git_root
    if [ -z "$id" ] || [ "$id" = "-y" ]; then
        tag=$(get_latest_tag)
        id="(최근)"
    else
        tag=$(get_tag "$id")
    fi
    [ -z "$tag" ] && { echo -e "${RED}태그를 찾을 수 없습니다${NC}"; exit 1; }

    git_root=$(git rev-parse --show-toplevel)
    echo -e "${YELLOW}[ROLLBACK] ${id} → ${tag}${NC}"
    git diff "${tag}..HEAD" --stat 2>/dev/null
    echo ""

    if confirm_action; then
        # 스냅샷 시점의 파일 목록
        local tag_files current_files
        tag_files=$(git ls-tree -r --name-only "$tag" 2>/dev/null | sort)
        current_files=$(git ls-tree -r --name-only HEAD 2>/dev/null | sort)

        # 스냅샷 시점으로 파일 복원
        git checkout "$tag" -- . 2>/dev/null

        # 스냅샷 이후 추가된 파일 삭제
        local added_files
        added_files=$(comm -13 <(echo "$tag_files") <(echo "$current_files"))
        if [ -n "$added_files" ]; then
            echo -e "${YELLOW}[CLEAN] 추가된 파일 삭제:${NC}"
            echo "$added_files" | while read -r f; do
                if [ -f "$git_root/$f" ]; then
                    rm "$git_root/$f"
                    echo "  - $f"
                fi
            done
        fi

        echo -e "${GREEN}[DONE] 롤백 완료${NC}"
    else
        echo -e "${BLUE}[CANCEL] 취소${NC}"
    fi
}

cmd_clean() {
    require_git
    local count
    count=$(git tag -l 'rollback/*' | wc -l | tr -d ' ')
    echo -e "${YELLOW}롤백 태그 ${count}개 삭제${NC}"
    if confirm_action; then
        git tag -l 'rollback/*' | xargs git tag -d 2>/dev/null || true
        : > "$SNAPSHOT_LOG"
        echo -e "${GREEN}[DONE] 정리 완료${NC}"
    fi
}

# 첫 인자에서 -y 제외
CMD="${1:-help}"
[ "$CMD" = "-y" ] && CMD="help"

case "$CMD" in
    list)   cmd_list ;;
    last)   cmd_rollback "${2:-}" ;;
    to)     cmd_rollback "${2:?ID를 입력하세요}" ;;
    diff)   cmd_diff "${2:-}" ;;
    clean)  cmd_clean ;;
    help|*) echo "Usage: rollback.sh [list|last|to <id>|diff [id]|clean] [-y]" ;;
esac
