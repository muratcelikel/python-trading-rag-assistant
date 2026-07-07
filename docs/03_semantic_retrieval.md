# Semantic Retrieval ve Kaynak Gösterme

Bu aşamada proje, önceden oluşturulan metin parçalarını anlam tabanlı arama için hazırlar.

## Akış

```text
TXT/MD dosyası
→ loader
→ cleaner
→ chunker
→ Sentence Transformers embedding
→ ChromaDB
→ semantic retrieval
→ kaynak etiketi
```

## Embedding Modeli

İlk sürümde `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` kullanılır. Model Türkçe dahil birden fazla dilde cümle ve paragraf embedding'i üretmek için seçilmiştir.

## Vektör Veritabanı

ChromaDB yerel diskte `data/chroma/` altında çalışır. Bu klasör GitHub'a yüklenmez; aynı bilgisayardaki indeksin saklanması içindir.

## Kaynak Şeffaflığı

Her sonuç şu bilgileri taşır:

- kaynak dosya adı
- parça numarası
- parçada geçen kelime aralığı
- Chroma mesafesi

Bu aşamada sistem henüz LLM ile cevap üretmez. Önce retrieval çıktısının doğru kaynakları bulduğu doğrulanır.
