# Temel Prompt Engineering Teknikleri — Gemini API ve Ollama

Bu proje, **aynı müşteri mesajına farklı prompt teknikleri uygulamayı** ve sonuçları iki model ortamında karşılaştırmayı öğretmek için hazırlanmıştır:

- **Bulut:** Google Gemini API (`gemini_prompt_uygulamasi.py`)
- **Yerel:** Ollama üzerinde `qwen3:4b` (`ollama_prompt_uygulamasi.py`)

Her iki uygulama **aynı `prompts.json` dosyasını** kullanır. Teknik seçimi kullanıcıdan giriş alınarak değil, Python dosyasının başındaki **`PROMPT_TEKNIGI` adlı sabit ayar değiştirilerek** yapılır. Bu, eğitim sırasında tek değişkenin etkisini kolayca görmeyi sağlar.

> Bu bir eğitim uygulamasıdır; üretim ortamına uygun bir müşteri yönlendirme veya güvenlik sistemi değildir. Müşteri mesajları örnektir; gerçek kişisel verilerle test etmeyin.

## 1. Öğrenme hedefleri

Bu projeyi tamamladığınızda:

1. Zero-shot, one-shot, few-shot ve diğer temel prompt desenlerini birbirinden ayırabileceksiniz.
2. Promptları Python koduna gömmek yerine JSON dosyasında tutabileceksiniz.
3. JSON'daki promptu seçilen müşteri mesajıyla birleştirerek modele gönderebileceksiniz.
4. Gemini API ile bulut modeline, Ollama API ile yerel modele bağlanabileceksiniz.
5. System ve user talimatlarının nerede kullanıldığını görebileceksiniz.
6. Aynı görevde teknik/model değişikliklerinin çıktı üzerindeki etkisini inceleyebileceksiniz.

## 2. Proje klasör yapısı

```text
temel_prompt_engineering/
├── gemini_prompt_uygulamasi.py    # Bulut modelini çağırır
├── ollama_prompt_uygulamasi.py    # Yerel qwen3:4b modelini çağırır
├── prompts.json                   # Tekniklere göre prompt şablonları
└── README.md                      # Proje açıklaması ve kurulum
```

**Dosyaların rolleri**

| Dosya | Görevi |
| --- | --- |
| `prompts.json` | Her teknik için `aciklama`, `system`, `prompt` alanlarını saklar. |
| `gemini_prompt_uygulamasi.py` | JSON'u okur, seçilen şablonu doldurur ve Gemini API ile çalıştırır. |
| `ollama_prompt_uygulamasi.py` | Aynı JSON'u okur, seçilen şablonu doldurur ve `qwen3:4b` modelini Ollama üzerinden çalıştırır. |
| `README.md` | Kurulum, çalışma adımları, karşılaştırma ve hata çözümlerini içerir. |

İki Python dosyasının farklı olmasının nedeni model bağlantı kodlarının farklı olmasıdır. **Teknik tanımları tek bir JSON dosyasında ortak tutulur.**

## 3. Gereksinimler

- Python **3.10 veya üzeri** önerilir.
- Gemini örneği için internet erişimi ve geçerli **Gemini API anahtarı** gerekir.
- Ollama örneği için bilgisayarda kurulu ve çalışan **Ollama** ile indirilmiş `qwen3:4b` modeli gerekir.
- `qwen3:4b` yerel donanım tüketir; RAM/VRAM ihtiyacı platforma, model sürümüne, bağlam uzunluğuna ve çalışma ayarlarına bağlıdır. Kısıtlı bilgisayarlarda yavaş çalışabilir.
- Dosyaları bir arada ve aynı klasörde tutun.

Gemini model kimliği örnekte `gemini-2.5-flash` olarak tanımlıdır. Kullanım hakkınız ve sağlayıcıdaki model erişiminiz değişebileceğinden gerekirse bu değişkeni erişiminiz olan model kimliğiyle güncelleyin.

## 4. Ortam hazırlığı — adım adım

### 4.1. ZIP dosyasını çıkartın ve klasöre geçin

ZIP paketini çıkarttıktan sonra terminali dosyaların bulunduğu klasörde açın.

```bash
cd temel_prompt_engineering
```

### 4.2. Python sürümünü kontrol edin

```bash
python --version
```

Bazı macOS/Linux kurulumlarında komut `python3` olabilir. Bu durumda aşağıdaki komutlarda da `python3` kullanabilirsiniz.

### 4.3. Sanal ortam oluşturun (önerilir)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Komut İstemi (CMD):

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

