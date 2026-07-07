"""Typed data structures used by preprocessing and retrieval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    """A document chunk returned by semantic retrieval."""

    chunk_id: int
    text: str
    source_file: str
    source_key: str
    start_word: int
    end_word: int
    distance: float

    @property
    def similarity_hint(self) -> float:
        """Return a simple 0-1 display hint derived from cosine distance.

        This is intended for transparent debugging output, not as a calibrated
        probability or a claim of answer correctness.
        """
        return max(0.0, min(1.0, 1.0 - self.distance))
