"""
Temel Prompt Engineering Teknikleri — Yerel Ollama (qwen3:4b)

Kurulum: pip install -U ollama
Modeli indir: ollama pull qwen3:4b
Çalıştırma: python ollama_prompt_uygulamasi.py
Ollama servisinin açık olması gerekir.
"""

import json
from pathlib import Path

from ollama import Client

# =========================================================
# 0. AYARLAR — sadece burayı değiştirin
# =========================================================
PROMPT_TEKNIGI = "few_shot"
MODEL = "qwen3:4b"
OLLAMA_ADRESI = "http://localhost:11434"
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
# 2. YEREL OLLAMA ÇAĞRISI
# =========================================================
client = Client(host=OLLAMA_ADRESI)
yanit = client.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
)

print("\n=== OLLAMA YANITI ===")
print(yanit.message.content or "Metin yanıtı alınamadı.")
