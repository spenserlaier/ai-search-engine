# Overview

This is a project demonstrating various integrations and augmentations to search behavior between a locally hosted LLM (via Ollama) and a locally hosted SearXNG instance. By default, AI features are powered by google's Gemma 3 model, as seen here: `https://deepmind.google/models/gemma/gemma-3/`

## Features:

- Intelligent reranking of search results
- Relevance analysis of retrieved search results
- Ai-generated responses to queries
- Ai-optimized queries

## Stack:

- Svelte + typescript frontend
- Python + FastAPI backend
- Ollama (to run LLMs locally)
- SearXNG (to facilitate search result retrieval)

## Getting Started
The project experimentally supports docker, which greatly simplifies deployment and management of program services

### Docker
- Ensure that you have node installed in your local environment
- To run using docker, ensure that you have docker and docker compose installed in your local environment.
- Compile the svelte frontend code by running `npm install` followed by `npm run build` from the `frontend` directory
- Then, run `docker compose up` from the project root
- The frontend will be hosted at `http://localhost:800`

### Manual
If docker does not work as intended, you may need to set the project up manually, which involves installing and running a number of services locally:

#### Set up environment

Rename the default environment files (named `old-env.env`) from within the
backend and frontend directories to `.env` to properly set up environment variables. You may also choose different values
aside from the provided defaults, but this has not been tested.

#### Setting up Ollama

Follow the relevant installation instructions found at "https://github.com/ollama/ollama" to install and run ollama on your system
The default model used is gemma3:4b, so ensure that this model is available in your local installation

#### Setting up SearXNG

Follow the relevant instructions found at "https://docs.searxng.org/admin/installation-searxng.html" to install and run searxng on your system

#### Setting up frontend

Run `npm run dev` from within the project's `frontend` directory

#### Setting up backend

Create and activate a python virtual environment in the backend directory

Install relevant dependencies by running `pip install -r requirements.txt`

Run `uvicorn main:app --host 0.0.0.0 --port 5000`

With all services running, the app frontend should be available locally under the default svelte dev port
