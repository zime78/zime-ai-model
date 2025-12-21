from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import aiofiles
from typing import List, Optional
from apps.server.services.evaluation import evaluation_service

router = APIRouter()

WORK_LOG_DIR = "data/personal/work_logs"

class WorkLogCreate(BaseModel):
    content: str
    tags: List[str] = []
    category: str = "daily"  # daily, weekly, project

@router.post("/logs")
async def create_work_log(log: WorkLogCreate):
    """
    업무 로그를 생성하여 마크다운 파일로 저장합니다.
    저장된 파일은 Ingestion Service에 의해 자동으로 인덱싱됩니다.
    """
    if not os.path.exists(WORK_LOG_DIR):
        os.makedirs(WORK_LOG_DIR, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    filename = f"{date_str}.md"
    filepath = os.path.join(WORK_LOG_DIR, filename)
    
    # 마크다운 형식으로 추가 (Existing file append or create new)
    log_entry = f"""
## [{timestamp}] [{log.category.upper()}]
**Tags:** {", ".join(log.tags)}

{log.content}

---
"""
    
    try:
        async with aiofiles.open(filepath, mode='a', encoding='utf-8') as f:
            await f.write(log_entry)
            
        return {"status": "success", "file": filename, "message": "Work log saved and will be indexed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def list_work_logs():
    """저장된 업무 로그 날짜 목록 조회"""
    if not os.path.exists(WORK_LOG_DIR):
        return []
    
    files = [f.replace(".md", "") for f in os.listdir(WORK_LOG_DIR) if f.endswith(".md")]
    files.sort(reverse=True)
    return files

@router.get("/logs/{date}")
async def get_work_log(date: str):
    """특정 날짜의 업무 로그 조회 (YYYY-MM-DD)"""
    filepath = os.path.join(WORK_LOG_DIR, f"{date}.md")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Log not found")
        
    async with aiofiles.open(filepath, mode='r', encoding='utf-8') as f:
        content = await f.read()
    
    return {"date": date, "content": content}

@router.get("/evaluation/summary")
async def get_work_evaluation(period: str = "1 year"):
    """
    최근 업무 히스토리를 기반으로 AI 성과 평가를 수행합니다.
    """
    summary = await evaluation_service.evaluate_performance(period)
    return {"period": period, "evaluation": summary}
