import http_client
from readability import Document
import httpx
from bs4 import BeautifulSoup
import json

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma3:4b"

async def generate_model_response(prompt, stream=False):
    print('attempting to generate model response')
    response = await http_client.get_client().post(f"{OLLAMA_URL}/api/generate", json={
        "model": OLLAMA_MODEL,
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
    print("extracting article text from url: ", url)
    try:
        response = await httpx.AsyncClient().get(url, timeout=10, follow_redirects=False)
        # redirects get messy on certain websites, might need special procedures to handle them
        response.raise_for_status()
        print("got extracted response: ", response)

        doc = Document(response.text)
        summary_html = doc.summary()

        soup = BeautifulSoup(summary_html, "html.parser")
        text = soup.get_text()
        return text.strip()
    except Exception:
        return ""

async def analyze_article(url: str, query: str):
    article_text = await extract_article_text(url)
    print(article_text)
    if article_text != None and article_text != "":
        prompt = f"""
Query: {query}

You are an assistant that analyzes an article to find content relevant to the user's query above.

Your task:
- Read the article below.
- Identify the most relevant snippet that directly answers or relates to the query.
- Relevance should be based on literal, factual connection — not metaphorical, symbolic, or humorous interpretation.
- Briefly explain why the snippet is relevant.

Example:
Query: What are the fastest land animals?
Article: "Cheetahs can reach speeds of up to 70 mph, making them the fastest land animal. Falcons are even faster, but they fly."
Snippet: "Cheetahs can reach speeds of up to 70 mph, making them the fastest land animal."
Relevance: It directly answers the query by naming and describing the fastest land animal.

Format your response like this (no extra commentary):
Snippet: "<the relevant sentence or passage from the article>"
Relevance: <a short explanation of how it answers or relates to the query>

Article:
{article_text}
"""
        response = await generate_model_response(prompt)
        print("received response: ", response)
        return response
    else:
        return "analysis unavailable for this article"
