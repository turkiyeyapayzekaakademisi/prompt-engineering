# Yapılandırılmış Çıktı ve Validasyon — Gemini / Ollama

Bu proje eğitimde **tek müşteri talebi** üzerinden JSON, iç içe ürün listesi, Pydantic doğrulama, API seviyesinde şema zorlaması ve kontrollü yeniden denemeyi öğretir.

## 1. Proje dosyaları

```text
yapilandirilmis_cikti_validasyon/
├── schemas.py                        # Ortak Pydantic modelleri + iş kuralı
├── gemini_yapilandirilmis_cikti.py   # Bulut: Gemini API; içinde tek PROMPT
├── ollama_yapilandirilmis_cikti.py   # Yerel: qwen3:4b; içinde tek PROMPT
└── README.md
```

`prompts.json` bulunmaz. Her `.py` dosyasında tek, aynı içerikli `PROMPT` metni vardır; aynı girdiyi iki farklı modelde karşılaştırabilirsiniz.

## 2. Gereksinimler

- Python 3.10 veya üzeri.
- Gemini için API anahtarı ve internet erişimi.
- Ollama kurulumu ve `qwen3:4b` modeli (yeterli RAM ve depolama alanı).

## 3. Kurulum

Proje klasöründe terminal açın. Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U google-genai ollama "pydantic>=2"
$env:GEMINI_API_KEY="API_ANAHTARINIZ"
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U google-genai ollama "pydantic>=2"
export GEMINI_API_KEY="API_ANAHTARINIZ"
```

Anahtarı Python koduna yazmayın veya Git'e eklemeyin.

Ollama'yı https://ollama.com adresinden kurun. Ardından:

```bash
ollama pull qwen3:4b
ollama list
```

Normalde Ollama yerel API'yi `http://localhost:11434` üzerinden sunar. Çalışmıyorsa Ollama uygulamasını açın veya `ollama serve` ile başlatın.

## 4. Çalıştırma

```bash
python gemini_yapilandirilmis_cikti.py
python ollama_yapilandirilmis_cikti.py
```

Her iki dosyanın üst bölümündeki ayarlar:

```python
CIKTI_YONTEMI = "schema"   # "schema" / "prompt"
MAX_DENEME = 3
```

`schema`: Gemini'de `response_schema`, Ollama'da `format` kullanılır. `prompt`: Modelden yalnızca metinsel talimatla JSON istenir. İki durumda da Pydantic kontrolü yapılır. Şema zorlaması her hata türünü ortadan kaldırmaz.

## 5. Tek örnek ve beklenen alanlar

Örnek girdi: İki kulaklıktan biri bozuk, sipariş numarası 45821, iade sorusu.

`schemas.py` içindeki `MusteriTalebi` modeli şu alanları zorunlu tutar:

| Alan | Tip | Açıklama |
| --- | --- | --- |
| `kategori` | enum | `sikayet`, `bilgi_talebi`, `oneri` |
| `oncelik` | enum | `dusuk`, `orta`, `yuksek` |
| `siparis_no` | `str \| None` | Bilinmiyorsa `null` |
| `urunler` | `list[Urun]` | `urun_adi` (string) ve `adet` (pozitif tam sayı) |
| `ozet` | string | Boş olmayan Türkçe özet |
| `insan_onayi_gerekli` | bool | İnsan kontrolü işareti |

Ayrıca örnek iş kuralı: `oncelik == "yuksek"` olduğunda `insan_onayi_gerekli == true` olmalı.

**Önemli:** `str | None` alanlarının varsayılan değeri yoktur: Alanın JSON'da bulunması gerekir fakat değeri `null` olabilir. `extra="forbid"` beklenmeyen alanları reddeder. Modelin alıntıdaki ürün sayısını doğru anlaması ayrıca kaynakla karşılaştırılmalıdır.

## 6. Kod nasıl çalışır?

1. `schemas.py` içinden ortak Pydantic modeli içe aktarılır.
2. Python dosyasındaki `PROMPT` ve `model_json_schema()` birleştirilir.
3. Gemini veya Ollama'ya istek gönderilir; `schema` modunda API seviyesinde yapılandırılmış çıktı istenir.
4. **Ham yanıt terminale yazdırılır.**
5. `MusteriTalebi.model_validate_json()` ile JSON sözdizimi, alanlar, enum, tipler ve örnek iş kuralı kontrol edilir.
6. Hata çıkarsa hata mesajı sonraki denemeye eklenir. En fazla `MAX_DENEME` kez denenir.
7. Başarılıysa doğrulanmış JSON yazdırılır. Tüm denemeler başarısızsa hata yükseltilir; sessizce yanlış veri kabul edilmez.

Ağ, kota ve model bulunamaması gibi API hataları, veri doğrulama hatalarından ayrıdır. Bunlar otomatik olarak aynı şema retry döngüsünde çözülmez.

## 7. Derste yapılacak deney

1. `CIKTI_YONTEMI = "prompt"` ile Gemini çalıştırın, ham JSON'u inceleyin.
2. `CIKTI_YONTEMI = "schema"` yaparak tekrar çalıştırın; çıktı yapısını karşılaştırın.
3. Aynı iki denemeyi Ollama `qwen3:4b` ile yapın.
4. `schemas.py` dosyasında izin verilen kategorilerden birini çıkarın ve doğrulama davranışını gözlemleyin.
5. `insan_onayi_gerekli` iş kuralını açıklayın; neden şema doğrulamasından ayrı bir denetim olduğunu gösterin.
6. Sonuçları yapı uyumu ve anlam doğruluğu açısından değerlendirin; tek çalıştırmadan genel model üstünlüğü sonucu çıkarmayın.

## 8. Sık sorunlar

- `ModuleNotFoundError`: Sanal ortamı etkinleştirip paketleri yükleyin.
- `GEMINI_API_KEY`: Ortam değişkenini aynı terminalde tanımlayın.
- Gemini `404` / model hatası: Erişiminiz olan bir modeli `MODEL` değişkenine yazın.
- Ollama bağlantı hatası: Ollama servisinin çalıştığından emin olun.
- Ollama model bulunamadı: `ollama pull qwen3:4b` çalıştırın.
- `ValidationError`: Ham cevabı inceleyin; şema ile tip ve alan adlarını kontrol edin.
- Uzun/yarım JSON: Token sınırı ve şema karmaşıklığını inceleyin.

## 9. Güvenlik ve üretim notları

- Eğitimde gerçek müşteri verisi değil sentetik veri kullanın.
- Şema uyumu **olgusal doğruluk garantisi değildir**. Kaynak bilgileri ve iş kuralları ayrıca doğrulanmalıdır.
- Prompt injection'a karşı yalnızca şemaya güvenmeyin; veriyi talimattan ayırın ve yetki kontrollerini uygulama katmanında uygulayın.
- Retry sayısı sınırlı tutulmalıdır. Üretimde hatalı kayıtlar uygun loglama ve insan kontrolü akışına aktarılmalıdır.
