"""Prompt construction for document-grounded answers."""

from __future__ import annotations

from collections.abc import Sequence

from .citations import format_citation
from .schemas import RetrievedChunk

SYSTEM_INSTRUCTION = """Sen, yalnızca sağlanan belge parçalarına dayanarak cevap veren bir trading
doküman araştırma asistanısın.

Kurallar:
1. Yalnızca KAYNAKLAR bölümündeki bilgiyle cevap ver.
2. Kaynakta olmayan bilgiyi tahmin etme, dış bilgini kullanma ve uydurma.
3. Kaynaklar soruyu doğrudan yanıtlamıyorsa açıkça yeterli bilgi olmadığını söyle.
4. Yatırım tavsiyesi, al-sat talimatı veya kesin kâr iddiası verme.
5. Cevabı Türkçe, kısa ve anlaşılır yaz.
6. Kaynak etiketi üretme; uygulama kaynak listesini cevabın altına ekleyecek.
"""


def build_context_block(chunks: Sequence[RetrievedChunk]) -> str:
    """Create a readable context block while preserving source identity."""
    if not chunks:
        return ""

    parts = []
    for position, chunk in enumerate(chunks, start=1):
        parts.append(
            "\n".join(
                [
                    f"--- KAYNAK {position} ---",
                    format_citation(chunk),
                    chunk.text,
                ]
            )
        )

    return "\n\n".join(parts)


def build_grounded_messages(
    question: str,
    chunks: Sequence[RetrievedChunk],
) -> list[dict[str, str]]:
    """Build system and user messages for one source-grounded answer request."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Soru boş olamaz.")

    context_block = build_context_block(chunks)
    user_content = (
        f"KAYNAKLAR:\n{context_block}\n\n"
        f"SORU:\n{question.strip()}\n\n"
        "Yalnızca yukarıdaki kaynaklara dayanarak cevap ver."
    )

    return [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": user_content},
    ]
