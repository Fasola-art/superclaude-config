#!/bin/bash
PLIST="$HOME/Library/LaunchAgents/com.superclaude.mcp-router.plist"
LABEL="com.superclaude.mcp-router"

case "$1" in
    load)
        echo "MCP Router 서비스 등록 중..."
        bash ~/.claude/mcp-router/daemon.sh stop 2>/dev/null
        launchctl load -w "$PLIST" 2>/dev/null
        if launchctl list | grep -q "$LABEL"; then
            echo "서비스 등록됨 (부팅 시 자동 시작)"
        else
            echo "서비스 등록 실패"
        fi
        ;;
    unload)
        launchctl unload -w "$PLIST" 2>/dev/null
        echo "서비스 해제됨"
        ;;
    start)
        launchctl start "$LABEL"
        sleep 2
        bash ~/.claude/mcp-router/launchctl.sh status
        ;;
    stop)
        launchctl stop "$LABEL"
        echo "서비스 중지됨"
        ;;
    status)
        if launchctl list | grep -q "$LABEL"; then
            echo "서비스 등록됨"
            PID=$(launchctl list | grep "$LABEL" | awk '{print $1}')
            if [ "$PID" != "-" ] && [ -n "$PID" ]; then
                echo "실행 중 (PID: $PID)"
            fi
        else
            echo "서비스 등록되지 않음"
        fi
        ;;
    logs)
        tail -30 ~/.claude/logs/mcp-router/launchd.log 2>/dev/null
        ;;
    *)
        echo "사용법: $0 {load|unload|start|stop|status|logs}"
        ;;
esac
