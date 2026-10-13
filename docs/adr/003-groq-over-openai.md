# Why I chose Groq for free, fast inference.

# ADR 003: Groq for LLM Inference

## Status
Accepted

## Context
The project had a $0 budget. OpenAI's API requires paid credits; local LLMs were too slow on my Mac for interactive demos.

## Decision
Use Groq's free tier with `openai/gpt-oss-120b`.

## Consequences
**Positive**: Free, extremely fast (sub-second latency), no credit card required.
**Negative**: Hard 8,000 TPM limit on the free tier, which required careful prompt budgeting.