PowerShell aktivasyon ilkesi izin vermiyorsa, sanal ortamı etkinleştirmek yerine doğrudan `.venv\Scripts\python.exe` ile komutları çalıştırabilirsiniz.

### 4.4. Python paketlerini yükleyin

```bash
python -m pip install --upgrade pip
python -m pip install -U google-genai ollama
```

- `google-genai`: Gemini API istemcisi.
- `ollama`: Python üzerinden yerel Ollama sunucusuna bağlanır.
- `json` ve `pathlib`: Python standart kütüphanesidir, ayrıca kurulmaz.

## 5. Gemini API hazırlığı

### 5.1. API anahtarı edinin

1. Google AI Studio üzerinden Gemini API anahtarına erişin: <https://aistudio.google.com/apikey>
2. API anahtarını güvenli şekilde saklayın.
3. Anahtarı Python kaynak koduna veya `prompts.json` dosyasına doğrudan yazmayın.
4. Kod, anahtarı `GEMINI_API_KEY` adlı **ortam değişkeninden** okuyacaktır.

### 5.2. API anahtarını ortam değişkenine ekleyin

Windows PowerShell (yalnızca **mevcut terminal oturumu** için):

```powershell
$env:GEMINI_API_KEY="BURAYA_API_ANAHTARINIZ"
```

Windows CMD (yalnızca mevcut oturum için):

```bat
set GEMINI_API_KEY=BURAYA_API_ANAHTARINIZ
```

macOS/Linux (yalnızca mevcut oturum için):

```bash
export GEMINI_API_KEY="BURAYA_API_ANAHTARINIZ"
```

Aynı terminal penceresinde Python uygulamasını çalıştırın. Terminali kapatıp yeniden açarsanız bu oturum değişkenini tekrar ayarlamanız gerekebilir. Gerçek API anahtarını ekran görüntüsü, Git deposu veya eğitim çıktısında paylaşmayın.

### 5.3. Gemini uygulamasını çalıştırın

```bash
python gemini_prompt_uygulamasi.py
```

Kodun başındaki varsayılan ayarlar:

```python
PROMPT_TEKNIGI = "few_shot"
MODEL = "gemini-2.5-flash"
MUSTERI_MESAJI = "Aldığım kulaklık iki gün sonra bozuldu, iade etmek istiyorum."
```

Bu ayarlarla Gemini, JSON dosyasındaki `few_shot` şablonunu kullanarak müşteri mesajını sınıflandırmaya çalışır.

## 6. Ollama ile yerel model hazırlığı

### 6.1. Ollama'yı yükleyin

İşletim sisteminiz için kurulum: <https://ollama.com/download>

Kurulumdan sonra terminalde sürüm kontrolü yapabilirsiniz:

```bash
ollama --version
```

### 6.2. Modeli indirin

```bash
ollama pull qwen3:4b
```

Bu komut model ağırlıklarını bilgisayarınıza indirir. **İlk indirmede internet gerekir.** Model indirilip yerel sunucu hazırlandıktan sonra yerel model çıkarımı için bulut API anahtarına ihtiyaç yoktur. Yerel model kullanırken Ollama'nın bulut modellerini ayrıca seçmediğinizden emin olun.

İndirilen modelleri kontrol etmek için:

```bash
ollama list
```

### 6.3. Ollama servisinin çalıştığını doğrulayın

Ollama masaüstü uygulaması zaten arka planda çalışıyor olabilir. Çalışmıyorsa uygun bir terminalde sunucuyu başlatın:

```bash
ollama serve
```

**Not:** `ollama serve` mevcut çalışan servisle aynı portu kullanmaya çalışırsa port kullanım hatası verebilir. Bu, servis zaten açıksa ikinci kez başlatmanız gerekmediği anlamına gelebilir.

İsteğe bağlı olarak modelle terminalde sohbet edebilirsiniz:

```bash
ollama run qwen3:4b
```

### 6.4. Ollama Python uygulamasını çalıştırın

```bash
python ollama_prompt_uygulamasi.py
```

Kodun başındaki varsayılan ayarlar:

```python
PROMPT_TEKNIGI = "few_shot"
MODEL = "qwen3:4b"
OLLAMA_ADRESI = "http://localhost:11434"
MUSTERI_MESAJI = "Aldığım kulaklık iki gün sonra bozuldu, iade etmek istiyorum."
```

