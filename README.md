# 🧠 My-Brain AI - 나만의 개인 AI 비서

> Apple Silicon (M1 Max) 환경에 최적화된 로컬 AI 비서 시스템

My-Brain은 로컬에서 동작하는 개인화된 AI 비서입니다. Ollama를 통한 로컬 LLM, FastAPI 백엔드, Next.js 프론트엔드로 구성되어 있으며, 개인 문서를 기반으로 한 RAG(검색 증강 생성) 기능을 제공합니다.

---

## ✨ 주요 기능

- 🤖 **AI 채팅**: Ollama 기반 로컬 LLM과 대화
- 🔍 **문서 검색**: 개인 문서를 벡터화하여 시맨틱 검색
- 🖼️ **이미지 분석**: Vision 모델을 활용한 이미지 설명 생성
- 🌐 **URL 크롤링**: 웹 페이지 내용을 수집 및 인덱싱
- 📱 **외부 접속**: 같은 네트워크의 다른 기기(iPad, 모바일)에서 접속 가능
- 🇰🇷 **한국어 지원**: 전체 UI가 한국어로 구성

---

## 📋 사전 요구사항

시작하기 전에 아래 소프트웨어가 설치되어 있어야 합니다:

### 1. Python 3.11 이상

```bash
# macOS (Homebrew 사용)
brew install python@3.11

# 설치 확인
python3 --version
```

> ⚠️ **주의**: Python 3.14는 일부 라이브러리와 호환성 문제가 있을 수 있습니다. 3.11 ~ 3.13 버전을 권장합니다.

### 2. Node.js 18 이상

```bash
# macOS (Homebrew 사용)
brew install node

# 설치 확인
node --version
npm --version
```

### 3. Ollama (로컬 LLM)

Ollama는 로컬에서 LLM을 실행하기 위한 필수 도구입니다.

```bash
# macOS 설치
brew install ollama

# 또는 공식 사이트에서 다운로드
# https://ollama.ai/download
```

#### Ollama 서비스 시작

```bash
# Ollama 서비스 백그라운드 실행
ollama serve
```

#### 필수 모델 다운로드

```bash
# Vision 지원 모델 (이미지 분석용) - 권장
ollama pull qwen2.5-vl:7b

# 일반 대화용 모델 (선택)
ollama pull llama3.1:8b
```

> 💡 **팁**: 모델 다운로드는 시간이 걸릴 수 있습니다. `qwen2.5-vl:7b` 모델은 약 4.7GB입니다.

---

## 🚀 설치 방법

### Step 1: 저장소 클론

```bash
git clone https://github.com/your-username/zime-ai-model.git
cd zime-ai-model
```

### Step 2: 백엔드 설정 (Python)

```bash
# 1. 가상환경 생성
python3 -m venv .venv

# 2. 가상환경 활성화 (macOS/Linux)
source .venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt
```

> ⚠️ **zsh 사용자 주의**: `uvicorn[standard]` 설치 시 에러가 발생하면 따옴표로 감싸야 합니다:
> ```bash
> pip install "uvicorn[standard]"
> ```

### Step 3: 프론트엔드 설정 (Node.js)

```bash
# 웹 앱 디렉토리로 이동
cd apps/web

# 의존성 설치
npm install

# 루트 디렉토리로 돌아오기
cd ../..
```

---

## 📂 학습 데이터 추가 방법

이 프로젝트는 개인 문서를 RAG 시스템에 인덱싱하여 AI가 참조할 수 있게 합니다.

### 데이터 폴더 구조

```
data/
├── company/    # 회사 관련 문서
├── personal/   # 개인 문서
└── project/    # 프로젝트 문서
```

### 지원되는 파일 형식

| 형식 | 확장자 | 설명 |
|------|--------|------|
| 텍스트 | `.txt` | 일반 텍스트 파일 |
| 마크다운 | `.md` | 마크다운 문서 |
| 이미지 | `.png`, `.jpg`, `.jpeg` | Vision 모델로 분석 |
| URL 링크 | `.url` | 웹 페이지 내용 크롤링 |

### 데이터 추가하기

원하는 폴더에 파일을 복사하면 됩니다. 서버가 실행 중이면 자동으로 감지하여 인덱싱합니다.

```bash
# 예시: 개인 노트 추가
cp ~/Desktop/my-notes.md data/personal/

# 예시: 프로젝트 문서 추가
cp -r ~/Projects/my-project/docs/* data/project/
```

> 💡 **팁**: 서버 실행 중에 파일을 추가해도 자동으로 인덱싱됩니다!

---

## ▶️ 실행 방법

### 방법 1: Docker 실행 (권장)

```bash
# 환경변수 설정
cp .env.example .env

# Docker로 서버 시작 (백그라운드)
./scripts/start-server.sh docker

# 로그 확인
docker-compose logs -f
```

### 방법 2: 통합 스크립트 실행

```bash
# 환경변수 설정
cp .env.example .env

# 개발 모드 (핫 리로드)
./scripts/start-server.sh dev

# 프로덕션 모드 (Gunicorn)
./scripts/start-server.sh prod
```

