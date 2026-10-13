from rank_bm25 import BM25Okapi
from app.ingest import collection, model


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """Hybrid retrieval: dense (vector) + sparse (BM25), merged and deduplicated."""
    if collection.count() == 0:
        return []

    # --- Dense retrieval (semantic similarity) ---
    query_embedding = model.encode(query).tolist()
    dense_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k * 2, collection.count()),
    )

    # --- Sparse retrieval (BM25 keyword match) ---
    all_docs = collection.get()
    tokenized_corpus = [doc.lower().split() for doc in all_docs["documents"]]
    bm25 = BM25Okapi(tokenized_corpus)
    bm25_scores = bm25.get_scores(query.lower().split())

    bm25_ranked = sorted(
        zip(all_docs["ids"], bm25_scores, all_docs["documents"], all_docs["metadatas"]),
        key=lambda x: x[1],
        reverse=True,
    )[: top_k]

    # --- Merge results (dense first, BM25 adds anything missed) ---
    combined = {}
    for i, doc_id in enumerate(dense_results["ids"][0]):
        combined[doc_id] = {
            "id": doc_id,
            "text": dense_results["documents"][0][i],
            "source": dense_results["metadatas"][0][i]["source"],
            "score": 1.0 / (i + 1),
            "method": "dense",
        }

    for rank, (doc_id, score, text, meta) in enumerate(bm25_ranked):
        if doc_id not in combined and score > 0:
            combined[doc_id] = {
                "id": doc_id,
                "text": text,
                "source": meta["source"],
                "score": 1.0 / (rank + 1),
                "method": "bm25",
            }

    return sorted(combined.values(), key=lambda x: x["score"], reverse=True)[:top_k]