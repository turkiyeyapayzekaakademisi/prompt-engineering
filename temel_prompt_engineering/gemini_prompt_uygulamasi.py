"""
Temel Prompt Engineering Teknikleri — Gemini API

Kurulum: pip install -U google-genai
API anahtarı: GEMINI_API_KEY ortam değişkeninde bulunmalı.
Çalıştırma: python gemini_prompt_uygulamasi.py
"""

import json
import os
from pathlib import Path

from google import genai
from google.genai import types

# =========================================================
# 0. AYARLAR — sadece burayı değiştirin
# =========================================================
PROMPT_TEKNIGI = "few_shot"
MODEL = "gemini-2.5-flash"
MUSTERI_MESAJI = "Aldığım kulaklık iki gün sonra bozuldu, iade etmek istiyorum."

PROMPT_DOSYASI = Path(__file__).with_name("prompts.json")

# =========================================================
# 1. JSON'DAN SEÇİLEN PROMPT'U OKU
# =========================================================
with PROMPT_DOSYASI.open("r", encoding="utf-8") as dosya:
    teknikler = json.load(dosya)

if PROMPT_TEKNIGI not in teknikler:
    raise ValueError(
        f"Bilinmeyen teknik: {PROMPT_TEKNIGI}. "
        f"Seçenekler: {', '.join(teknikler)}"
    )

secili = teknikler[PROMPT_TEKNIGI]
system_prompt = secili["system"]
user_prompt = secili["prompt"].replace("{{mesaj}}", MUSTERI_MESAJI)

print("\n=== SEÇİLEN PROMPT TEKNİĞİ ===")
print(f"Teknik: {PROMPT_TEKNIGI} — {secili['aciklama']}")
print(f"Model: {MODEL}")
print(f"\n[SYSTEM]\n{system_prompt}")
print(f"\n[USER]\n{user_prompt}")

# =========================================================
# 2. GEMINI API ÇAĞRISI
# =========================================================
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY ortam değişkenini tanımlayın.")

client = genai.Client(api_key=api_key)
try:
    yanit = client.models.generate_content(
        model=MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    print("\n=== GEMINI YANITI ===")
    print(yanit.text or "Metin yanıtı alınamadı.")
finally:
    client.close()