**터미널 2 - 프론트엔드:**

```bash
cd apps/web
npm run dev
```

### 방법 3: 수동 실행

**터미널 1 - 백엔드:**

```bash
# 가상환경 활성화
source .venv/bin/activate

# PYTHONPATH 설정 및 서버 실행
export PYTHONPATH=$PYTHONPATH:$(pwd)
python apps/server/main.py
```

**터미널 2 - 프론트엔드:**

```bash
cd apps/web
npm run dev
```

### 접속하기

- **로컬 접속**: http://localhost:3000
- **외부 기기 접속**: http://[서버-IP]:3000
  - 예: http://192.168.0.38:3000
- **API 문서**: http://localhost:8000/docs (개발 모드)
- **헬스체크**: http://localhost:8000/health

> 💡 같은 WiFi에 연결된 iPad나 스마트폰에서도 접속할 수 있습니다!

---

## 🔧 트러블슈팅

### 1. "ModuleNotFoundError" 에러

```bash
# PYTHONPATH가 설정되지 않은 경우
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

또는 `run_server.sh` 스크립트를 사용하세요 (자동으로 설정됨).

### 2. Ollama 연결 실패

Ollama 서비스가 실행 중인지 확인하세요:

```bash
# Ollama 상태 확인
curl http://localhost:11434/api/tags

# 실행되지 않았다면
ollama serve
```

### 3. 의존성 설치 느림/실패

Apple Silicon에서 일부 패키지는 컴파일이 필요할 수 있습니다:

```bash
# 핵심 패키지 먼저 설치
pip install fastapi uvicorn python-dotenv

# 나머지 설치
pip install -r requirements.txt
```

### 4. ChromaDB 설치 실패

Python 버전 호환성 문제가 있을 수 있습니다:

```bash
# Python 버전 확인
python3 --version

# 3.11 또는 3.12 권장
```

> 💡 chromadb 설치가 어려우면 프로젝트는 자동으로 인메모리 폴백 모드로 동작합니다.

### 5. 포트 충돌

이미 사용 중인 포트인 경우:

```bash
# 8000 포트 사용 중인 프로세스 확인
lsof -i :8000

# 3000 포트 사용 중인 프로세스 확인
lsof -i :3000
```

---

## 📁 프로젝트 구조

```
zime-ai-model/
├── apps/
│   ├── server/              # FastAPI 백엔드
│   │   ├── api/             # API 라우터
│   │   │   └── health.py    # 헬스체크 API
│   │   ├── core/            # 설정 및 핵심 로직
│   │   │   ├── config.py    # 환경변수 설정
│   │   │   ├── logging.py   # 구조화 로깅
│   │   │   └── middleware.py # 미들웨어
│   │   ├── services/        # 비즈니스 로직
│   │   └── main.py          # 서버 진입점
│   └── web/                 # Next.js 프론트엔드
│       └── src/             # React 컴포넌트
├── data/                    # 학습 데이터 (gitignore)
│   ├── company/
│   ├── personal/
│   └── project/
├── scripts/
│   └── start-server.sh      # 서버 시작 스크립트
├── docs/                    # 프로젝트 문서
├── .env.example             # 환경변수 템플릿
├── docker-compose.yml       # Docker 설정
├── Dockerfile.server        # 백엔드 Docker 이미지
├── Dockerfile.web           # 프론트엔드 Docker 이미지
├── gunicorn.conf.py         # Gunicorn 설정
└── requirements.txt         # Python 의존성
```

---

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| **LLM** | Ollama (Qwen2.5-VL, Llama3.1) |
| **백엔드** | FastAPI, Gunicorn, Python 3.11+ |
| **프론트엔드** | Next.js 16, React 19, TypeScript |
| **RAG** | LangChain, ChromaDB |
| **배포** | Docker, Docker Compose |
| **파일 감시** | Watchdog |

---

## ⚠️ 주의사항

1. **개인 데이터 보안**: `data/` 폴더의 내용은 `.gitignore`에 포함되어 있습니다. 민감한 정보가 GitHub에 업로드되지 않도록 주의하세요.

2. **Ollama 필수**: 이 프로젝트는 Ollama 없이는 동작하지 않습니다. 반드시 Ollama를 설치하고 서비스를 실행해야 합니다.

3. **메모리 사용량**: Vision 모델(`qwen2.5-vl:7b`)은 약 8GB 이상의 RAM을 사용합니다. M1 Mac의 경우 16GB 이상의 메모리를 권장합니다.

4. **첫 실행 시 지연**: 모델을 처음 로드할 때 시간이 걸릴 수 있습니다. 이는 정상적인 동작입니다.

5. **네트워크 접속**: 외부 기기에서 접속하려면 방화벽 설정에서 포트 3000, 8000을 허용해야 할 수 있습니다.

---

## 🤝 기여하기

버그 리포트, 기능 제안, Pull Request를 환영합니다!

---

## 📄 라이선스

MIT License
