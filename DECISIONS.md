# Teknik Kararlar

## 1. Desteklenen İlk Dosya Türleri

İlk çalışan sürüm `.txt` ve `.md` dosyalarını destekler. PDF/Word desteği sonraki aşamaya bırakılmıştır; çünkü metin çıkarma ve taranmış belge OCR süreçleri ayrı doğrulama gerektirir.

## 2. Yerel Retrieval

Çok dilli Sentence Transformers embedding modeli ve yerel ChromaDB kullanılır. Böylece belge vektörleri proje bilgisayarında tutulur.

## 3. Çoklu Belge Kimliği

Her belge, indekslendiği klasöre göre göreli `source_key` alır. Bu anahtar metadata içinde saklanır; aynı dosya adı farklı alt klasörlerde olsa bile çakışma riski azaltılır.

## 4. Re-index Koruması

Aynı kaynak yeniden indekslenmeden önce eski parçaları silinir. Bu karar, değişen belgelerden kalabilecek eski parçaların yanlış retrieval üretmesini önlemek içindir.

## 5. Retrieval Eşiği

Eşik üstündeki uzak sonuçlar LLM'e gönderilmez. Amaç, en yakın sonuç her zaman ilgiliymiş gibi davranılmasını engellemektir. Eşik proje veri seti büyüdükçe test edilerek ayarlanacaktır.

## 6. Kaynak Dayanaklı Cevap

LLM'e yalnızca retrieval tarafından dönen parçalar gönderilir. Prompt kaynak dışı bilgi eklemeyi yasaklar; yeterli bağlam yoksa LLM çağrılmaz.

## 7. Kapsam Dışı

Canlı işlem, broker bağlantısı, otomatik emir, kişiye özel yatırım tavsiyesi ve kârlılık vaadi bu projenin kapsamı dışındadır.
