# Kaynak Dayanaklı Cevap Üretimi

Bu aşamada proje, semantic retrieval sonucunda bulunan belge parçalarını bir LLM'e bağlar.

## Akış

```text
kullanıcı sorusu
→ Sentence Transformers ile query embedding
→ ChromaDB semantic retrieval
→ bulunan parçalar ve kaynak etiketleri
→ kısıtlı LLM promptu
→ Türkçe cevap
→ kullanılan kaynak parçalarının listesi
```

## Güvenlik ve Kapsam

LLM'e şu kurallar verilir:

- yalnızca sağlanan parçaları kullanmak,
- kaynakta bulunmayan bilgiyi uydurmamak,
- yeterli bilgi yoksa bunu açıkça söylemek,
- yatırım tavsiyesi, emir veya kesin kâr iddiası vermemek.

## Kaynak Gösterme Sınırı

İlk sürüm, LLM cevabının altında retrieval sırasında kullanılan bütün kaynak parçalarını listeler.
Bu, her cümle için ayrı kanıt eşlemesi değildir. Cümle-bazlı atıf ve kalite ölçümü sonraki RAGAS aşamasında geliştirilecektir.

## Yerel Kurulum

Gerçek API anahtarı yalnızca `calisma/.env` dosyasında tutulur:

```text
GROQ_API_KEY=...
GROQ_MODEL=llama-3.3-70b-versatile
```

`.env` dosyası GitHub'a yüklenmez. Sadece `.env.example` repoda bulunur.

## Çalıştırma Sırası

```bash
python -m pip install -e .[dev]
python scripts/index_sample.py
python scripts/ask_sample.py "Günlük maksimum kayıp sınırı nedir?"
pytest
```
