# Python Trading RAG Assistant v1.4.8 — Final Teslim

Kaynak dayanaklı doküman soru-cevap sistemi geliştirmek için hazırlanmış Python tabanlı RAG (Retrieval-Augmented Generation) portföy projesidir. Trading, yalnızca örnek bilgi alanıdır; canlı işlem, broker entegrasyonu ve yatırım tavsiyesi kapsam dışıdır.

## Final Durum

Proje uçtan uca çalışır durumdadır:

`Validation → Loader → Cleaner → Chunker → Embedding → ChromaDB → Retrieval → Prompt → LLM → Citation → Evaluation`

11 Ağustos 2026 tarihinde Windows 11 üzerinde `llama3.2:3b` modeliyle yapılan taze Ollama canlı değerlendirmesinde:

- Total cases: **100**
- Passed cases: **100**
- Pass rate: **100.00%**
- Retrieval hit rate: **100.00%**
- Answer keyword hit rate: **100.00%**
- Refusal success rate: **100.00%**
- Hallucination guard rate: **100.00%**
- Runtime errors: **0**
- Average latency: **9.312 seconds**
- Evaluator: **contract-aware v2**

Bu sonuçlar kullanıcının teslim bilgisayarında gerçek Ollama çalıştırmasıyla elde edilmiştir. Ham kanıt dosyaları `output/live_evaluation_ollama_v147/` altında üretilir.

## Özellikler

- TXT / Markdown / PDF / DOCX belge desteği
- Belge doğrulama ve metin temizleme
- Chunking ve metadata yönetimi
- Sentence-transformers embedding
- ChromaDB vector database
- Semantic retrieval
- Kaynak dayanaklı LLM cevabı
- Groq ve Ollama sağlayıcıları
- Kurulumsuz ve açıkça etiketlenmiş Demo Mode
- Kaynak dosyası, chunk bilgisi, cosine distance ve latency gösterimi
- Hallucination guard
- Out-of-domain / güvenli ret mantığı
- 100 soruluk canlı evaluation
- Checkpoint, retry, backoff ve kaldığı yerden devam desteği
- JSON / CSV / Markdown / HTML kanıt çıktıları
- Streamlit arayüzü
- Dockerfile ve test paketi
- Windows kurulum ve başlatma scriptleri

## Tek Arayüz, Üç Çalışma Modu

| Mod | Gereksinim | Kullanım |
|---|---|---|
| Demo (kurulumsuz) | Ek gereksinim yok | Paketlenmiş örnek cevapları ve raporları inceler |
| Groq (bulut) | İnternet + `GROQ_API_KEY` | Hızlı canlı soru-cevap |
| Ollama (yerel) | Ollama + yerel model | API anahtarsız, tamamen yerel canlı çalışma |

Demo modu hiçbir zaman canlı LLM sonucu gibi sunulmaz.

## Windows Kurulum

PowerShell'i proje klasöründe açın:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\KURULUM_WINDOWS.ps1
```

Arayüzü açmak için:

```powershell
.\BASLAT_WINDOWS.bat
```

Alternatif:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Ollama ile Çalışma

Önerilen model:

```powershell
ollama pull llama3.2:3b
```

`.env` örneği:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

Arayüzde **Ollama (yerel)** seçilerek gerçek LLM çağrısı yapılır.

## 100 Soruluk Canlı Kanıt

Windows'ta:

```powershell
.\CALISTIR_100_SORU_OLLAMA.bat
```

Alternatif komut:

```powershell
.\.venv\Scripts\python.exe scripts\run_live_evaluation.py --provider ollama
```

Değerlendirme hattı:

`Question → Retrieval → Context → Ollama → Grounded Answer → Citation → Contract-aware Evaluation → Evidence Export`

Canlı koşu çıktıları aşağıdaki klasörde oluşturulur:

```text
output/live_evaluation_ollama_v147/
├── live_results.json
├── live_results.csv
├── failed_questions.csv
├── evaluation_summary.md
├── evaluation_report.html
└── evidence/
```

## Değerlendirme Kapsamı

100 soruluk benchmark şu alanları kapsar:

- Retrieval doğruluğu
- Kaynakla tutarlı cevap üretimi
- Paraphrase / farklı ifade biçimleri
- Out-of-domain reddetme
- Hallucination guard
- Yanlış veya çelişkili öncüller
- Kısa ve belirsiz sorgular
- Çok adımlı sorular

Evaluator, `contract-aware v2` yaklaşımını kullanır. Güvenli ret paraphrase'lerini tanır ve hallucination kontrolünü kelime/ifade sınırları üzerinden yapar.

## Testler

V1.4.8 geliştirme paketinde:

```text
74 unit test PASS
Final smoke check: OK
Recorded live-output regression replay: 100/100 PASS
Fresh Ollama live run on submission PC: 100/100 PASS
```

## Proje Kapsamı

Bu proje şunları yapar:

- Belge tabanlı bilgi alımı
- Semantic retrieval
- Yerel/bulut LLM ile kaynaklı cevap
- Citation ve evaluation
- Canlı kalite kanıtı üretimi

Bilinçli olarak kapsam dışı bırakılanlar:

- Canlı trading
- Broker bağlantısı
- Otomatik emir gönderimi
- Yatırım tavsiyesi
- Backtesting motoru
- Prop-firm entegrasyonu

## Proje Yapısı

```text
src/trading_rag_assistant/
    validation.py
    document_loader.py
    cleaner.py
    chunker.py
    embeddings.py
    vector_store.py
    retriever.py
    prompting.py
    query_engine.py
    providers.py
    grounding_guard.py
    live_evaluation.py
    ...

