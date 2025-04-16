from typing import Optional
import httpx

_client: Optional[httpx.AsyncClient] = None

def set_client(c: httpx.AsyncClient):
    global _client
    _client = c

def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("HTTP client is not initialized!")
    return _client
