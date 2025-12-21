"""
애플리케이션 설정 관리
환경변수를 통해 설정값을 주입받습니다.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 기본 설정
    PROJECT_NAME: str = "My-Brain AI Assistant"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # 서버 설정
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # CORS (쉼표로 구분된 문자열 또는 리스트)
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        """쉼표로 구분된 문자열을 리스트로 변환"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # LLM 설정
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5vl:7b"
    OLLAMA_TIMEOUT: int = 120

    # Vector DB
    CHROMA_DB_PATH: str = "./data/.vector_db"
    USE_CHROMADB: bool = False

    # 데이터 경로
    DATA_DIR: str = "./data"
    COMPANY_DATA_DIR: str = "./data/company"
    PERSONAL_DATA_DIR: str = "./data/personal"
    PROJECT_DATA_DIR: str = "./data/project"

    # 로깅
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json | text

    # 성능
    WORKERS_COUNT: int = 4
    REQUEST_TIMEOUT: int = 60

    @property
    def is_production(self) -> bool:
        """프로덕션 환경 여부"""
        return self.ENVIRONMENT == "production"

    @property
    def is_debug(self) -> bool:
        """디버그 모드 여부"""
        return self.DEBUG and not self.is_production

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """캐시된 설정 인스턴스 반환"""
    return Settings()


settings = get_settings()