`localhost:11434`, Ollama'nın varsayılan **yerel API adresidir**. Uzak sunucu kullanmıyorsanız değiştirmeyin.

> Ollama örneğindeki `qwen3:4b`, reasoning davranışı ve çıktı uzunluğu bakımından Gemini'den farklılık gösterebilir. Bu örnekte Qwen3 için düşünme modu ayrıca yapılandırılmıyor. Karşılaştırma sırasında yalnızca sonuç kalitesine değil, üretilen metnin biçimine ve süresine de bakın.

## 7. Teknik nasıl seçiliyor?

**En önemli ayar:** Her iki Python dosyasının başındaki `PROMPT_TEKNIGI` değişkenidir.

```python
PROMPT_TEKNIGI = "zero_shot"
```

Örneğin önce `zero_shot` seçip dosyayı çalıştırın, daha sonra yalnızca bu satırı `one_shot`, ardından `few_shot` olarak değiştirip yeniden çalıştırın. Uygulama sizden terminalde teknik seçmenizi istemez; bu değer **hard-coded** olarak belirlenmiştir.

### Teknik listesi

| `PROMPT_TEKNIGI` değeri | Öğrettiği yaklaşım | JSON'da ne değişir? |
| --- | --- | --- |
| `zero_shot` | Örneksiz talimat | Yalnızca görev verilir. |
| `one_shot` | Tek örnekle yönlendirme | Tek mesaj/kategori örneği vardır. |
| `few_shot` | Çoklu örnekle yönlendirme | Üç örnek gösterilir. |
| `rol_verme` | Modelin rolünü belirleme | `system` alanında müşteri destek uzmanı rolü verilir. |
| `baglam_ekleme` | Kuruma özgü bağlam ekleme | Şirketin sınıflandırma politikası belirtilir. |
| `hedef_kitle` | Hedef kitleye göre anlatım | Üst yönetime uygun kısa, teknik olmayan açıklama istenir. |
| `kisit_belirleme` | Sınır ve kurallarla yönlendirme | İzin verilen kategoriler ve azami uzunluk belirtilir. |
| `cikti_formati` | Belirli çıktı formatı isteme | Modelden JSON biçiminde yanıt istenir. |

**Önemli:** Son beş desen, zero-shot/one-shot/few-shot ile birbirini dışlayan teknikler değildir. Gerçek projelerde rol, bağlam, kısıt ve çıktı formatını bir arada kullanabilirsiniz. Bu örnekte öğretim amacıyla ayrı seçenekler halinde tutulmuştur.

## 8. `prompts.json` nasıl çalışıyor?

Dosyanın en üst seviyesinde teknik isimleri bulunur. Her teknik üç alan içerir:

- `aciklama`: Kullanılan yöntemin kısa özeti; terminale yazdırılır.
- `system`: Modele gönderilen sistem talimatı.
- `prompt`: Müşteri mesajının yerleştirileceği user prompt şablonu.

Örnek (dosyanın tamamı değil):

```json
{
  "zero_shot": {
    "aciklama": "Örnek vermeden müşteri mesajını sınıflandırma",
    "system": "Türkçe yanıt veren bir asistansın.",
    "prompt": "Aşağıdaki müşteri mesajını değerlendir ve talebin türünü belirt.\n\nMüşteri mesajı:\n{{mesaj}}"
  }
}
```

`{{mesaj}}`, **placeholder** olarak kullanılan özel metindir. Python aşağıdaki satırla bu bölümü gerçek müşteri mesajıyla değiştirir:

```python
user_prompt = secili["prompt"].replace("{{mesaj}}", MUSTERI_MESAJI)
```

Bu örnekte `str.replace()` kullanıldığı için gelişmiş şablon motoru veya dinamik değişken doğrulaması bulunmuyor. JSON'a yeni bir teknik eklediğinizde `system`, `prompt` ve `aciklama` alanlarını eksiksiz yazın.

### Yeni bir teknik ekleme

1. `prompts.json` dosyasına yeni bir üst seviye anahtar ekleyin; örneğin `ozel_teknik`.
2. `aciklama`, `system`, `prompt` alanlarını doldurun.
3. Müşteri mesajının geleceği konumda `{{mesaj}}` kullanın.
4. JSON sözdiziminin geçerli olduğundan emin olun (özellikle virgül ve çift tırnaklar).
5. Python'da `PROMPT_TEKNIGI = "ozel_teknik"` yapın.
6. Dosyayı yeniden çalıştırın.

JSON dosyasının geçerliliğini kontrol etmek için:

