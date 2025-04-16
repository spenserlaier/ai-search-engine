from fastapi import APIRouter, Query
from searxng_client import search_searxng
from ollama_client import analyze_results
from models import SearchResult, SearchResponse

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