data/
    sample/
    eval/

scripts/
    run_live_evaluation.py
    run_offline_evaluation.py
    index_documents.py
    final_smoke_check.py
    ...

tests/
docs/
app.py
```

## Teslim Dokümanları

- `FINAL_RAPOR.docx` — proje amacı, mimari, değerlendirme ve final sonuçları
- `FINAL_CANLI_TEST_SONUCU.md` — 100 soruluk gerçek Ollama final koşusunun kısa özeti
- `FINAL_NOTES.md` — sürüm geliştirme notları
- `docs/` — ayrıntılı teknik dokümantasyon

## Sonuç

Python Trading RAG Assistant v1.4.8; belge ingestion, semantic retrieval, yerel/bulut LLM entegrasyonu, kaynak gösterimi, güvenli ret, hallucination kontrolü ve 100 soruluk canlı değerlendirme zincirini tek projede uçtan uca birleştiren, test edilmiş bir RAG portföy projesidir.

## Future Work — Kapanış Araştırma Deltası (30.09.2026)

Teslim sürümünün çalışan çekirdeği değiştirilmeden, son trading/RAG kaynak taramasından aşağıdaki dört geliştirme hattı gelecek çalışma olarak ayrılmıştır:

1. **RAG Debugger / failure taxonomy** — retrieval sorunlarını yalnızca "başarısız" diye işaretlemek yerine `HEALTHY`, `NOISY_CONTEXT`, `RETRIEVAL_MISS` ve `CORPUS_GAP` sınıflarıyla teşhis etmek. Bu katman, mevcut 100-soruluk evaluation sisteminin hata açıklanabilirliğini artırabilir.
2. **Poison-resistant knowledge base** — belge ingestion sırasında source authority, metadata/tarih ve validity gate kontrolleri; şüpheli veya çelişkili pasajları izole ederek değerlendirme; poisoned-knowledge-base test vakaları. Amaç, semantik olarak çok benzer fakat güvenilmez bir pasajın sırf yüksek retrieval skoru nedeniyle cevabı ele geçirmesini önlemektir.
3. **Hybrid retrieval** — mevcut dense/vector retrieval'ı BM25 gibi lexical retrieval ile birleştirmek; daha ileri aşamada ilişkisel ihtiyaçlar için Knowledge Graph katmanını değerlendirmek. Bu madde mevcut ChromaDB retriever'ının yerine geçmekten çok kontrollü bir karşılaştırma/ensemble çalışması olarak ele alınmalıdır.
4. **Context engineering** — `cap → pin → retrieve → window → summarize` katmanlarıyla token bütçesini yönetmek; ablation ladder ve validity gate'lerle hangi context katmanının gerçekten katkı sağladığını ölçmek. Özellikle uzun konuşma ve çok-belgeli kullanım senaryoları için düşünülmüştür.

Bu maddeler **final teslim kapsamına dahil edilmemiştir**. Canlı trading, broker entegrasyonu, otomatik emir yürütme ve yatırım tavsiyesi yine kapsam dışıdır. Amaç final sürümü şişirmek değil, mevcut RAG çekirdeğinin sonraki araştırma yönlerini açık ve test edilebilir biçimde tanımlamaktır.

Kaynaklar: `Build a RAG Debugger That Shows Why Retrieval Failed in 40 Minutes`, `Build a RAG Pipeline That Survives a Poisoned Knowledge Base in 90 Minutes`, `Build a Context Engineering Layer That Stops Your Agent Breaking at Long Conversations` (kullanıcı tarafından sağlanan kapanış araştırma paketi).
