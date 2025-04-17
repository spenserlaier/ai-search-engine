from fastapi import APIRouter, Query
from searxng_client import search_searxng
from ollama_client import analyze_results, analyze_article, rank_results
from models import RankingRequest, RankingResponse, SearchResult, SearchResponse, AnalysisRequest, AnalysisResponse

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search(query: str = Query(..., min_length=1)):
    print("received query from backend: ", query)
    raw_results = await search_searxng(query)

    # You can even validate/clean results here if needed
    parsed_results = [SearchResult(**r) for r in raw_results]

    #analysis = await analyze_results(query, parsed_results)
    analysis = "this is a sample analysis"
    return SearchResponse(
        query=query,
        results=parsed_results,
        analysis=analysis
    )
@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    print("received analysis request: ", request)
    response = await analyze_article(request.url, request.query)
    print("generated analysis response: ", response)
    return response

@router.post("/rank", response_model=RankingResponse)
async def rank(request: RankingRequest):
    response = await rank_results(request)
    return response

