from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to My-Brain API"}

from apps.server.api.chat import router as chat_router
from apps.server.api.rag import router as rag_router
from apps.server.api.work import router as work_router

router.include_router(chat_router, tags=["chat"])
router.include_router(rag_router, tags=["rag"])
router.include_router(work_router, tags=["work"])
