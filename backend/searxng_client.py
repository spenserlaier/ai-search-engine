import http_client
from models import SearchRequest
SEARXNG_URL = "http://localhost:8000"

async def search_searxng(query: str, categories: str | None= None, page_number: int =1  ):
    #print("this is the page number we received in backend: ", page_number)
    #print("this is the category we received in backend: ", categories)
    #print("this is the query we received in backend: ", query)
    params = dict()
    params['q'] = query
    params['format'] = 'json'
    params['pageno'] = page_number
    if categories != None:
        params['categories'] = categories
    response = await http_client.get_client().post(f"{SEARXNG_URL}/search", params=params)
    response.raise_for_status()
    return response.json().get("results", [])


async def search_searxng_post(request: SearchRequest):
    #print("received post request for search: ", request)
    response = await http_client.get_client().post(f"{SEARXNG_URL}/search",
                                                   params={"format": "json"},
                                                   data=request.model_dump(), headers={"Accept": "application/json"})
    response.raise_for_status()
    json = response.json()
    json["query"] = request.q

    #return response.json().get("results", [])
    return json

