import http_client
SEARXNG_URL = "http://localhost:8000"

async def search_searxng(query: str, categories: str | None= None):
    params = dict()
    params['q'] = query
    params['format'] = 'json'
    if categories != None:
        params['categories'] = categories
    response = await http_client.get_client().get(f"{SEARXNG_URL}/search", params=params)
    response.raise_for_status()
    return response.json().get("results", [])

