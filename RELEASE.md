# Release — Python Trading RAG Assistant v1.4.8 FINAL

## Final status

- 74 automated unit tests PASS
- Final smoke check OK
- Recorded live-output replay regression: 100/100 PASS
- Fresh Ollama live evaluation on submission PC: 100/100 PASS
- Retrieval: 100%
- Answer keyword: 100%
- Refusal: 100%
- Hallucination guard: 100%
- Runtime errors: 0
- Average live latency: 9.312 s

## Final capabilities

- TXT / MD / PDF / DOCX ingestion
- Validation, cleaning and chunking
- Embeddings + ChromaDB
- Semantic retrieval
- Groq and Ollama providers
- Clearly labelled Demo Mode
- Source/citation evidence
- Answerability contract and grounding guard
- Contract-aware evaluation
- 100-question live evidence runner with retry/checkpoint/resume
- JSON, CSV, Markdown, HTML and per-question evidence outputs
- Streamlit UI
- Windows setup/start scripts
- Dockerfile and automated tests

## Scope exclusions

Live trading, broker integration, order execution, investment advice and backtesting are intentionally out of scope.

## Documentation-only research delta — 30.09.2026

Final kod kapsamı değiştirilmeden README ve `docs/FUTURE_WORK_RESEARCH_DELTA.md` içine dört gelecek çalışma hattı eklendi: RAG Debugger failure taxonomy, poison-resistant knowledge base, hybrid retrieval (dense + BM25; ileride Knowledge Graph) ve context engineering/token-budget ablation. Bu ekleme final canlı sonuçlarını veya proje kapsamını değiştirmez.
