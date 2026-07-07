# Çoklu Belge İndeksleme ve Retrieval Kalite Kontrolü

## Neden Bu Aşama Eklendi?

Tek örnek metin üzerinde çalışan bir sistem, RAG akışını göstermek için yeterlidir; ancak gerçek kullanımda birden fazla belge bulunur. Bu sürümde sistem, bir klasördeki desteklenen TXT ve Markdown dosyalarını toplu biçimde keşfeder, her belgeye ayrı bir kaynak anahtarı verir ve hepsini aynı yerel Chroma koleksiyonuna indeksler.

## Yeni Akış

```text
kaynak klasörü
→ TXT / MD belge keşfi
→ belge bazlı temizleme ve parçalara ayırma
→ embedding
→ ChromaDB'ye kaynak metadata'sı ile kayıt
→ semantic retrieval
→ mesafe eşiği ile ilgisiz sonuçları eleme
→ LLM ile kaynak dayanaklı cevap
```

## Re-index Davranışı

Bir belge yeniden indekslenmeden önce aynı `source_key` ile ilişkili eski parçalar silinir. Böylece belge kısaldığında geçmişten kalan eski parçaların retrieval sonucuna karışması önlenir.

## Retrieval Eşiği

Chroma'nın cosine distance sonucu küçüldükçe parça sorguya daha yakındır. Bu sürümde başlangıç için `RETRIEVAL_MAX_DISTANCE=0.85` kullanılır. Bu değer kesin doğruluk ölçüsü değildir; farklı belge setleri için test edilerek ayarlanmalıdır.

Eşik nedeniyle yeterince yakın kaynak bulunamazsa LLM çağrısı yapılmaz; sistem "yeterli ve ilgili bilgi bulunamadı" durumuna geçer.

## Yerel Kalite Kontrolü

`data/evaluation/retrieval_testset.json` dosyasında insan tarafından yazılmış soru-kaynak çiftleri bulunur. `scripts/evaluate_retrieval.py` bu sorularda beklenen kaynak dosyasının ilk üç sonuç içinde yer alıp almadığını ölçer.

Üretilen metrik:

```text
source_hit_rate@3 = beklenen kaynağın ilk 3 sonuçta bulunma oranı
```

Bu metrik yalnızca retrieval katmanını ölçer. LLM cevabının kaynaklara sadakati, sonraki aşamada RAGAS gibi bir değerlendirme katmanıyla ölçülecektir.
