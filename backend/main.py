from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import http_client
import httpx
load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client.set_client(httpx.AsyncClient())
    yield  # App runs here
    await http_client.get_client().aclose()

app = FastAPI(lifespan=lifespan)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

