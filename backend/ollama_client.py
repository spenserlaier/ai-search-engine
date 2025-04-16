import http_client

OLLAMA_URL = "http://localhost:11434"

async def analyze_results(query: str, results: list):
    text_blob = "\n".join([r["title"] + "\n" + r.get("content", "") for r in results])
    prompt = f"Analyze these search results for '{query}':\n{text_blob}"
    response = await http_client.get_client().post(f"{OLLAMA_URL}/api/generate", json={
        "model": "gemma",
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    return response.json()["response"]

