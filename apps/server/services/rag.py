import os
from langchain_core.documents import Document
from apps.server.core.config import settings

class SimpleRAGEngine:
    """
    ChromaDB 설치 실패 대비용 경량 인메모리 검색 엔진.
    단순 키워드 매칭 기반으로 동작합니다.
    """
    def __init__(self):
        self.documents = []

    def add_text(self, text: str, meta: dict):
        """텍스트를 메모리에 저장"""
        # 단순화를 위해 전체 텍스트를 하나의 문서로 저장
        doc = Document(page_content=text, metadata=meta)
        self.documents.append(doc)
        print(f"[RAG] Indexed document: {meta.get('filename')}")

    def search(self, query: str, k: int = 3):
        """단순 키워드 검색"""
        results = []
        query_terms = query.lower().split()
        
        for doc in self.documents:
            content_lower = doc.page_content.lower()
            score = 0
            for term in query_terms:
                if term in content_lower:
                    score += 1
            
            if score > 0:
                results.append((doc, score))
        
        # 점수순 정렬
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:k]]

# ChromaDB 대신 SimpleRAGEngine 사용
rag_engine = SimpleRAGEngine()
