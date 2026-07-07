# Çalıştırma ve Demo Akışı

## 1. Bağımlılıkları Kur

```bash
python -m pip install -e .[dev]
```

## 2. Örnek Belgeleri Toplu İndeksle

```bash
python scripts/index_documents.py data/sample --reset
```

Bu işlem üç sentetik örnek belgeyi yerel ChromaDB koleksiyonuna ekler.

## 3. Retrieval Sonucunu LLM Kullanmadan İncele

```bash
python scripts/search_sample.py
```

Bu komut örnek soru için bulunan belge parçalarını ve kaynak etiketlerini gösterir.

## 4. Kaynak Dayanaklı Soru Sor

Önce `.env.example` dosyasını `.env` olarak kopyalayın ve Groq anahtarını ekleyin.

```bash
python scripts/ask_documents.py "Kırılma sonrası hangi doğrulama beklenir?"
```

Tek bir belge üzerinde arama yapmak için:

```bash
python scripts/ask_documents.py "Günlük maksimum kayıp sınırı nedir?" --source risk_management_notes.md
```

## 5. Retrieval Kalitesini Ölç

```bash
python scripts/evaluate_retrieval.py
```

Komut çıktısı `output/retrieval_evaluation.json` dosyasına yazılır. Bu dosya GitHub'a yüklenmez.

## 6. Testleri Çalıştır

```bash
pytest
```

## Not

İlk embedding model indirmesinde internet gerekir. İndeks verisi `data/chroma/` altında yerel olarak oluşur ve `.gitignore` ile repodan hariç tutulur.