```bash
python -m json.tool prompts.json
```

## 9. Python dosyaları adım adım nasıl çalışıyor?

Her iki Python dosyasının işlem sırası aynıdır; yalnızca son model çağrısı farklıdır.

**Adım 0 — Ayarları seçme**

`PROMPT_TEKNIGI`, `MODEL` ve `MUSTERI_MESAJI` dosyanın başında tanımlanır. Ollama tarafında ayrıca `OLLAMA_ADRESI` vardır.

**Adım 1 — JSON dosyasını bulma**

```python
PROMPT_DOSYASI = Path(__file__).with_name("prompts.json")
```

Bu kullanım JSON'u Python dosyasıyla **aynı klasörde** arar. Bu nedenle programı başka bir çalışma klasöründen başlatsanız bile dosya yolu korunur.

**Adım 2 — JSON dosyasını okuma**

```python
with PROMPT_DOSYASI.open("r", encoding="utf-8") as dosya:
    teknikler = json.load(dosya)
```

`utf-8`, Türkçe karakterlerin doğru okunmasına yardımcı olur. `json.load`, JSON verisini Python sözlüğüne çevirir.

**Adım 3 — Teknik adını kontrol etme**

Seçilen anahtar JSON'da yoksa `ValueError` oluşur ve kullanılabilir teknikler gösterilir. Böylece yanlış teknik adıyla model çağrısı yapılmaz.

**Adım 4 — System ve user promptlarını hazırlama**

```python
secili = teknikler[PROMPT_TEKNIGI]
system_prompt = secili["system"]
user_prompt = secili["prompt"].replace("{{mesaj}}", MUSTERI_MESAJI)
```

İki ayrı mesaj hazırlıyoruz: uygulamanın genel davranışını anlatan **system** talimatı ve üzerinde çalışılacak görevi içeren **user** promptu.

**Adım 5 — Promptu ekrana yazdırma**

Her iki uygulama da model çağrısından önce teknik adını, açıklamasını, model kimliğini, system ve user promptlarını terminale yazdırır. Böylece JSON'dan gerçekten hangi promptun okunduğunu görebilirsiniz.

**Adım 6A — Gemini modeline gönderme**

Gemini uygulaması `GEMINI_API_KEY` ortam değişkenini okur ve Google GenAI istemcisiyle çağrı yapar:

```python
yanit = client.models.generate_content(
    model=MODEL,
    contents=user_prompt,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)
```

Burada `contents` kullanıcı talimatını, `system_instruction` ise sistem talimatını taşır. API erişimi gerektirir.

**Adım 6B — Ollama modeline gönderme**

Ollama uygulaması yerel sunucuya aşağıdaki mesaj yapısını gönderir:

```python
yanit = client.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
)
```

Aynı talimatlar farklı sağlayıcılara özgü çağrı biçimleriyle aktarılır. Roller ve davranışlar sağlayıcılar arasında tam olarak birebir aynı olmayabilir.

**Adım 7 — Yanıtı ekrana yazdırma**

Gemini tarafında `yanit.text`, Ollama tarafında `yanit.message.content` alınır. Bu örnekte dosyaya/veritabanına kayıt veya otomatik kalite puanlaması yapılmaz.

### Genel akış

```text
PROMPT_TEKNIGI seç
        |
        v
prompts.json dosyasını oku
        |
        v
Seçilen system ve prompt alanlarını al
        |
        v
{{mesaj}} -> MUSTERI_MESAJI ile değiştir
        |
        v
Prompt'u terminale yazdır
        |
        +-----------------------+
        |                       |
        v                       v
 Gemini API                 Ollama API
 (bulut)                    (yerel)
        |                       |
        +------------+----------+
                     |
                     v
              Yanıtı yazdır
```

## 10. Örnek bir çalıştırma

Her iki Python dosyasında:

```python
PROMPT_TEKNIGI = "few_shot"
MUSTERI_MESAJI = "Aldığım kulaklık iki gün sonra bozuldu, iade etmek istiyorum."
```

Bu durumda JSON'daki few-shot promptu, önce şu örnekleri içerir:

- "Ürün hasarlı geldi." → Şikayet
- "Teslimat süreniz kaç gün?" → Bilgi Talebi
- "Mobil uygulamaya karanlık mod ekleyebilirsiniz." → Öneri

Ardından gerçek müşteri mesajı eklenir. Modelin **muhtemel** çıktısı `Şikayet` olabilir. Bu yalnızca beklenen örnektir, garanti edilen bir yanıt değildir.

