# main.py
import logging
from typing import Optional
from fastapi import FastAPI, UploadFile, Form, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from server.chunking import chunk_text
from server.embeddings import embed_text
from server.llm import generate_answer
from server.db import upsert_document, query_documents
from server.reranker import rerank_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mini_rag")

app = FastAPI(title="Mini RAG")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
def health():
    return {"status": "ok"}

def _decode_bytes_to_text(b: bytes) -> str:
    if not b:
        return ""
    if b.startswith(b"\xef\xbb\xbf"):
        try: return b.decode("utf-8-sig")
        except Exception: pass
    try: return b.decode("utf-8")
    except UnicodeDecodeError:
        try: return b.decode("utf-16")
        except UnicodeDecodeError:
            try: return b.decode("latin-1")
            except Exception: return b.decode("utf-8", errors="replace")

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        raw = await file.read()
        text = _decode_bytes_to_text(raw)
        if not text.strip():
            msg = "Uploaded file could not be decoded or is empty."
            logger.warning(msg)
            return JSONResponse({"error": msg}, status_code=400)

        chunks = chunk_text(text)
        inserted = 0
        for idx, chunk in enumerate(chunks):
            try:
                emb = embed_text(chunk)
                metadata = {"source": file.filename, "chunk_index": idx}
                upsert_document(chunk, emb, metadata)
                inserted += 1
            except Exception as e:
                logger.exception("Failed to embed/upsert chunk: %s", e)

        return {"message": f"Inserted {inserted} chunks from {file.filename}"}
    except Exception as e:
        logger.exception("Unhandled error in /upload: %s", e)
        return JSONResponse({"error": "Internal server error during upload."}, status_code=500)

@app.post("/query")
async def query(request: Request):
    try:
        form = await request.form()
        q = form.get("q") if form else None
        text_doc = form.get("text") if form else None  # New: optional text
    except Exception:
        q, text_doc = None, None

    if not q:
        try:
            body = await request.json()
            q = body.get("q")
            text_doc = body.get("text")  # JSON alternative
        except Exception:
            q, text_doc = None, None

    if not q:
        return JSONResponse(
            {"error": "Missing query parameter 'q'"},
            status_code=400
        )

    try:
        # If the user provided text, treat it as the document
        if text_doc:
            docs = [{"content": text_doc}]
        else:
            # Otherwise, fetch from Supabase using embeddings
            q_emb = embed_text(q)
            docs = query_documents(q_emb)

        if not docs:
            return {"answer": "I could not find relevant information.", "sources": []}

        docs = rerank_query(q, docs)
        top_docs = docs[:3]
        context = "\n\n".join(d.get("content", "") for d in top_docs)
        answer = generate_answer(q, context)

        return {"answer": answer, "sources": top_docs}

    except Exception as e:
        logger.exception("Unhandled error in /query: %s", e)
        return JSONResponse(
            {"error": "Internal server error during query."},
            status_code=500
        )
