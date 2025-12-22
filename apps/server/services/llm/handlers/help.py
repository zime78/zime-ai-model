from apps.server.services.llm.handlers.base import BaseHandler

class HelpHandler(BaseHandler):
    keywords = ["도움말", "명령어", "기능", "할 수 있는 것", "사용법"]

    def can_handle(self, prompt: str) -> bool:
        return any(kw in prompt for kw in self.keywords)

    def handle(self, prompt: str) -> str:
        print(f"[LLM] Help request detected.")
        help_message = """
## 🤖 My-Brain 사용 가이드

현재 다음 기능들을 사용하실 수 있습니다:

### 1. 📂 파일 및 구조 조회
- **파일 목록**: "현재 파일 목록 보여줘", "어떤 파일이 있어?"
- **폴더 구조 (텍스트)**: "폴더 구조 보여줘", "트리 구조 알려줘"
- **폴더 구조 (이미지)**: "폴더 구조 이미지로 보여줘", "트리 사진 보여줘"

### 2. 🔍 지식 검색 (RAG)
- 궁금한 내용을 질문하면 학습된 파일 내용을 바탕으로 답변합니다.
- 예: "Q앱 버전이 뭐야?", "프로젝트 일정 알려줘"

### 3. 중복/환각 방지
- 저는 학습된 데이터에 기반해서만 답변합니다.
- 모르는 내용은 솔직하게 모른다고 답변드립니다.
"""
        return f"\n\n[시스템 도움말/Help Message]:\n{help_message}\n\n사용자가 도움말을 요청했습니다. 위 내용을 마크다운 형식을 유지하여 깔끔하게 보여주세요."
