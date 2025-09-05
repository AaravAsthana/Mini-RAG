# llm.py
from google import genai
client = genai.Client()

def generate_answer(query: str, context: str) -> str:
    prompt = (
        "You are an assistant that answers the user's question using ONLY the provided context.\n"
        "If the answer is not contained in the context, reply: \"I don't know.\".\n\n"
        f"Context:\n{context}\n\nQuestion:\n{query}\n\n"
        "Answer concisely with inline citations like [1], [2]."
    )

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return resp.text
