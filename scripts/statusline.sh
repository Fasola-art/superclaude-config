#!/bin/bash
# Claude Code status line 스크립트
# 표시: [모델] | [Git branch] | [시간]
BRANCH=$(git branch --show-current 2>/dev/null || echo "no-git")
echo "opus-4.6 | $BRANCH | $(date +%H:%M)"
