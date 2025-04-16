from pydantic import BaseModel
from typing import List, Optional

class SearchResult(BaseModel):
    title: str
    content: Optional[str] = None
    url: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    analysis: str
