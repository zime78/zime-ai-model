"""
My-Brain AI Assistant - FastAPI 애플리케이션 진입점
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from apps.server.core.config import settings
from apps.server.core.logging import setup_logging
from apps.server.core.middleware import RequestTimingMiddleware
from apps.server.api.routes import router as api_router
from apps.server.api.health import router as health_router
from apps.server.services.ingest import ingestion_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # Startup
    setup_logging()
    ingestion_service.start_watching()
    yield
    # Shutdown
    ingestion_service.stop_watching()


def create_app() -> FastAPI:
    """FastAPI 애플리케이션 생성"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs" if settings.is_debug else None,
        redoc_url="/redoc" if settings.is_debug else None,
        lifespan=lifespan
    )

    # 요청 타이밍 미들웨어
    app.add_middleware(RequestTimingMiddleware)

    # CORS 설정 (환경별 분리)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
        max_age=600,  # preflight 캐시 10분
    )

    # API 라우터
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # 헬스체크 라우터 (prefix 없이)
    app.include_router(health_router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "apps.server.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.is_debug,
    )
