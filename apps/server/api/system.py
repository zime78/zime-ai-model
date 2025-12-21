from fastapi import APIRouter
from apps.server.services.ingest import ingestion_service
from pydantic import BaseModel

router = APIRouter()

class ReloadResponse(BaseModel):
    message: str
    status: str

@router.post("/reload", response_model=ReloadResponse)
async def reload_data():
    """
    기존 데이터 폴더를 다시 스캔하여 인덱싱을 갱신합니다.
    (새로 추가된 파일을 인식하거나, 인덱스가 깨졌을 때 유용)
    """
    try:
        ingestion_service.scan_existing_files()
        return ReloadResponse(
            message="Data reload initiated successfully.",
            status="success"
        )
    except Exception as e:
        return ReloadResponse(
            message=f"Failed to reload data: {str(e)}",
            status="error"
        )
