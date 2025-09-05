# db.py
import logging
from supabase import create_client
from server.config import SUPABASE_URL, SUPABASE_KEY, TOP_K

logger = logging.getLogger("mini_rag.db")
logger.setLevel(logging.INFO)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
VECTOR_TABLE = "documents_vector"

def upsert_document(content: str, embedding: list[float], metadata: dict):
    try:
        row = {"content": content, "embedding": embedding, "metadata": metadata}
        res = supabase.table(VECTOR_TABLE).upsert(row).execute()
        logger.info("Upsert response: %s", getattr(res, "data", res))
        return res
    except Exception as e:
        logger.exception("Failed to upsert document: %s", e)
        raise

def query_documents(embedding: list[float], top_k: int = TOP_K):
    try:
        # Ensure 3072-dim embedding
        if len(embedding) < 3072:
            embedding += [0.0] * (3072 - len(embedding))
        elif len(embedding) > 3072:
            embedding = embedding[:3072]

        payload = {"query_embedding": embedding, "match_count": top_k}
        res = supabase.rpc("query_knn", payload).execute()
        data = getattr(res, "data", res)
        logger.info("RPC returned %d rows", len(data) if data else 0)
        return data or []
    except Exception as e:
        logger.exception("RPC query_knn failed: %s", e)
        raise
