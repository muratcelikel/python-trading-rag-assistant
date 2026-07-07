# Python Trading RAG Assistant

Bu proje, Python bitirme ödevi kapsamında geliştirilen kaynak dayanaklı bir trading doküman araştırma sistemidir.

Sistem; TXT/Markdown notlarını okur, temizler, parçalara ayırır, çok dilli embedding ile yerel ChromaDB'ye kaydeder ve kullanıcı sorularında ilgili kaynakları bulur. Yeterince ilgili kaynak bulunduğunda LLM yalnızca bu bağlama dayanarak Türkçe cevap üretir; kullanılan parçalar cevapla birlikte gösterilir.

> Eğitim ve araştırma amaçlıdır. Canlı işlem, broker entegrasyonu, otomatik emir gönderimi ve yatırım tavsiyesi kapsam dışıdır.

## Mevcut Özellikler

- TXT ve Markdown belge okuma
- Metin temizleme ve bindirmeli parçalama
- Çoklu belge klasörü indeksleme
- Yerel Sentence Transformers embedding
- Yerel ChromaDB semantic retrieval
- Kaynak dosyası, parça ve kelime aralığı gösterme
- Mesafe eşiğiyle ilgisiz retrieval sonuçlarını eleme
- Groq ile kaynak dayanaklı cevap üretimi
- İnsan yazımı test setiyle `source_hit_rate@k` retrieval değerlendirmesi
- Birim testleri

## Akış

```text
belge klasörü
→ loader / cleaner / chunker
→ embedding
→ ChromaDB
→ semantic retrieval + eşik
→ kaynak dayanaklı LLM cevabı
→ kaynak listesi
```

## Hızlı Demo

```bash
python -m pip install -e .[dev]
python scripts/index_documents.py data/sample --reset
python scripts/search_sample.py
python scripts/evaluate_retrieval.py
pytest
```

LLM cevabı için `.env.example` dosyasını `.env` olarak kopyalayın ve `GROQ_API_KEY` ekleyin:

```bash
python scripts/ask_documents.py "Günlük maksimum kayıp sınırı nedir?"
```

Ayrıntılar için `docs/06_calistirma_ve_demo.md` dosyasına bakın.
