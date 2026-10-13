# Why I combined dense vector search with BM25.

# ADR 002: Hybrid Retrieval (Dense + BM25)

## Status
Accepted

## Context
Pure vector search misses exact keyword matches (e.g., acronyms, numbers, proper nouns). This hurt retrieval quality for factual queries.

## Decision
Combine ChromaDB dense retrieval with BM25 keyword retrieval, then merge and deduplicate results.

## Consequences
**Positive**: Improved relevant-chunk rate on my test set (documented in POSTMORTEMS.md).
**Negative**: Adds a second dependency (rank_bm25) and slightly higher retrieval latency.