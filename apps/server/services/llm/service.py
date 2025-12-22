import warnings
from langchain_core._api import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from apps.server.core.config import settings
import base64

# Handlers
from apps.server.services.llm.handlers.file_list import FileListHandler
from apps.server.services.llm.handlers.folder_tree import TreeHandler
from apps.server.services.llm.handlers.help import HelpHandler
from apps.server.services.llm.handlers.rag import RAGHandler

class LLMService:
    def __init__(self):
        # TODO: settings에서 모델명 가져오도록 수정
        self.model_name = "qwen2.5vl:7b"
        self.llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=self.model_name
        )
        
        # Register handlers (Order matters!)
        self.handlers = [
            HelpHandler(),
            TreeHandler(),
            FileListHandler(),
            RAGHandler() # Fallback handler
        ]

    def check_connection(self) -> bool:
        """Ollama 서버 연결 확인"""
        try:
            self.llm.invoke([HumanMessage(content="test")])
            return True
        except Exception:
            return False

    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        context_text = ""
        
        # Dispatcher strategies
        for handler in self.handlers:
            if handler.can_handle(prompt):
                context_text = handler.handle(prompt)
                break
        
        # Construct messages
        messages = []
        if system_prompt:
            combined_system_prompt = system_prompt
            
            # Core Instructions
            combined_system_prompt += """
\n[핵심 지침/Core Instructions]
1. **사실 기반 답변**: 제공된 [참고 자료]에 없는 내용은 절대 지어내지 마십시오. 정보가 부족하면 "제공된 문서에 해당 내용이 없어 알 수 없습니다"라고 정중히 답하십시오.
2. **가독성**: 긴 답변은 반드시 불릿 포인트(-), 번호 매기기(1.), 단락 나누기를 사용하여 가독성을 높이십시오.
3. **폴더/파일 구조**: 텍스트로 된 트리 구조는 반드시 멀티라인 코드 블록(```)으로 감싸서 표현하십시오.
"""

            if context_text:
                combined_system_prompt += f"\n\n다음은 사용자의 질문과 관련된 참고 자료입니다. 답변 시 이를 적극 활용하십시오.\n{context_text}"
                
                # Image instruction
                if "![Folder Structure]" in context_text:
                    combined_system_prompt += "\n\n[IMPORTANT INSTRUCTION]: 참고 자료에 포함된 `![Folder Structure](...)` 이미지를 답변에 그대로 포함하여 사용자에게 보여주십시오. 텍스트 인터페이스라 하더라도 마크다운 이미지는 렌더링될 수 있습니다. '이미지를 보여줄 수 없다'고 거절하지 마십시오."
            
            messages.append(SystemMessage(content=combined_system_prompt))
        
        messages.append(HumanMessage(content=prompt))

        response = self.llm.invoke(messages)
        return response.content
    
    def describe_image(self, image_path: str) -> str:
        """이미지 파일을 읽어서 설명을 생성합니다."""
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": "Describe this image in detail, including text (OCR) if present."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
            ]
        )
        
        response = self.llm.invoke([message])
        return response.content

    async def a_generate_response_stream(self, prompt: str):
        # Streaming response implementation
        async for chunk in self.llm.astream([HumanMessage(content=prompt)]):
            yield chunk.content
