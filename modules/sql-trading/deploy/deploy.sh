#!/bin/bash
set -e

# ===================================================
# SQL Trading 대시보드 배포 스크립트
# Oracle Cloud / Hetzner / 모든 Linux VPS 호환
# ===================================================

echo "=== SQL Trading 배포 ==="

# 1. Docker 설치 확인
if ! command -v docker &> /dev/null; then
    echo "Docker 설치 중..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo "Docker 설치 완료. 재로그인 후 다시 실행하세요."
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "Docker Compose 플러그인이 없습니다."
    echo "sudo apt install docker-compose-plugin"
    exit 1
fi

# 2. .env 파일 확인
cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo ".env 파일 생성 중 (.env.example 복사)..."
    cp .env.example .env
    echo ""
    echo "⚠️  .env 파일을 편집하세요:"
    echo "   nano $(pwd)/.env"
    echo ""
    echo "필수 변경:"
    echo "  - POSTGRES_PASSWORD: 강력한 비밀번호"
    echo "  - DB_PASSWORD: 위와 동일"
    echo "  - DOMAIN: 도메인 또는 서버 IP"
    echo "  - API 키: ALPHA_VANTAGE_KEY, FRED_API_KEY"
    echo ""
    echo ".env 편집 후 다시 실행하세요."
    exit 0
fi

# 3. 빌드 + 실행
echo "Docker 이미지 빌드 중..."
docker compose build

echo "서비스 시작 중..."
docker compose up -d

echo ""
echo "=== 배포 완료 ==="
echo ""
docker compose ps
echo ""
echo "접속:"
echo "  대시보드: http://$(grep DOMAIN .env | cut -d= -f2)"
echo "  API 문서: http://$(grep DOMAIN .env | cut -d= -f2)/api/docs"
echo ""
echo "로그 확인: docker compose logs -f"
echo "중지:      docker compose down"
echo "업데이트:  git pull && docker compose up -d --build"
