# 시스템 아키텍처 문서 (Architecture Document)

## 1. 개요 (Overview)
본 문서는 "나만의 AI 비서 (My-Brain)" 프로젝트의 전체 시스템 구조와 모듈 간의 상호작용을 정의합니다.
시스템은 **Monorepo** 구조를 따르며, **FastAPI 백엔드**와 **Next.js 프론트엔드**로 구성됩니다. 로컬 AI 모델(Ollama)과 벡터 데이터베이스(ChromaDB)를 활용하여 개인 데이터를 처리합니다.

## 2. 디렉토리 구조 (Directory Structure)
```
/Users/zime/Git/zime-ai-model/
├── apps/
│   ├── web/                # [Frontend] Next.js Application
│   │   ├── src/pages/      # UI 화면 (Dashboard, Chat)
│   │   └── src/api/        # Backend 통신 클라이언트
│   └── server/             # [Backend] FastAPI Application
│       ├── main.py         # App Entry Point
│       ├── api/            # API 라우터 (Endpoints)
│       ├── core/           # 설정 및 공통 유틸리티
│       ├── services/       # 비즈니스 로직
│       │   ├── llm.py      # Ollama 연동
│       │   ├── rag.py      # RAG (Vector DB) 엔진
│       │   └── ingest.py   # 파일 수집 및 처리
│       └── models/         # Pydantic 모델 및 DB 스키마
├── data/                   # [Data] 사용자 데이터 저장소
│   ├── company/
│   ├── personal/
│   ├── project/
│   └── .vector_db/         # ChromaDB 데이터 저장 경로
└── scripts/                # [Scripts] 유틸리티 및 실행 스크립트
```

## 3. 시스템 구성 요소 (Components)

### 3.1. 백엔드 (Backend - Python/FastAPI)
- **API Server:** 프론트엔드 요청 처리 및 데이터 제공.
- **Ingestion Engine (수집기):**
    - `Watchdog`을 사용하여 `data/` 폴더 하위의 파일 변경 사항 감지.
    - 파일 타입별(Text, Markdown, Image) 처리기 분리.
    - 이미지의 경우 Vision 모델(Ollama) 또는 OCR을 통해 텍스트 추출.
- **RAG Engine (검색기):**
    - 추출된 텍스트를 임베딩(Embedding)하여 ChromaDB에 저장.
    - 사용자 질문에 대한 의미론적 검색(Semantic Search) 수행.
- **LLM Service:**
    - Ollama API와 통신하여 검색된 문맥(Context)을 바탕으로 답변 생성.

### 3.2. 프론트엔드 (Frontend - Next.js)
- **Dashboard:** 인덱싱 상태, 최근 작업 문서, 시스템 리소스 현황 시각화.
- **Chat Interface:**
    - 실시간 스트리밍 답변 표시.
    - 이전 대화 내역 조회.

### 3.3. 데이터 흐름 (Data Flow)
1.  **데이터 수집:** 사용자 파일 저장 -> `Ingestion Engine` 감지 -> 텍스트 추출 -> 임베딩 -> `ChromaDB` 저장.
2.  **질의 응답:** 사용자 질문(Web) -> API 호출 -> `RAG Engine` 검색 -> 관련 문서 확보 -> `LLM Service` 프롬프트 구성 -> Ollama 생성 -> 답변 반환 -> Web 표시.

## 4. 모듈화 전략 (Modularization)
- **Service Layer Pattern:** API 라우터와 비즈니스 로직(Service)을 명확히 분리하여 테스트 용이성 확보.
- **Interface Driven:** LLM이나 Vector DB 교체가 용이하도록 추상화된 인터페이스 사용 권장.
