## V1.4.8 - Deterministic Grounding Guard

- Added source-only post-generation grounding guard.
- Unsupported/current/external intents are forced to the canonical refusal.
- Unnecessary LLM refusals and prompt echoes are replaced only with sentences that already exist in retrieved evidence.
- Turkish uppercase normalization made Unicode-safe.
- Multi-step moving-average + risk questions receive evidence from both relevant source rules.
- Recorded V1.4.7 100-case Ollama replay regression: 100/100 PASS.
- Full unit test suite: 74 PASS.

## V1.4.7 - Answerability / Evidence Selection Fix

- Ollama 3B modelinin doğrudan kanıt varken aşırı ret vermesine neden olan prompt sözleşmesi düzeltildi.
- Herhangi bir kaynak doğrudan cevap içeriyorsa ilgisiz diğer kaynaklar ret nedeni sayılmıyor.
- Paraphrase, Türkçe çekim ve açık olumsuz ifadeler kanıt olarak kabul ediliyor.
- İki scope sorusunun beklenen kaynak sözleşmesi project_scope_notes.md ile güncellendi.
- Retrieval, refusal ve hallucination güvenlik kuralları korunuyor.

## v1.4.6 - Evaluation contract and scope guard hardening

- Analysed the real 100-question Ollama evidence bundle from v1.4.5 instead of tuning against synthetic scores.
- Replaced brittle exact-phrase grading with contract-aware refusal grading and lightweight Turkish inflection tolerance.
- Forbidden hallucination terms now use word/phrase boundaries; substrings such as `al` inside `alım` no longer create false failures.
- A safe refusal may mention the queried term (for example `RSI bilgisi bulunamadı`) without being misclassified as hallucination.
- Prompt contract now requires one canonical refusal sentence when the sources do not directly support the answer and forbids echoing the source blocks.
- Verbose model refusals are normalized to the canonical refusal contract before UI/evaluation.
- Added `project_scope_notes.md` to make project boundaries explicit and retrievable: no live market data, investment advice, broker execution, unsupported indicators/metrics, or unrelated general-purpose tasks.
- Corrected a benchmark boundary case (`ood_010`): a grounded negative answer about real order code is a valid project-capability answer, not an OOD failure.
- Evaluation output is isolated under `output/live_evaluation_ollama_v146`; old checkpoints are not reused.
- Reproducible evaluation now indexes 4 documents including the project-scope note and defaults to top-k=5.
- 66 automated tests pass; source and script compilation also pass.
- Metrics remain evidence-based; no pass-rate value is hard-coded.

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


## v1.4.2 - Final source evidence compatibility fix
- Added a read-only `RetrievedChunk.chunk_index` alias for backward compatibility.
- Made Streamlit source rendering tolerant of both `chunk_id` and `chunk_index`.
- Hardened live evidence export against schema variations.
- Added a regression test for source evidence rendering compatibility.
# Değişiklik Günlüğü

## 1.0.0
- Exception ve logging katmanı
- Belge/soru doğrulama ve SHA-256
- Provider factory
- Runtime snapshot
- 55+ evaluation sorusu
- Final smoke check ve final belgeleri

## v1.2.0 - Portfolio Evidence Final

- Streamlit arayüzüne belge yükleme ve indeksleme eklendi.
- Canlı soru-cevap ekranına retrieval distance ve latency kontrolleri eklendi.
- 100 soruluk evaluation arayüzden çalıştırılabilir hale getirildi.
- Yazdırılabilir HTML değerlendirme raporu eklendi.
- JSON, CSV, failed-case CSV ve soru bazlı kanıt çıktıları korundu.
- Dockerfile ve GitHub Actions test workflow eklendi.
- Test sayısı 50'ye çıkarıldı; tüm testler geçti.

## v1.3.0
- 100 soruluk tekrarlanabilir çevrimdışı kanıt çalıştırması eklendi.
- JSON, CSV, başarısız vaka, HTML ve soru başına JSON kanıtları üretildi.
- `RetrievedChunk.chunk_id` / `chunk_index` uyumsuzluğu düzeltildi.
- Çevrimdışı baseline sonucu: 73/100; retrieval %84; refusal %91; hallucination guard %99.

## v1.4.0
- Tek Streamlit arayüzünde Demo, Groq ve Ollama modları eklendi.
- Demo modu API anahtarı/Ollama/vektör indeks olmadan paketlenmiş örnekleri gösterir.
- Demo ve çevrimdışı sonuçların canlı LLM sonucu olmadığı arayüz ve dokümanlarda açıkça etiketlendi.
- Groq ve Ollama değerlendirme çıktıları ayrı klasörlere yönlendirildi.
- Üç modlu teslim ve inceleme dokümanı eklendi.
