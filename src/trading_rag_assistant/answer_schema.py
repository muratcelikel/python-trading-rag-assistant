"""Data structures for source-grounded answers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence

from .schemas import RetrievedChunk


@dataclass(frozen=True)
class GroundedAnswer:
    """Answer text together with the source chunks used as context."""

    question: str
    answer: str
    sources: Sequence[RetrievedChunk]
    status: Literal["answered", "insufficient_context"]

    @property
    def used_sources(self) -> bool:
        return bool(self.sources)
