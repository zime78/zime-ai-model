# 구현 계획: 나만의 AI 비서 (My-Brain)

## 목표 설명
Apple Silicon (M1 Max) 환경에서 로컬로 동작하는 개인화된 AI 비서를 구축합니다. 개인 데이터(회사, 개인, 프로젝트 폴더)를 수집하여 시맨틱 검색과 채팅을 지원하며, 업무 현황 파악 및 성과 평가를 보조하는 기능을 목표로 합니다.

**주요 요구사항:**
- **로컬 AI:** Ollama (Llama 3 또는 Mistral 등 효율적인 소형 모델 사용).
- **지원 언어:** 한국어, 영어.
- **데이터 소스:** 이미지, 텍스트, 마크다운, URL.
- **접근성:** 내부 네트워크 (다른 기기에서도 접속 가능).
- **주요 기능:** 검색, 채팅, 업무 히스토리, 대시보드.

## 개발 지침 (Guidelines)
1.  **언어:** 주석(Comments), 코드 설명, AI 답변, 사용자 가이드 등 모든 텍스트는 **한국어(Korean)**로 작성합니다.
    - 변수명, 함수명 등 코드는 영어를 사용하되, 설명은 한글로 작성합니다.
2.  **문서화 (Documentation):**
    - **문서 작업:** 주요 기능 구현 시 관련 문서를 작성합니다.
    - **아키텍처(구조) 문서:** 전체 시스템 구조를 파악할 수 있는 아키텍처 문서를 작성하고 유지 관리합니다.
3.  **개발 프로세스:**
    - **단계별 진행:** 기능 단위로 나누어 단계별로 개발을 진행합니다.
    - **단계별 빌드 점검:** 각 단계 완료 시 빌드 및 테스트를 수행하여 문제가 없는지 확인합니다.
    - **모듈화:** 구조적 변경이나 문제 발생 시 쉽게 처리할 수 있도록 기능별로 모듈을 분리합니다.

## 사용자 검토 필요
> [!IMPORTANT]
> **대용량 데이터 초기 성능:** 많은 양의 파일(특히 이미지)을 초기 인덱싱할 때 CPU 사용량이 높을 수 있습니다. 이를 완화하기 위해 백그라운드 처리를 구현할 예정입니다.

> [!NOTE]
> **네트워크 접속:** 다른 컴퓨터에서 접속하려면 서버를 `0.0.0.0` 또는 특정 LAN IP로 바인딩해야 합니다. Mac의 방화벽 설정 확인이 필요할 수 있습니다.

## 제안된 아키텍처

### 기술 스택 (Tech Stack)
- **프론트엔드:** Next.js (React) - 모던하고 반응형인 UI.
- **백엔드:** Python (FastAPI) - 강력한 API 처리 및 AI 라이브러리 연동 용이.
- **AI/LLM:** Ollama (로컬 실행).
- **오케스트레이션:** LangChain 또는 LlamaIndex (RAG 파이프라인용).
- **벡터 데이터베이스:** ChromaDB (간편한 로컬 설정) 또는 FAISS.
- **파일 감시:** Python `watchdog` 라이브러리를 사용한 실시간 업데이트.

### 시스템 구성 요소
1.  **수집 엔진 (Ingestion Engine):** 폴더를 감시하고, 파일을 읽고(이미지는 OCR), 텍스트를 청킹(chunking)하여 Vector DB에 임베딩합니다.
2.  **검색 시스템 (Retrieval System - RAG):** 사용자 질문에 기반하여 Vector DB에서 관련 내용을 검색합니다.
3.  **LLM 서비스:** 검색된 문맥을 사용하여 Ollama에 연결하고 답변을 생성합니다.
4.  **웹 UI:** 시스템 상태 대시보드 및 상호작용을 위한 채팅 인터페이스입니다.

## 제안된 변경 사항

### 디렉토리 구조
현재 디렉토리에서 Monorepo 구조를 사용할 예정입니다:
```
/Users/zime/Git/zime-ai-model/
├── apps/
│   ├── web/ (Next.js 프론트엔드)
│   └── server/ (FastAPI 백엔드)
├── data/ (인덱싱될 폴더들 - 외부 드라이브나 폴더를 이곳에 매핑 가능)
│   ├── company/
│   ├── personal/
│   └── project/
└── scripts/ (유틸리티 스크립트)
```

### [백엔드] AI 코어 & API
#### [NEW] apps/server/main.py
- FastAPI 진입점 (Entry point).
- 엔드포인트: `/chat`, `/query`, `/status`, `/index/refresh`.

#### [NEW] apps/server/rag_engine.py
- LlamaIndex/LangChain 파이프라인 설정.
- ChromaDB 연결 설정.

#### [NEW] apps/server/ingest.py
- 파일 처리 로직.
- 파일 변경 시 인덱스를 자동 업데이트하기 위한 Watchdog 옵저버 설정.
- [.md](file:///Users/zime/.gemini/antigravity/brain/5aa34699-302d-46ce-9e4d-d631679215a5/task.md), `.txt`, `.png/.jpg` (Ollama의 Vision 모델 또는 Tesseract/EasyOCR 사용) 처리를 위한 핸들러.

### [프론트엔드] 웹 클라이언트
#### [NEW] apps/web/
- 표준 Next.js 설정.
- **페이지 구성:**
    - `index.tsx`: 대시보드 (시스템 상태, 최근 인덱싱된 파일).
    - `chat.tsx`: 메인 채팅 인터페이스.
    - `history.tsx`: 과거 대화 및 작업 로그 확인.
    - `settings.tsx`: 폴더 경로 및 모델 파라미터 설정.

## 검증 계획

### 자동화 테스트
- **백엔드:** 파일 파싱 및 임베딩 생성 로직 단위 테스트 (LLM 모킹).
- **통합 테스트:** "파일 추가" -> "검색 결과에 내용 표시" 까지의 End-to-End 흐름 테스트.

### 수동 검증
1.  **Ollama 시작:** `ollama serve` 실행 확인.
2.  **백엔드 시작:** `cd apps/server && uvicorn main:app --host 0.0.0.0`.
3.  **프론트엔드 시작:** `cd apps/web && npm run dev`.
4.  **접속 테스트:** Mac에서 `http://localhost:3000`, 다른 기기에서 `http://<MAC-IP>:3000` 접속 확인.
5.  **수집 테스트:** `data/personal` 폴더에 파일을 넣고 검색 결과에 나오는지 확인.