Terminal yapısı yaklaşık şöyledir:

```text
=== SEÇİLEN PROMPT TEKNİĞİ ===
Teknik: few_shot — Birden fazla örnekle kategorileri ve çıktı biçimini gösterme
Model: gemini-2.5-flash

[SYSTEM]
Türkçe yanıt veren bir asistansın.

[USER]
Müşteri mesajını aşağıdaki örnekler gibi sınıflandır.
...
Mesaj: Aldığım kulaklık iki gün sonra bozuldu, iade etmek istiyorum.
Kategori:

=== GEMINI YANITI ===
Şikayet
```

Ollama uygulamasında aynı yerleşim `=== OLLAMA YANITI ===` başlığıyla gösterilir. Qwen3 modelinin çıktısı bu örnekten daha uzun veya farklı formatta olabilir.

## 11. Sınıf içi uygulama planı

Katılımcılarla aynı mesaj ve modeli kullanarak teknikleri sırayla değiştirmek faydalıdır:

| Deney | Yapılacak değişiklik | İncelenecek nokta |
| --- | --- | --- |
| 1 | `PROMPT_TEKNIGI = "zero_shot"` | Örnek olmadan görev anlaşılıyor mu? |
| 2 | `"one_shot"` | Tek örnek, etiketi veya yanıt biçimini etkiliyor mu? |
| 3 | `"few_shot"` | Üç örnek sonucu daha tutarlı yapıyor mu? |
| 4 | `"rol_verme"` | Rol, açıklama tonunu değiştiriyor mu? |
| 5 | `"baglam_ekleme"` | Kurumun sınıf tanımları sonucu etkiliyor mu? |
| 6 | `"hedef_kitle"` | Yanıt üst yönetime daha uygun mu? |
| 7 | `"kisit_belirleme"` | Kategori ve uzunluk sınırına uyuluyor mu? |
| 8 | `"cikti_formati"` | JSON istenen yapıya benziyor mu? |
| 9 | Aynı teknikle Gemini ve Ollama | Model değişince sonuç değişiyor mu? |

**İkinci test mesajı önerisi:** `Siparişimin ne zaman kargoya verileceğini öğrenmek istiyorum.` Beklenen kategori: **Bilgi Talebi**.

**Üçüncü test mesajı önerisi:** `Uygulamada sipariş geçmişini Excel olarak indirebilsek iyi olur.` Beklenen kategori: **Öneri**.

**Dördüncü test mesajı önerisi:** `Üründen memnunum ama teslimat gecikti.` Bu mesaj birden fazla yorum içerdiğinden kurumun karar kuralı açıkça tanımlanmalıdır; tek ve tartışmasız bir etiket varmış gibi değerlendirmeyin.

### Elle karşılaştırma tablosu

| Teknik | Model | Beklenen kategori | Gelen kategori | Format uygun mu? | Eğitmen notu |
| --- | --- | --- | --- | --- | --- |
| zero_shot | Gemini | Şikayet | ... | ... | ... |
| one_shot | Gemini | Şikayet | ... | ... | ... |
| few_shot | Gemini | Şikayet | ... | ... | ... |
| zero_shot | Qwen3 | Şikayet | ... | ... | ... |
| few_shot | Qwen3 | Şikayet | ... | ... | ... |

İlk aşamada manuel değerlendirme yeterlidir. **Daha ileri otomatik değerlendirme**, golden set, A/B testi, token ve gecikme hesapları bu eğitim müfredatının sonraki bölümlerinde ele alınacaktır.

## 12. Sık karşılaşılan hatalar ve çözümleri

