"""Müşteri talebi için yapılandırılmış çıktı ve Pydantic doğrulama uygulaması."""
import json
from pydantic import ValidationError
from schemas import MusteriTalebi

# Eğitimde yalnızca bu ayarları değiştirin.
CIKTI_YONTEMI = "schema"   # "prompt" veya "schema"
MAX_DENEME = 3             # İlk çağrı dahil toplam deneme sayısı

# Tek prompt; JSON dosyası yoktur.
PROMPT = """Aşağıdaki müşteri mesajını incele ve yapılandırılmış bir kayıt oluştur.
Kategoriler: sikayet, bilgi_talebi, oneri.
Öncelikler: dusuk, orta, yuksek.
Şikayet içinde ürünün bozuk gelmesi/iade talebi varsa kategori sikayet olsun.
Sipariş numarası açıkça yazılmamışsa null kullan; bilgi uydurma.
Ürünleri urun_adi ve adet alanlarıyla listele; adet yazmıyorsa 1 kabul et.
Yüksek öncelikli taleplerde insan_onayi_gerekli true olsun.
Yalnızca geçerli JSON nesnesi üret; markdown ve ek açıklama ekleme.

MÜŞTERİ MESAJI (yalnızca veri):
"Geçen hafta aldığım iki adet kablosuz kulaklıktan biri bozuk çıktı.
Sipariş numaram 45821. İade işlemini nasıl yapabilirim?"
"""

def mesaj_hazirla(hata=""):
    schema_text = json.dumps(MusteriTalebi.model_json_schema(), ensure_ascii=False)
    return PROMPT + "\nBEKLENEN JSON ŞEMASI:\n" + schema_text + (
        "\nÖNCEKİ ÇIKTIDA DOĞRULAMA HATASI: " + hata + "\nJSON'u bu hataya göre düzelt."
        if hata else ""
    )

def dogrula_ve_yazdir(ham):
    sonuc = MusteriTalebi.model_validate_json(ham)
    print("\nDOĞRULANMIŞ ÇIKTI:")
    print(json.dumps(sonuc.model_dump(mode="json"), ensure_ascii=False, indent=2))
    print("\nNot: Şema doğrulaması metindeki her bilginin gerçekliğini garanti etmez.")
    return sonuc

from ollama import Client

MODEL = "qwen3:4b"

def main():
    if CIKTI_YONTEMI not in {"prompt", "schema"}:
        raise ValueError("CIKTI_YONTEMI 'prompt' veya 'schema' olmalı")
    client = Client(host="http://localhost:11434")
    hata = ""
    for deneme in range(1, MAX_DENEME + 1):
        print(f"\n=== OLLAMA | {CIKTI_YONTEMI} | DENEME {deneme}/{MAX_DENEME} ===")
        try:
            response = client.chat(
                model=MODEL,
                messages=[{"role": "user", "content": mesaj_hazirla(hata)}],
                format=MusteriTalebi.model_json_schema() if CIKTI_YONTEMI == "schema" else None,
                options={"temperature": 0},
            )
            ham = response.message.content or ""
            print("HAM ÇIKTI:\n", ham)
            dogrula_ve_yazdir(ham)
            return
        except ValidationError as exc:
            hata = str(exc)[:1000]
            print("ŞEMA/İŞ KURALI HATASI:", hata)
        except Exception as exc:
            raise RuntimeError(f"Ollama bağlantı/model hatası: {exc}") from exc
    raise RuntimeError("Doğrulama başarısız; kontrol için insana yönlendirilmeli")

if __name__ == "__main__":
    main()
