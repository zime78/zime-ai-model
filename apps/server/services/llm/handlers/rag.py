from apps.server.services.llm.handlers.base import BaseHandler
from apps.server.services.rag import rag_engine

class RAGHandler(BaseHandler):
    def can_handle(self, prompt: str) -> bool:
        # Default handler, always returns True if no other handler caught it
        return True

    def handle(self, prompt: str) -> str:
        print(f"[LLM] Searching RAG for: {prompt}")
        context_docs = rag_engine.search(prompt, k=3)
        
        if context_docs:
            context_text = "\n\n[참고 자료/Documents]:\n"
            for doc in context_docs:
                source = doc.metadata.get('filename', 'Unknown Source')
                context_text += f"Source: {source}\nContent: {doc.page_content}\n---\n"
            print(f"[LLM] Found {len(context_docs)} documents.")
            return context_text
        else:
            print("[LLM] No relevant documents found.")
            return ""
