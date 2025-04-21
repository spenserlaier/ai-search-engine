from fastapi import APIRouter, Query
from searxng_client import search_searxng
from ollama_client import analyze_article, generate_query_response, rank_results, rewrite_query
from models import GenerateAnswerRequest, GenerateAnswerResponse, RankingRequest, RankingResponse, RewriteRequest, RewriteResponse, SearchResult, SearchResponse, AnalysisRequest, AnalysisResponse

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
async def search(query: str = Query(..., min_length=1), 
                 categories: str | None = Query(None),
                 engines: str | None = Query(None)):
    print("received query from backend: ", query)
    print("received category list from the backend: ", categories)
    raw_results = await search_searxng(query, categories)

    # You can even validate/clean results here if needed
    parsed_results = [SearchResult(**r) for r in raw_results]
    for p in raw_results:
        if "thumbnail" in p: print(p["thumbnail"]);
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
    # TODO: sorting is done in the backend, so we may not need a RankingResponse
    # (which includes the llm scores)-- we may just want to return a regular
    # searchresponse
    response = await rank_results(request)
    return response

@router.post("/smart-search", response_model=SearchResponse)
async def rewrite(request: RewriteRequest):
    response: RewriteResponse = await rewrite_query(request)
    search_results = await search(response.rewritten_query)
    print("finished smart search: ", search_results)
    return search_results

@router.post("/generate-answer", response_model=GenerateAnswerResponse)
async def generateAnswer(request: GenerateAnswerRequest):
    response: GenerateAnswerResponse = await generate_query_response(request)
    return response



