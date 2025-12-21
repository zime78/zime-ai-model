#!/bin/bash
# My-Brain AI 서버 시작 스크립트

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# 환경변수 로드
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# PYTHONPATH 설정
export PYTHONPATH=$PYTHONPATH:$PROJECT_DIR

# 실행 모드 확인
MODE=${1:-"dev"}

case $MODE in
    "dev")
        echo "개발 모드로 서버 시작..."
        source .venv/bin/activate
        uvicorn apps.server.main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    "prod")
        echo "프로덕션 모드로 서버 시작 (Gunicorn)..."
        source .venv/bin/activate
        gunicorn apps.server.main:app -c gunicorn.conf.py
        ;;
    "docker")
        echo "Docker로 서버 시작..."
        docker-compose up -d
        echo "서버가 백그라운드에서 실행 중입니다."
        echo "로그 확인: docker-compose logs -f"
        ;;
    "docker-dev")
        echo "Docker 개발 모드로 서버 시작..."
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
        ;;
    *)
        echo "사용법: $0 [dev|prod|docker|docker-dev]"
        echo "  dev       - uvicorn 개발 서버 (핫 리로드)"
        echo "  prod      - gunicorn 프로덕션 서버"
        echo "  docker    - Docker 컨테이너 (백그라운드)"
        echo "  docker-dev - Docker 개발 모드"
        exit 1
        ;;
esac
