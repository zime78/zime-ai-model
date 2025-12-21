from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from apps.server.services.rag import rag_engine

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    k: int = 3

class SearchResult(BaseModel):
    content: str
    metadata: dict

@router.post("/search")
async def search(request: SearchRequest):
    docs = rag_engine.search(request.query, k=request.k)
    results = [
        SearchResult(content=doc.page_content, metadata=doc.metadata)
        for doc in docs
    ]
    return {"results": results}
