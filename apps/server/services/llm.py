import warnings
from langchain_core._api import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from apps.server.core.config import settings
import base64

class LLMService:
    def __init__(self):
        # TODO: settings에서 모델명 가져오도록 수정 (현재 하드코딩 또는 기본값)
        self.model_name = "qwen2.5vl:7b"
        self.llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=self.model_name  # 로컬 가용 모델 사용
        )

    def check_connection(self) -> bool:
        """Ollama 서버 연결 확인"""
        try:
            # 간단한 메타데이터 요청으로 연결 확인
            self.llm.invoke([HumanMessage(content="test")])
            return True
        except Exception:
            return False

    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
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

llm_service = LLMService()
