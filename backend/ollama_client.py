import http_client
from readability import Document
import httpx
from bs4 import BeautifulSoup
import json

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma3:4b"

async def generate_model_response(prompt="", stream=False, system_prompt=""):
    print('attempting to generate model response')
    response = None
    if system_prompt:
        response = await http_client.get_client().post(f"{OLLAMA_URL}/api/chat", json={
        "model": OLLAMA_MODEL,  # or your chosen model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "stream": False
        })
        print("got llm response: ", response.json())
    else:
        response = await http_client.get_client().post(f"{OLLAMA_URL}/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": stream
            })
    response.raise_for_status()
    return response.json()["message"]["content"]

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
        system_prompt = (
    "You are a strict snippet extractor.\n"
    "Your job is to read an article and extract the single most relevant quoted snippet "
    "that answers a user's query.\n\n"
    "Your response must follow this exact format (with no additions):\n"
    "\"<quoted passage from the article>\"\n"
    "<brief explanation of how the snippet directly answers or relates to the query>\n\n"
    "If the snippet chosen is not highly relevant to the query as presented, simply return the string 'Analysis unavailable for this link'."
    "Do NOT include greetings, summaries, bullet points, markdown, or commentary.\n"
    "Do NOT answer the query yourself — only extract from the article.\n"
    "Focus on literal and factual relevance — not metaphor, humor, or symbolic associations."
        )
        user_prompt = f"""Query: {query}
Article:
{article_text}
"""
        response = await generate_model_response(user_prompt, False, system_prompt)
        print("received response: ", response)
        return response
    else:
        return "analysis unavailable for this article"
