# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

**My-Brain AI Assistant** - Apple Silicon 환경에서 로컬로 동작하는 개인화된 AI 비서. 개인 데이터(회사, 개인, 프로젝트 폴더)를 수집하여 시맨틱 검색과 채팅을 지원합니다.

## 개발 명령어

### 백엔드 (FastAPI)
```bash
# 가상환경 활성화
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행 (루트에서)
uvicorn apps.server.main:app --host 0.0.0.0 --port 8000 --reload

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
├── server/          # FastAPI 백엔드
│   ├── main.py      # 앱 진입점, lifespan에서 파일 감시 시작/종료
│   ├── api/         # API 라우터 (chat, rag, work)
│   ├── core/        # 설정 (config.py)
│   └── services/    # 비즈니스 로직
│       ├── llm.py      # Ollama 연동
│       ├── rag.py      # 벡터 검색 엔진
│       └── ingest.py   # 파일 감시 및 처리 (Watchdog)
└── web/             # Next.js 프론트엔드
    └── src/
        ├── app/     # 페이지 (/, /chat, /history, /settings)
        ├── api/     # 백엔드 통신 클라이언트
        └── components/
```

### 데이터 흐름
1. **수집**: `data/` 폴더 파일 → Watchdog 감지 → 텍스트 추출 → RAG 엔진 저장
2. **질의응답**: 사용자 질문 → RAG 검색 → Ollama LLM → 답변 생성

### 주요 설정 (apps/server/core/config.py)
- `OLLAMA_BASE_URL`: http://localhost:11434
- `CHROMA_DB_PATH`: ./data/.vector_db
- API prefix: `/api/v1`

## 기술 스택

- **백엔드**: Python 3.14, FastAPI, LangChain, ChromaDB, Watchdog
- **프론트엔드**: Next.js 16, React 19, TypeScript
- **AI**: Ollama (로컬 LLM)
