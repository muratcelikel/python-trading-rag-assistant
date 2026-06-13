"""Word-based text chunking utilities."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    chunk_id: int
    text: str
    start_word: int
    end_word: int


def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[TextChunk]:
    """Split text into overlapping word-based chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size sıfırdan büyük olmalıdır.")
    if overlap < 0:
        raise ValueError("overlap negatif olamaz.")
    if overlap >= chunk_size:
        raise ValueError("overlap, chunk_size değerinden küçük olmalıdır.")

    words = text.split()
    if not words:
        return []

    chunks = []
    step = chunk_size - overlap
    start = 0
    chunk_id = 1

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(
            TextChunk(
                chunk_id=chunk_id,
                text=" ".join(words[start:end]),
                start_word=start,
                end_word=end,
            )
        )
        if end == len(words):
            break
        start += step
        chunk_id += 1

    return chunks
