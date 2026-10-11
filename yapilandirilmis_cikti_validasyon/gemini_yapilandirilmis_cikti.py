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

import os
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"

def main():
    if CIKTI_YONTEMI not in {"prompt", "schema"}:
        raise ValueError("CIKTI_YONTEMI 'prompt' veya 'schema' olmalı")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY ortam değişkenini ayarlayın")
    client = genai.Client(api_key=api_key)
    hata = ""
    for deneme in range(1, MAX_DENEME + 1):
        print(f"\n=== GEMINI | {CIKTI_YONTEMI} | DENEME {deneme}/{MAX_DENEME} ===")
        try:
            config_args = {"temperature": 0}
            if CIKTI_YONTEMI == "schema":
                config_args.update(response_mime_type="application/json", response_schema=MusteriTalebi)
            response = client.models.generate_content(
                model=MODEL,
                contents=mesaj_hazirla(hata),
                config=types.GenerateContentConfig(**config_args),
            )
            ham = response.text or ""
            print("HAM ÇIKTI:\n", ham)
            dogrula_ve_yazdir(ham)
            return
        except ValidationError as exc:
            hata = str(exc)[:1000]
            print("ŞEMA/İŞ KURALI HATASI:", hata)
        except Exception as exc:
            raise RuntimeError(f"Gemini API hatası: {exc}") from exc
    raise RuntimeError("Doğrulama başarısız; kontrol için insana yönlendirilmeli")

if __name__ == "__main__":
    main()
