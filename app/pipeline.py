from app.retrieve import retrieve
from app.generate import generate_answer


def ask(query: str, top_k: int = 5) -> dict:
    """Full RAG pipeline: retrieve relevant chunks, then generate a cited answer."""
    chunks = retrieve(query, top_k=top_k)
    result = generate_answer(query, chunks)
    result["retrieved_chunks"] = chunks
    return result