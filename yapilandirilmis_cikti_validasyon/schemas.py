"""Gemini ve Ollama uygulamalarının ortak Pydantic şeması."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class Urun(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    urun_adi: str = Field(min_length=1, description="Mesajdaki ürün adı")
    adet: int = Field(ge=1, description="Ürün adedi")

class MusteriTalebi(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    kategori: Literal["sikayet", "bilgi_talebi", "oneri"]
    oncelik: Literal["dusuk", "orta", "yuksek"]
    siparis_no: str | None = Field(description="Mesajda varsa sipariş numarası, yoksa null")
    urunler: list[Urun] = Field(description="Mesajda bahsedilen ürünlerin listesi")
    ozet: str = Field(min_length=1, description="Müşteri talebinin kısa Türkçe özeti")
    insan_onayi_gerekli: bool = Field(description="İnsan incelemesi gerekip gerekmediği")

    @model_validator(mode="after")
    def kritik_talep_kontrolu(self):
        # Eğitim amaçlı örnek İŞ KURALI: yüksek öncelikli taleplerde insan kontrolü zorunlu.
        if self.oncelik == "yuksek" and not self.insan_onayi_gerekli:
            raise ValueError("Yüksek öncelikli taleplerde insan_onayi_gerekli true olmalıdır")
        return self
