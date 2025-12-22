from apps.server.services.llm.handlers.base import BaseHandler
from apps.server.services.rag import rag_engine

class TreeHandler(BaseHandler):
    tree_keywords = ["트리", "폴더 구조", "구조", "폴더 보여줘"]
    image_keywords = ["이미지", "사진", "그림", "캡쳐"]

    def can_handle(self, prompt: str) -> bool:
        return any(kw in prompt for kw in self.tree_keywords)

    def handle(self, prompt: str) -> str:
        print(f"[LLM] Folder tree request detected.")
        is_image_request = any(kw in prompt for kw in self.image_keywords)

        if is_image_request:
            try:
                img_base64 = rag_engine.get_tree_image()
                return f"\n\n[폴더 구조 이미지]:\n![Folder Structure](data:image/png;base64,{img_base64})\n\n위 이미지는 현재 폴더 구조를 시각화한 것입니다."
            except Exception as e:
                print(f"[LLM] Failed to generate tree image: {e}")
                tree_str = rag_engine.get_tree_structure()
                return f"\n\n[현재 폴더 구조/Folder Tree]:\n```\n{tree_str}\n```\n\n(이미지 생성에 실패하여 텍스트로 보여드립니다. 위 텍스트는 반드시 코드 블록으로 감싸서 보여주세요.)"
        else:
            tree_str = rag_engine.get_tree_structure()
            return f"\n\n[현재 폴더 구조/Folder Tree]:\n```\n{tree_str}\n```\n\n사용자가 폴더 구조를 물어보면 위 트리 형태를 반드시 멀티라인 코드 블록(```)으로 감싸서 줄바꿈을 유지하여 보여주세요."
