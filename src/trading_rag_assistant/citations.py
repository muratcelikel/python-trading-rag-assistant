"""Formatting helpers for transparent retrieval and answer output."""

from __future__ import annotations

from collections.abc import Sequence

from .answer_schema import GroundedAnswer
from .schemas import RetrievedChunk


def format_citation(chunk: RetrievedChunk) -> str:
    """Return a compact source label."""
    return (
        f"[Kaynak: {chunk.source_key} | Parça {chunk.chunk_id} | "
        f"Kelime {chunk.start_word}-{chunk.end_word}]"
    )


def format_retrieval_results(results: Sequence[RetrievedChunk]) -> str:
    """Render raw retrieval evidence for debugging and inspection."""
    if not results:
        return "Eşik altında yeterince ilgili kaynak parçası bulunamadı."

    blocks: list[str] = []
    for index, chunk in enumerate(results, start=1):
        blocks.append(
            "\n".join(
                [
                    f"{index}. {format_citation(chunk)}",
                    f"Mesafe: {chunk.distance:.4f} | Benzerlik ipucu: {chunk.similarity_hint:.2f}",
                    chunk.text,
                ]
            )
        )
    return "\n\n".join(blocks)


def format_grounded_answer(result: GroundedAnswer) -> str:
    """Render answer plus the exact chunks passed into answer generation."""
    lines = [f"Soru: {result.question}", f"Durum: {result.status}", "", "Cevap:", result.answer]
    if result.sources:
        lines.extend(["", "Kullanılan kaynak parçaları:"])
        lines.extend(f"- {format_citation(source)}" for source in result.sources)
    else:
        lines.extend(["", "Kullanılan kaynak parçası: yok"])
    return "\n".join(lines)
