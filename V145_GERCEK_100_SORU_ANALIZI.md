# v1.4.5 Gerçek 100 Soru Sonuç Analizi

Kullanıcının gerçek Ollama koşusundan gelen `output.zip` incelendi.

## Ölçülen sonuç

- Toplam vaka: 100
- Retrieval hit: %100
- Pass rate: %50
- Answer keyword hit: %64
- Refusal success: %63
- Hallucination guard: %72
- Runtime error: 0

## Kök neden

Başarısız 50 vakanın dağılımı: 26 out-of-domain, 19 hallucination-guard, 3 faithfulness, 2 retrieval. Retrieval %100 olduğu için ana sorun belge bulma değildi. Başlıca sorunlar evaluator ve cevap sözleşmesindeydi:

1. Doğru ret cevapları yalnızca birkaç sabit ifadeyle eşleştiriliyordu. `bilgi vermiyor`, `yer almıyor`, `cevap bulamıyorum` gibi güvenli retler FAIL olabiliyordu.
2. Yasak kelime kontrolü substring tabanlıydı. `al` ifadesi `alım` içinde veya `sat` ifadesi `satıcı` içinde geçince yanlış hallucination FAIL üretebiliyordu.
3. Model bazı OOD cevaplarda kaynak bloklarını cevaba tekrar yazıyor, sonra da kaynak dışı açıklama ekliyordu.
4. Türkçe çekim varyantları (`açmaz`/`açmıyor`, `vermez`/`vermiyor`) doğru anlamı taşımasına rağmen keyword FAIL olabiliyordu.
5. `Bu projede gerçek emir gönderme kodu var mı?` vakası benchmarkta OOD/refusal olarak etiketlenmişti; oysa kaynaklardan grounded bir `hayır` cevabı geçerlidir.

## v1.4.6 düzeltmesi

- Contract-aware evaluator v2
- Canonical refusal contract
- Kelime/ifade sınırına duyarlı hallucination denetimi
- Türkçe çekim toleransı
- Proje kapsamı belgesi
- Kaynak bloklarını cevapta tekrar etmeme kuralı
- Benchmark boundary düzeltmesi

Yeni skor ancak gerçek Ollama koşusu yeniden çalıştırıldığında nihai olarak raporlanacaktır; skor yapay biçimde yükseltilmemiştir.
