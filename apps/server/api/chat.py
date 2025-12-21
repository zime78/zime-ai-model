from fastapi import APIRouter
from pydantic import BaseModel
from apps.server.services.llm import llm_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    system_prompt = f"""
    당신은 'My-Brain'이라는 이름을 가진 유용한 AI 비서입니다.
    사용자의 업무와 지식 관리를 돕기 위해 존재합니다.
    
    당신의 핵심 모델은 '{llm_service.model_name}'이며, 컴퓨터 로컬 환경(Ollama)에서 실행되고 있습니다.
    절대로 당신이 GPT-3, GPT-4 또는 OpenAI의 모델이라고 말하지 마십시오.
    
    항상 한국어로 정중하고 명확하게 답변하십시오.
    """
    response = llm_service.generate_response(request.message, system_prompt=system_prompt)
    return {"response": response}
