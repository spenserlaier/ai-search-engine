from pydantic import BaseModel, RootModel
from typing import List, Optional

class SearchResult(BaseModel):
    title: str
    content: Optional[str] = None
    url: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    analysis: str

class ScoredSearchResponse(SearchResponse):
    score: int

class AnalysisRequest(BaseModel):
    url: str
    query: str

class AnalysisResponse(BaseModel):
    analysis: str

class RewriteRequest(BaseModel):
    query: str

class RewriteResponse(BaseModel):
    rewritten_query: str

class RankingResponse(RootModel[List[ScoredSearchResponse]]):
    pass

class RankingRequest(BaseModel):
    search_results: list[SearchResult]
    query: str





