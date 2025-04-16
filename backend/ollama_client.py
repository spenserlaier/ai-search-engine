import http_client
from readability import Document
import httpx
from bs4 import BeautifulSoup

OLLAMA_URL = "http://localhost:11434"

async def generate_model_response(prompt, stream=False):
    response = await http_client.get_client().post(f"{OLLAMA_URL}/api/generate", json={
        "model": "gemma",
        "prompt": prompt,
        "stream": stream
        })
    response.raise_for_status()
    return response.json()["response"]

async def analyze_results(query: str, results: list):
    text_blob = "\n".join([r["title"] + "\n" + r.get("content", "") for r in results])
    prompt = f"Analyze these search results for '{query}':\n{text_blob}"
    response = await generate_model_response(prompt)
    return response

async def extract_article_text(url: str) -> str:
    response = await httpx.AsyncClient().get(url, timeout=10)
    response.raise_for_status()

    doc = Document(response.text)
    summary_html = doc.summary()

    soup = BeautifulSoup(summary_html, "html.parser")
    text = soup.get_text()
    return text.strip()


async def analyze_article(url: str, query: str):
    article_text = extract_article_text(url)
    prompt = f'Given the following query: {query}, probe the provided article text for a relevant snippet that helps to answer the query. You may also provide additional context which helps to explain the relevance of the query, insofar as it clarifies or expands upon the relevant snippet. Return your response in the following format:  {{"snippet":"<snippet>", "relevance": "<relevance>"}}. Here is the article text: {article_text}'
    response = await generate_model_response(prompt)
    return response
