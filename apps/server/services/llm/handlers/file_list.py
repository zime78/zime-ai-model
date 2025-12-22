from apps.server.services.llm.handlers.base import BaseHandler
from apps.server.services.rag import rag_engine

class FileListHandler(BaseHandler):
    keywords = ["목록", "리스트", "파일들"]

    def can_handle(self, prompt: str) -> bool:
        return any(kw in prompt for kw in self.keywords)

    def handle(self, prompt: str) -> str:
        print(f"[LLM] File list request detected.")
        all_docs = rag_engine.get_all_documents()
        if all_docs:
            doc_list_str = "\n".join([f"- {doc}" for doc in all_docs])
            return f"\n\n[현재 학습된 파일 목록/Indexed Files]:\n{doc_list_str}\n\n사용자가 파일 목록을 물어보면 위 리스트를 정리해서 보여주세요."
        else:
            return "\n\n[현재 학습된 파일 목록]: 없음 (아직 업로드된 파일이 없습니다)."
