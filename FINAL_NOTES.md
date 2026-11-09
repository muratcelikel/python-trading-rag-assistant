# FINAL STATUS — v1.4.8

- Fresh Ollama live evaluation on submission PC: **100/100 PASS**
- Retrieval: **100%**
- Answer keyword: **100%**
- Refusal: **100%**
- Hallucination guard: **100%**
- Runtime errors: **0**
- Average latency: **9.312 s**
- Unit tests: **74 PASS**
- Final smoke check: **OK**

## V1.4.7 - Answerability / Evidence Selection Fix

- Ollama 3B modelinin doğrudan kanıt varken aşırı ret vermesine neden olan prompt sözleşmesi düzeltildi.
- Herhangi bir kaynak doğrudan cevap içeriyorsa ilgisiz diğer kaynaklar ret nedeni sayılmıyor.
- Paraphrase, Türkçe çekim ve açık olumsuz ifadeler kanıt olarak kabul ediliyor.
- İki scope sorusunun beklenen kaynak sözleşmesi project_scope_notes.md ile güncellendi.
- Retrieval, refusal ve hallucination güvenlik kuralları korunuyor.

## v1.4.5 - Chroma first-run reset fix

- Fixed `chromadb.errors.NotFoundError: Collection [trading_notes_eval] does not exist` on the first 100-question run.
- The dedicated evaluation Chroma directory is now recreated at filesystem level before indexing; the runner no longer attempts to delete a collection that may not exist.
- `ChromaVectorStore.clear()` is also idempotent across Chroma versions that raise either `ValueError` or `NotFoundError`.
- The evaluation output path is now `output/live_evaluation_ollama_v145` so no failed v1.4.4 checkpoint is reused.
- Quality metrics remain evidence-based and are not hard-coded.
- 62 automated tests pass.


## v1.4.4 - Reproducible 100-question evaluation fix

- 100-question live evaluation now builds a dedicated clean Chroma evaluation index automatically from `data/sample`.
- The evaluation no longer depends on whether the Streamlit/UI index was created in another project folder.
- Dedicated evaluation index uses 3 sample documents / 4 chunks and top-k=4 for reproducibility.
- Blank/whitespace boundary questions are safely rejected instead of becoming runtime errors.
- A new output path (`output/live_evaluation_ollama_v144`) avoids reusing stale checkpoints from v1.4.3.
- Quality metrics remain evidence-based; the pass rate is not hard-coded or artificially inflated.
- 60 automated tests pass.

# FINAL NOTES — v1.0

Tamamlananlar: belge desteği, doğrulama, chunking, embedding, ChromaDB, retrieval, kaynaklı cevap, logging/exception yapısı, 55+ evaluation sorusu, OOD/hallucination testleri, final rapor ve smoke check.

Bilinçli kapsam dışı: canlı trading, broker, backtesting, PEAD, vectorbt, Wasserstein, agents, MCP, OCR, web arayüzü.

## 30.09.2026 — Kapanış araştırma deltası (documentation-only)

Final çalışan kod değiştirilmedi. Son trading/RAG kaynak taramasından dört gelecek çalışma başlığı README, final rapor ve `docs/FUTURE_WORK_RESEARCH_DELTA.md` içine işlendi: RAG Debugger failure taxonomy; poison-resistant knowledge base; hybrid retrieval (dense + BM25, ileride Knowledge Graph); context engineering (cap → pin → retrieve → window → summarize, token budget, ablation/validity gates). Canlı trading/broker/emir/yatırım tavsiyesi kapsam dışı kalmaya devam eder.
