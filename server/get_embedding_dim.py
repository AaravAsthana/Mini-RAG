# get_embedding_dim.py
"""
Run this to print the embedding vector dimension returned by the Gemini embed API.
Save in mini_rag\server and run with: poetry run python get_embedding_dim.py
"""

from google import genai

def main():
    client = genai.Client()
    # model used previously in this project
    model = "gemini-embedding-001"
    print("Calling model:", model)
    resp = client.models.embed_content(model=model, contents="hello")
    vec = None

    # Try several common response shapes
    if hasattr(resp, "embeddings"):
        # SDK object with embeddings attribute
        emb = resp.embeddings
        if emb and len(emb) > 0:
            # common property name used previously was .vector
            if hasattr(emb[0], "vector"):
                vec = emb[0].vector
            elif hasattr(emb[0], "values"):
                vec = emb[0].values
            elif isinstance(emb[0], (list, tuple)):
                vec = list(emb[0])
    elif isinstance(resp, dict) and "embeddings" in resp:
        e0 = resp["embeddings"][0]
        vec = e0.get("values") or e0.get("embedding") or e0
    elif isinstance(resp, (list, tuple)) and len(resp) > 0:
        first = resp[0]
        if isinstance(first, (list, tuple)):
            vec = list(first)
        elif isinstance(first, dict):
            vec = first.get("values") or first.get("embedding")

    if vec is None:
        print("Could not parse embedding response shape. Raw response:")
        print(resp)
        raise SystemExit(1)

    print("dim:", len(vec))

if __name__ == "__main__":
    main()
