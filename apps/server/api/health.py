"""
헬스체크 API
서비스 상태, 시스템 리소스, 의존성 상태를 확인합니다.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import httpx
import psutil

from apps.server.core.config import settings

router = APIRouter(tags=["Health"])


class ServiceStatus(BaseModel):
    """개별 서비스 상태"""
    status: str
    details: Dict[str, Any] = {}


class SystemMetrics(BaseModel):
    """시스템 리소스 메트릭"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float


class HealthResponse(BaseModel):
    """전체 헬스체크 응답"""
    status: str
    version: str
    environment: str
    services: Dict[str, ServiceStatus]
    system: SystemMetrics


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    상세 헬스체크
    모든 서비스 상태와 시스템 메트릭을 반환합니다.
    """
    services = {}

    # Ollama 상태 확인
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                services["ollama"] = ServiceStatus(
                    status="healthy",
                    details={"models_count": len(models)}
                )
            else:
                services["ollama"] = ServiceStatus(
                    status="unhealthy",
                    details={"error": f"HTTP {resp.status_code}"}
                )
    except Exception as e:
        services["ollama"] = ServiceStatus(
            status="unhealthy",
            details={"error": str(e)}
        )

    # RAG 엔진 상태 확인
    try:
        from apps.server.services.rag import rag_engine
        doc_count = len(rag_engine.documents) if hasattr(rag_engine, 'documents') else 0
        services["rag"] = ServiceStatus(
            status="healthy",
            details={
                "documents_count": doc_count,
                "type": "chromadb" if settings.USE_CHROMADB else "in-memory"
            }
        )
    except Exception as e:
        services["rag"] = ServiceStatus(
            status="unhealthy",
            details={"error": str(e)}
        )

    # 시스템 리소스
    system = SystemMetrics(
        cpu_percent=psutil.cpu_percent(interval=0.1),
        memory_percent=psutil.virtual_memory().percent,
        disk_percent=psutil.disk_usage('/').percent
    )

    # 전체 상태 결정
    overall_status = "healthy"
    for service in services.values():
        if service.status == "unhealthy":
            overall_status = "degraded"
            break

    return HealthResponse(
        status=overall_status,
        version="0.1.0",
        environment=settings.ENVIRONMENT,
        services=services,
        system=system
    )


@router.get("/health/live")
async def liveness() -> Dict[str, str]:
    """
    Liveness Probe
    서버가 살아있는지만 확인합니다.
    """
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness() -> Dict[str, str]:
    """
    Readiness Probe
    서버가 요청을 받을 준비가 되었는지 확인합니다.
    Ollama 연결이 필수입니다.
    """
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                return {"status": "ready"}
            raise HTTPException(status_code=503, detail="Ollama not responding")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Ollama connection failed: {e}")
