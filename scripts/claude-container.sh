#!/bin/bash
# 위험한 작업을 Docker 컨테이너에서 격리 실행
# 사용법: claude-container.sh [language] [command]
# 예시: claude-container.sh node "npm test"
#       claude-container.sh python "pytest"

set -euo pipefail

LANG="${1:-node}"
CMD="${2:-echo 'No command specified'}"
WORKDIR="${3:-$(pwd)}"

declare -A IMAGES=(
    [node]="node:20-slim"
    [python]="python:3.12-slim"
    [go]="golang:1.22-bookworm"
    [rust]="rust:1.77-slim"
)

IMAGE="${IMAGES[$LANG]:-$LANG}"

echo "🐳 Running in container: $IMAGE"
echo "📁 Mounting: $WORKDIR"
echo "🔧 Command: $CMD"

docker run --rm -it \
    -v "$WORKDIR:/workspace" \
    -w /workspace \
    --network none \
    --memory 4g \
    --cpus 4 \
    "$IMAGE" \
    sh -c "$CMD"
