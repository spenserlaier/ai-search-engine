from pydantic import BaseModel, RootModel, ConfigDict
from typing import List, Optional

class SearchResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    title: str
    content: Optional[str] = None
    url: Optional[str] = None
    img_src: Optional[str] = None
    thumbnail: Optional[str] = None
    score: Optional[float] = None


class SearchResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    query: str
    results: List[SearchResult]
    analysis: Optional[str] = None

class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    q: str
    categories: Optional[str] = None
    pageno: Optional[int] = 1
    format: Optional[str] = "json"

class ScoredSearchResult(SearchResult):
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

class RankingResponse(RootModel[List[ScoredSearchResult]]):
    pass

class RankingRequest(BaseModel):
    search_results: list[SearchResult]
    query: str

class GenerateAnswerRequest(BaseModel):
    query : str

class GenerateAnswerResponse(BaseModel):
    response: str






