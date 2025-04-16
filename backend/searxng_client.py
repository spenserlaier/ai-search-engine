import http_client
SEARXNG_URL = "http://localhost:8000"

async def search_searxng(query: str):
    response = await http_client.get_client().get(f"{SEARXNG_URL}/search", params={"q": query, "format": "json"})
    response.raise_for_status()
    return response.json().get("results", [])

