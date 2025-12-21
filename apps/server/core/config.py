from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My-Brain AI Assistant"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # LLM & Vector DB
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    CHROMA_DB_PATH: str = "./data/.vector_db"

    class Config:
        case_sensitive = True

settings = Settings()