| Hata / belirti | Olası neden | Çözüm |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'google'` | Gemini SDK kurulu değil veya yanlış Python ortamı kullanılıyor. | Etkin ortamda `python -m pip install -U google-genai` çalıştırın. |
| `ModuleNotFoundError: No module named 'ollama'` | Ollama Python paketi kurulu değil. | `python -m pip install -U ollama` çalıştırın. |
| `GEMINI_API_KEY ortam değişkenini tanımlayın` | API anahtarı mevcut terminal oturumuna tanımlanmamış. | Bölüm 5.2'deki işletim sisteminize uygun komutu aynı terminalde çalıştırın. |
| `401` / `403` / API anahtarı hatası | Anahtar geçersiz, erişim yok veya proje yetkisi yetersiz. | AI Studio anahtarını ve model erişimini kontrol edin. |
| `429` / Kota hatası | API sınırı veya kota aşılmış. | Kota durumunu kontrol edin, daha sonra yeniden deneyin veya izin verilen bir model kullanın. |
| Model bulunamadı / `404` | Yanlış model kimliği veya erişilmeyen model. | Python'daki `MODEL` değerini kontrol edin. |
| Ollama bağlantı reddedildi | Ollama servisi çalışmıyor veya farklı adreste. | Ollama'yı açın, gerekirse `ollama serve` çalıştırın; `OLLAMA_ADRESI` değerini kontrol edin. |
| Ollama modeli bulunamadı | `qwen3:4b` indirilmemiş. | `ollama pull qwen3:4b` ve `ollama list` kullanın. |
| Çok yavaş yanıt | Model donanımda yavaş çalışıyor veya ilk yükleme sürüyor. | Donanım kullanımını kontrol edin; model seçimini ortama göre değerlendirin. |
| `FileNotFoundError: prompts.json` | JSON dosyası aynı klasörde değil. | `prompts.json` dosyasını iki Python dosyasıyla aynı klasöre koyun. |
| `JSONDecodeError` | JSON sözdizimi bozuk. | `python -m json.tool prompts.json` ile kontrol edin. |
| `Bilinmeyen teknik` | `PROMPT_TEKNIGI` JSON anahtarıyla eşleşmiyor. | Bölüm 7'deki geçerli anahtarlardan birini seçin. |
| JSON yerine düz metin geliyor | `cikti_formati` yalnızca prompt düzeyinde biçim ister. | Çıktıyı doğrulayın; üretim senaryosunda API seviyesinde şema kısıtlama kullanın. |

## 13. Önemli sınırlamalar ve güvenlik notları

1. **Prompt ile JSON istemek, geçerli JSON'u garanti etmez.** `cikti_formati` yalnızca prompt talimatını gösterir. JSON Schema, Pydantic ve API seviyesinde yapılandırılmış çıktı sonraki uygulamada incelenecektir.
2. **Bu uygulamalar çıktı kalitesini otomatik ölçmez.** Aynı prompt için farklı modellerin yanıtları farklı olabilir; tek çalıştırma üzerinden genel üstünlük iddia etmeyin.
3. **Gerçek müşteri verisi kullanmayın.** Örneklerde sentetik mesajlar tercih edin; kişisel veriler kurumun veri koruma politikasına uygun işlenmelidir.
4. **System prompt güvenlik duvarı değildir.** Modelin talimatları takip etmesi güvenlik, yetkilendirme ve veri sızıntısı kontrollerinin yerine geçmez.
5. **Gemini bulut hizmetidir.** Gönderdiğiniz içerik sağlayıcının API altyapısına iletilir. Ollama yerel model kullanıldığında çıkarım yerel çalışır; seçilen ürün ve yapılandırmanın gerçekten yerel olduğundan emin olun.
6. **Token, gecikme ve maliyet ölçümleri henüz otomatikleştirilmedi.** Bu proje öncelikle prompt tekniklerini öğretir.
7. **Aynı model ailesi bile sürüm değişikliğiyle farklı davranabilir.** Uygulamadaki model kimliklerini ve test sonuçlarını birlikte kaydetmek yararlıdır.
8. **Sabit şablona kullanıcı verisi koymak güvenilir kaynak anlamına gelmez.** `{{mesaj}}` ile eklenen metin işlenecek veridir; uygulama talimatlarını değiştirmesine izin verilmemelidir.

## 14. Projeyi genişletme önerileri

Temel örneği tamamladıktan sonra aşağıdaki geliştirmeler ayrı alıştırma olarak yapılabilir:

- `prompts.json` içine yeni teknikler eklemek.
- Farklı müşteri mesajlarını sırayla çalıştıran bir döngü oluşturmak.
- Her yanıtı CSV/JSON dosyasına kaydederek manuel karşılaştırma tablosu hazırlamak.
- Çıktı formatını gerçek bir JSON Schema ile kısıtlamak ve Pydantic ile doğrulamak.
- Token tüketimi, gecikme ve tahmini maliyet ölçmek.
- Aynı test girdileriyle farklı model ve prompt sürümlerini karşılaştırmak.

**Eğitim sonucu:** Aynı prompt veri seti ve aynı örnek mesajlar üzerinden bulut ve yerel LLM çağrısı yapılır; zero-shot/few-shot, rol, bağlam, kısıt ve çıktı biçimi gibi tekniklerin model davranışını nasıl etkileyebildiği gözlemlenir.
