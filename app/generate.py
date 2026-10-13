import os
from groq import Groq

_client = None

SYSTEM_PROMPT = """You are a helpful assistant that answers questions strictly based on the provided context.

Rules:
- Only use information from the context below.
- Cite sources using [1], [2], etc. matching the numbered context items.
- If the answer is not in the context, say: "I don't have enough information to answer that."
- Be concise and direct. Do not make up information."""


def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")
        _client = Groq(api_key=api_key)
    return _client

def generate_answer(query: str, context_chunks: list[dict]) -> dict:
    # Cap total context to ~3000 characters (~750 tokens)
    MAX_CONTEXT_CHARS = 3000
    trimmed = []
    total = 0
    for c in context_chunks:
        text = c["text"][:1000]  # cap each chunk at 1000 chars
        if total + len(text) > MAX_CONTEXT_CHARS:
            break
        trimmed.append({**c, "text": text})
        total += len(text)
    
    context = "\n\n".join([f"[{i+1}] {c['text']}" for i, c in enumerate(trimmed)])
    prompt = f"""Answer the question using ONLY the context below. Cite sources as [1], [2], etc.
If the answer isn't in the context, say "I don't have enough information."

Context:
{context}

Question: {query}
Answer:"""
    
    response = _get_client().chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=500,
    )
    return {
        "answer": response.choices[0].message.content,
        "sources": [{"id": i+1, "source": c["source"], "text": c["text"][:200]} for i, c in enumerate(trimmed)]
    }