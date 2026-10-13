# Why I chose paragraph-aware chunking over fixed-size:

# ADR 001: Paragraph-Aware Chunking with Overlap

## Status
Accepted

## Context
Documents needed to be split into chunks before embedding. Fixed-size chunking is simple but breaks sentences and loses context, which reduces retrieval quality.

## Decision
Chunk by paragraph boundaries, using a 400-character target size with a 50-character overlap. For oversized paragraphs, apply a hard split.

## Consequences
**Positive**: Retrieved chunks preserve semantic meaning and read naturally when passed to the LLM.
**Negative**: Slightly more complex ingestion code and more chunks stored (1,147 for 5 PDFs).