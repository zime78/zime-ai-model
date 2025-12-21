# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

**My-Brain AI Assistant** - Apple Silicon 환경에서 로컬로 동작하는 개인화된 AI 비서. 개인 데이터(회사, 개인, 프로젝트 폴더)를 수집하여 시맨틱 검색과 채팅을 지원합니다.

## 개발 명령어

### 빠른 시작 (Docker)
```bash
# 환경변수 설정
cp .env.example .env

# Docker로 서버 시작
./scripts/start-server.sh docker

# 개발 모드 (핫 리로드)
./scripts/start-server.sh docker-dev
```

### 백엔드 (FastAPI)
```bash
# 가상환경 활성화
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
./scripts/start-server.sh dev

# 프로덕션 서버 실행 (Gunicorn)
./scripts/start-server.sh prod

# Ollama 사전 실행 필요
ollama serve
```

### 프론트엔드 (Next.js)
```bash
cd apps/web

# 의존성 설치
npm install

# 개발 서버 (LAN 접근 가능)
npm run dev

# 빌드
npm run build

# 린트
npm run lint
```

## 아키텍처

### Monorepo 구조
```
apps/
├── server/              # FastAPI 백엔드
│   ├── main.py          # 앱 진입점, lifespan에서 파일 감시 시작/종료
│   ├── api/             # API 라우터 (chat, rag, work, health)
│   ├── core/            # 설정 및 핵심 로직
│   │   ├── config.py    # 환경변수 설정 (pydantic-settings)
│   │   ├── logging.py   # 구조화 로깅 (JSON/텍스트)
│   │   └── middleware.py # 요청 타이밍 미들웨어
│   └── services/        # 비즈니스 로직
│       ├── llm.py       # Ollama 연동
│       ├── rag.py       # 벡터 검색 엔진
│       └── ingest.py    # 파일 감시 및 처리 (Watchdog)
└── web/                 # Next.js 프론트엔드
    └── src/
        ├── app/         # 페이지 (/, /chat, /history, /settings)
        ├── api/         # 백엔드 통신 클라이언트
        └── components/
```

### 배포 구조
```
/
├── Dockerfile.server     # FastAPI 이미지
├── Dockerfile.web        # Next.js 이미지 (standalone)
├── docker-compose.yml    # 프로덕션 오케스트레이션
├── docker-compose.dev.yml # 개발 오버라이드
├── gunicorn.conf.py      # Gunicorn 워커 설정
├── .env.example          # 환경변수 템플릿
└── scripts/
    └── start-server.sh   # 통합 실행 스크립트
```

### 데이터 흐름
1. **수집**: `data/` 폴더 파일 → Watchdog 감지 → 텍스트 추출 → RAG 엔진 저장
2. **질의응답**: 사용자 질문 → RAG 검색 → Ollama LLM → 답변 생성

### 주요 설정 (.env 또는 환경변수)
- `ENVIRONMENT`: development | production
- `OLLAMA_BASE_URL`: http://localhost:11434 (Docker: host.docker.internal)
- `CHROMA_DB_PATH`: ./data/.vector_db
- `BACKEND_CORS_ORIGINS`: 허용 도메인 (쉼표 구분)
- `LOG_LEVEL`: DEBUG | INFO | WARNING | ERROR
- `LOG_FORMAT`: json | text

### API 엔드포인트
- `/api/v1/chat` - 채팅 API
- `/api/v1/rag` - RAG 검색 API
- `/api/v1/work` - 작업 관리 API
- `/health` - 상세 헬스체크
- `/health/live` - Liveness 프로브
- `/health/ready` - Readiness 프로브
- `/docs` - Swagger UI (개발 모드만)

## 기술 스택

- **백엔드**: Python 3.11+, FastAPI, Gunicorn, LangChain, ChromaDB, Watchdog
- **프론트엔드**: Next.js 16, React 19, TypeScript
- **AI**: Ollama (로컬 LLM)
- **배포**: Docker, Docker Compose
