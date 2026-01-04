# 🔍 Ollama LLM 모델 검색 및 문서 검색 최적화 가이드

**조사 완료 날짜**: 2026년 1월 3일 오후 7시  
**출처**: Ollama 공식 모델 라이브러리

---

## 🎯 **임베딩 모델 (Embedding Models) - 파일/문서 검색에 최적**

### 최고 성능 모델들 (최신순)

1️⃣ **nomic-embed-text-v2-moe** - 📅 2025년 1월 (3주 전) ⭐⭐⭐⭐⭐
2️⃣ **qwen3-embedding** - 📅 2024년 10월 (3개월 전) ⭐⭐⭐⭐⭐
3️⃣ **nomic-embed-text** - 📅 2024년 1월 (1년 전) ⭐⭐⭐⭐
4️⃣ **mxbai-embed-large** - 📅 2024년 1월 (1년 전) ⭐⭐⭐⭐
5️⃣ **bge-m3** - 📅 2024년 1월 (1년 전) ⭐⭐⭐⭐

**경량 모델**: all-minilm, snowflake-arctic-embed2, embeddinggemma, paraphrase-multilingual

---

## 💬 **RAG 특화 모델**

1️⃣ **llama3-chatqa** (8B/70B) - 📅 2024년 1월 ⭐⭐⭐⭐⭐
2️⃣ **nemotron-mini** (4B) - 📅 2024년 1월 ⭐⭐⭐⭐⭐ (속도 최고)
3️⃣ **granite3-dense** (2B/8B) - 📅 2024년 1월 ⭐⭐⭐⭐
4️⃣ **granite3.1-dense** (2B/8B) - 📅 2024년 12월 ⭐⭐⭐⭐
5️⃣ **nemotron** (70B) - 📅 2024년 1월 ⭐⭐⭐⭐⭐ (최고 성능)

---

## ⚡ **최종 추천**

### 🥇 최고 추천

- **검색**: qwen3-embedding (0.6B)
- **RAG**: nemotron-mini (4B) 또는 llama3-chatqa (8B)

### 🥈 경량 추천

- **검색**: all-minilm (33m)
- **RAG**: granite3.1-dense (2B)

### 📊 성능 비교표

| 모델 | 용도 | 크기 | 속도 | 정확도 |
|------|------|------|------|--------|
| qwen3-embedding | 검색 | 0.6B-8B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| nemotron-mini | RAG | 4B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| all-minilm | 검색 | 22-33m | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| llama3-chatqa | RAG | 8B/70B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| granite3.1-dense | RAG | 2B/8B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

📚 **참고**: <https://ollama.com/search>
