from backend.models import SearchResult
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

async def rewrite_query(query: str):
    system_prompt = (
    "You are a search assistant tasked with improving user queries to optimize them for better search results.\n"
    "Your task is to rewrite the user's query in a way that will return more relevant and accurate results from the search engine.\n"
    "Consider the following when rewriting:\n"
    "1. Clarify vague or ambiguous terms to avoid irrelevant results.\n"
    "2. Use more specific terms to narrow down the scope, ensuring better relevance.\n"
    "3. Remove unnecessary words or concepts that might lead to too broad or irrelevant results.\n"
    "4. If the query is already clear, do not change it unless there is a strong opportunity to optimize it.\n\n"
    "Provide the rewritten query in a simple, natural form without excessive alterations.\n"
    "Return only the original query or its optimized variation, and nothing else."
)
    user_prompt = f"Query: {query}"
    response = await generate_model_response(user_prompt, False, system_prompt)
    return response

def format_search_results(results: list[SearchResult]) -> str:
    formatted = []
    for i, result in enumerate(results, start=1):
        formatted.append(
                f"{i}. Title: \"{result.title}\"\n   Snippet: \"{result.content}\" URL: \"{result.url}\""
        )
    return "\n\n".join(formatted)

async def rank_results(query: str, results: list[SearchResult]):
    system_prompt = (
    "You are an intelligent search assistant tasked with evaluating search results based on their relevance to a given query.\n"
    "Each result includes a title and a snippet.\n\n"
    "For each result, evaluate its relevance to the query on a scale from 0 to 10, where:\n"
    " - 10 means the snippet directly and thoroughly answers the query.\n"
    " - 0 means the snippet is completely unrelated.\n\n"
    "Output your results in the following JSON format (as a list of objects):\n\n"
    "[\n"
    "  {\n"
    "    \"score\": <integer between 0-10>,\n"
    "    \"title\": \"<title of the source>\",\n"
    "    \"snippet\": \"<snippet from the article>\"\n"
    "    \"url\": \"<article url>\"\n"
    "  },\n"
    "  ...\n"
    "]\n\n"
    "Do not include anything else outside the JSON array.\n"
    "Do NOT include YouTube results unless they are highly relevant to the query.\n"
)
    formatted_results = format_search_results(results)
    response = await generate_model_response(formatted_results, False, system_prompt)
    return response

