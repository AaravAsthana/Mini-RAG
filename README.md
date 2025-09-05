# Mini RAG

A minimal Retrieval-Augmented Generation (RAG) system using:

- **FastAPI** backend
- **Supabase** (Postgres + pgvector) for vector DB
- **Google Generative AI** (Gemini API) for embeddings + LLM
- **React (Vite)** frontend

## Features
- Upload documents → chunk + embed → store in Supabase
- Query with natural language → retrieve top chunks → rerank → answer

## Setup
1. Copy `.env.example` → `.env` and fill secrets.
2. Backend:
   ```sh
   cd server
   poetry install
   poetry run uvicorn server.main:app --reload
