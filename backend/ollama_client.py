from pydantic import TypeAdapter, parse_obj_as
from models import AnalysisResponse, GenerateAnswerRequest, GenerateAnswerResponse, RankingRequest, RankingResponse, RewriteRequest, RewriteResponse, ScoredSearchResult, SearchResult
import http_client
from readability import Document
import httpx
import re
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
        }, 
                                                       timeout=15)
    else:
        response = await http_client.get_client().post(f"{OLLAMA_URL}/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": stream
            },
                                                       timeout=15)
    response.raise_for_status()
    return response.json()["message"]["content"]

async def generate_query_response(request: GenerateAnswerRequest):
    system_prompt = (
    "You are an AI assistant integrated into a search engine. "
    "Your role is to provide clear, concise, and standalone answers to user queries using your general knowledge.\n\n"
    "- Respond with a direct answer whenever possible.\n"
    "- Avoid asking the user for more input.\n"
    "- If the question is ambiguous, briefly mention possible interpretations and give a general answer if feasible.\n"
    "- If you cannot answer with reasonable certainty, say so clearly.\n\n"
    "Do not include greetings, sign-offs, or follow-up questions. Keep your answer informative and to the point.\n\n"
    "At the end of your response, include a confidence score from 0 to 1 in the format: Confidence: [score]"
)
    response_text = await generate_model_response(request.query, False, system_prompt)
    return GenerateAnswerResponse(response=response_text)

async def analyze_results(query: str, results: list):
    text_blob = "\n".join([r["title"] + "\n" + r.get("content", "") for r in results])
    prompt = f"Analyze these search results for '{query}':\n{text_blob}"
    response = await generate_model_response(prompt)
    return response

async def extract_article_text(url: str) -> str:
    try:
        response = await httpx.AsyncClient().get(url, timeout=10, follow_redirects=False)
        # redirects get messy on certain websites, might need special procedures to handle them
        response.raise_for_status()

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
        return AnalysisResponse(analysis=response)
    else:
        return AnalysisResponse(analysis="Analysis unavailable for this article")

async def rewrite_query(request: RewriteRequest):
    query = request.query
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
    return RewriteResponse(rewritten_query=response)

def format_search_results(results: list[SearchResult]) -> str:
    formatted = []
    for i, result in enumerate(results, start=1):
        formatted.append(
                f"{i}. Title: \"{result.title}\"\n   Snippet: \"{result.content}\" URL: \"{result.url}\""
        )
    return "\n\n".join(formatted)

def sort_ranked_results(ranking: RankingResponse) -> RankingResponse:
    print(f"received results to sort:", ranking)
    sorted_items = sorted(
        ranking.root,
        key=lambda item: (-item.score, item.title.lower())  # Descending score, then alphabetical
    )
    return RankingResponse(sorted_items)

from typing import List, Any

def batch_list(data: List[Any], batch_size: int) -> List[List[Any]]:
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]


async def rank_results(request: RankingRequest):
    system_prompt = """
You are an intelligent search assistant.

Your task is to evaluate the relevance of search results to a given user query.

Each result contains:
- a title
- a snippet
- a URL

Instructions:
- Assign each result a score from 0 to 10 based on how relevant it is to the query.
  - 10 = The result directly and thoroughly answers the query.
  - 0 = The result is completely unrelated.
- Evaluate the results in the order they are provided.
- Return ONLY a JSON array of integers. Each integer represents the score for the corresponding result, by index.

Format:
[score1, score2, score3, ...]

Rules:
- Do NOT explain your reasoning.
- Do NOT include any additional text or formatting.
- Do NOT include object fields like "title" or "url".
- The number of scores MUST match the number of search results.
- Do NOT omit or merge any results — one score per result, in order.

Example:

Query: "economic impact of tariffs in 2025"

[
  9,
  2,
  6,
  0
]

Now evaluate the following results using the same format:
"""

    #formatted_results = format_search_results(request.search_results)
    response = []
    query = request.query
    idx = 0
    for batch in batch_list(request.search_results, 7):
        # if batch size is too large, gemma begins to ignore original prompt
        formatted_results = format_search_results(batch)
        try: 
            user_prompt = (f"Query: {query} \n"
                           f"Article data: {formatted_results}\n"
                            )
            model_response = await generate_model_response(user_prompt, False, system_prompt)
            print("model response: ", model_response)
            #match = re.search(r'\[\s*{.*}\s*\]', model_response, re.DOTALL)
            match = re.search(r'\[\s*(?:\d+\s*,\s*)*\d+\s*\]', model_response)
            if match:
                clean_json_str = match.group(0)
                parsed = json.loads(clean_json_str)
                for score in parsed:
                    old_result = request.search_results[idx]
                    scored_response = ScoredSearchResult(
                            title=old_result.title,
                            content=old_result.content,
                            url=old_result.url,
                            score=score
                            )
                    response.append(scored_response)
            else:
                print("Could not extract valid JSON array.")
        except Exception as e:
            print("failed to convert to json", e)
    #print("current state of the response looks like this:", response)
    try:
        #json_data = json.loads(response)
        print("loaded json data: ", response)
        adapter = TypeAdapter(RankingResponse)
        
        # sort in score order; break ties alphabetically
        ranked_results: RankingResponse = adapter.validate_python(response)
        return sort_ranked_results(ranked_results)
    except:
        #print("unable to parse result rankings from llm response")
        #return sort_ranked_results(response)
        print("problematic response:", response)
        return None

