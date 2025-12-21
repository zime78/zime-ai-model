from apps.server.services.llm import llm_service
from apps.server.services.rag import rag_engine
from datetime import datetime

class EvaluationService:
    def __init__(self):
        pass

    async def evaluate_performance(self, period: str = "1 year"):
        """
        RAG를 사용하여 업무 히스토리를 검색하고, 성과를 요약/평가합니다.
        """
        # 1. 관련 업무 로그 검색
        # "Work Log", "Project", "Achievements" 키워드로 검색
        query = f"My work history, achievements, and completed tasks for the last {period}"
        docs = rag_engine.search(query, k=20) # 많은 문맥 필요
        
        context = "\n\n".join([doc.page_content for doc in docs])
        
        if not context:
            return "No work history found to evaluate."

        # 2. LLM 평가 프롬프트
        system_prompt = """
        당신은 사려 깊고 객관적인 'AI 인사 담당자' 및 '성과 관리자'입니다.
        사용자의 업무 로그 데이터를 바탕으로 성과 평가(Performance Review) 초안을 작성해주세요.
        
        다음 구조로 작성하세요 (한국어):
        1. **주요 성과 요약 (Key Achievements)**: 성공적으로 완료한 프로젝트와 임팩트.
        2. **강점 분석 (Strengths)**: 업무 수행에서 드러난 사용자의 강점.
        3. **개선 영역 (Areas for Improvement)**: 보완이 필요한 부분이나 아쉬운 점.
        4. **총평 (Overall Summary)**: 전체적인 평가 및 다음 기간에 대한 조언.
        
        데이터에 기반하여 구체적으로 작성하고, 없는 내용은 지어내지 마십시오.
        """
        
        prompt = f"""
        다음은 사용자의 최근 업무 로그 및 프로젝트 기록입니다:
        
        {context}
        
        위 내용을 바탕으로 {period} 동안의 업무 성과를 평가해주세요.
        """
        
        response = llm_service.generate_response(prompt, system_prompt=system_prompt)
        return response

evaluation_service = EvaluationService()
