# embeddings.py
import logging
from typing import List, Any
from google import genai

logger = logging.getLogger("mini_rag.embeddings")
client = genai.Client()

DEFAULT_EMBED_MODEL = "gemini-embedding-001"

def _extract_vector_from_embedding_obj(obj: Any) -> List[float] | None:
    if obj is None:
        return None
    if hasattr(obj, "values"):
        try:
            return list(obj.values)
        except Exception:
            try:
                return list(obj.values())
            except Exception:
                pass
    if hasattr(obj, "embedding"):
        try:
            return list(obj.embedding)
        except Exception:
            pass
    if isinstance(obj, (list, tuple)):
        try:
            return [float(x) for x in obj]
        except Exception:
            return None
    if isinstance(obj, dict):
        if "values" in obj:
            try:
                return [float(x) for x in obj["values"]]
            except Exception:
                return None
        if "embedding" in obj:
            try:
                return [float(x) for x in obj["embedding"]]
            except Exception:
                return None
    return None

def embed_text(text: str, model: str | None = None) -> List[float]:
    if text is None:
        raise ValueError("text must be provided to embed_text")
    model = model or DEFAULT_EMBED_MODEL
    try:
        resp = client.models.embed_content(model=model, contents=text)
    except Exception as e:
        logger.exception("Failed to call embed_content: %s", e)
        raise RuntimeError(f"Embedding API call failed: {e}") from e

    # Extract embedding
    if hasattr(resp, "embeddings") and resp.embeddings:
        vec = _extract_vector_from_embedding_obj(resp.embeddings[0])
    elif isinstance(resp, dict) and "embeddings" in resp:
        vec = _extract_vector_from_embedding_obj(resp["embeddings"][0])
    elif isinstance(resp, (list, tuple)) and len(resp) > 0:
        vec = _extract_vector_from_embedding_obj(resp[0])
    else:
        vec = None

    if not vec:
        raise RuntimeError("Could not extract embedding vector from response.")

    # Pad or truncate to 3072-dim
    if len(vec) < 3072:
        vec += [0.0] * (3072 - len(vec))
    elif len(vec) > 3072:
        vec = vec[:3072]

    return vec
