# server/reranker.py
from server.llm import generate_answer

def rerank_query(query: str, documents: list[dict]) -> list[dict]:
    """
    Simple reranker: placeholder function that could call an LLM for scoring.
    For now, just returns documents as-is.
    """
    # Example: you could later score documents using generate_answer if desired
    return documents
