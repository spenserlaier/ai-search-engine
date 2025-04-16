from http_client import client
SEARXNG_URL = "http://localhost:8080"

async def search_searxng(query: str):
    response = await http_client.get(f"{SEARXNG_URL}/search", params={"q": query, "format": "json"})
    response.raise_for_status()
    return response.json().get("results", [])

