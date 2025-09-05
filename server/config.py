import os
from dotenv import load_dotenv
load_dotenv()
# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# RAG knobs
TOP_K = int(os.getenv("TOP_K", "5"))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "6000"))

# Chunking settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# Models (keep embedding dims in sync with DB!)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")  # 3072 dims
GENERATION_MODEL = os.getenv("GENERATION_MODEL", "gemini-1.5-flash")

# Safety / prompting
SYSTEM_INSTRUCTIONS = (
    "You are a helpful assistant. Answer using ONLY the provided context. "
    "If the answer is not in the context, say you don't know."
)
