from abc import ABC, abstractmethod

class BaseHandler(ABC):
    @abstractmethod
    def can_handle(self, prompt: str) -> bool:
        """이 핸들러가 해당 prompt를 처리할 수 있는지 판단"""
        pass

    @abstractmethod
    def handle(self, prompt: str) -> str:
        """처리 로직을 수행하고 context 텍스트를 반환 (시스템 프롬프트에 주입될 내용)"""
        pass
