#!/bin/bash
# MCP Router 데몬 관리 스크립트

ROUTER_DIR="$HOME/.claude/mcp-router"
LOG_DIR="$HOME/.claude/logs/mcp-router"
PID_FILE="$ROUTER_DIR/router.pid"
LOG_FILE="$LOG_DIR/daemon.log"

# 로그 디렉토리 생성
mkdir -p "$LOG_DIR"

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "MCP Router가 이미 실행 중입니다 (PID: $PID)"
            return 1
        fi
    fi

    echo "MCP Router 시작 중..."
    cd "$ROUTER_DIR"
    nohup python3 server.py >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 2

    if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        echo "✅ MCP Router 시작됨 (PID: $(cat $PID_FILE))"
        echo "로그: $LOG_FILE"
    else
        echo "❌ MCP Router 시작 실패"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "MCP Router가 실행 중이 아닙니다"
        return 0
    fi

    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "MCP Router 중지 중 (PID: $PID)..."
        kill "$PID"
        sleep 2

        if ps -p "$PID" > /dev/null 2>&1; then
            echo "강제 종료 중..."
            kill -9 "$PID"
        fi
    fi

    rm -f "$PID_FILE"
    rm -f "$ROUTER_DIR/router.sock"
    echo "✅ MCP Router 중지됨"
}

restart() {
    stop
    sleep 1
    start
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "✅ MCP Router 실행 중 (PID: $PID)"

            # 소켓 파일 확인
            if [ -S "$ROUTER_DIR/router.sock" ]; then
                echo "✅ Unix 소켓 활성"
            else
                echo "⚠️ Unix 소켓 없음"
            fi

            # 클라이언트로 상태 확인
            echo ""
            echo "서버 상태:"
            python3 "$ROUTER_DIR/client.py" status 2>/dev/null || echo "  (상태 조회 실패)"
            return 0
        fi
    fi

    echo "❌ MCP Router 실행 중 아님"
    return 1
}

logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "로그 파일 없음: $LOG_FILE"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    *)
        echo "사용법: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
