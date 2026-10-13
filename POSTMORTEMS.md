# Postmortems

## Incident 1: Model Deprecation (404)
**Date**: 13th october 2026.
**Symptom**: API calls returned `groq.NotFoundError: model llama-3.3-70b-versatile does not exist`.
**Root cause**: Groq retired the `llama-3.3-70b-versatile` model on Aug 16, 2026.
**Fix**: Migrated to `openai/gpt-oss-120b`, Groq's recommended replacement.
**Outcome**: API calls succeeded. Learned to check provider deprecation notices before pinning model versions.

## Incident 2: Token Limit Exceeded (413)
**Date**: 14th october 2026.
**Symptom**: `groq.APIStatusError: 413 - Request too large... Limit 8000 TPM, Requested 57748`.
**Root cause**: Chunking strategy produced chunks too large (500 tokens each) and retrieval sent 5 chunks per query, producing a ~57K token prompt.
**Fix**: 
1. Reduced chunk size from ~2000 chars to 400 chars with hard-split fallback.
2. Reduced top_k from 5 to 3.
3. Added a 3000-character context cap in the prompt builder.
**Outcome**: Prompt size dropped to ~450 tokens per query, well under the 8K TPM free-tier limit.

