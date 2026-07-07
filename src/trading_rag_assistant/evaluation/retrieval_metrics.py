"""Dependency-light retrieval evaluation for the MVP stage."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Protocol, Sequence

from .dataset import RetrievalTestCase


class SearchProvider(Protocol):
    def search(self, question: str, top_k: int | None = None):
        """Return retrieved chunks with source_key attributes."""


@dataclass(frozen=True)
class RetrievalEvaluationResult:
    question: str
    expected_source_key: str
    retrieved_source_keys: list[str]
    hit: bool


def evaluate_source_hit_rate(
    retriever: SearchProvider,
    cases: Sequence[RetrievalTestCase],
    top_k: int = 3,
) -> dict:
    """Measure whether the expected source appears in top-k retrieval results."""
    if top_k <= 0:
        raise ValueError("top_k sıfırdan büyük olmalıdır.")
    if not cases:
        raise ValueError("Değerlendirme için en az bir test sorusu gerekir.")

    rows: list[RetrievalEvaluationResult] = []
    for case in cases:
        chunks = retriever.search(case.question, top_k=top_k)
        retrieved_sources = [chunk.source_key for chunk in chunks]
        rows.append(
            RetrievalEvaluationResult(
                question=case.question,
                expected_source_key=case.expected_source_key,
                retrieved_source_keys=retrieved_sources,
                hit=case.expected_source_key in retrieved_sources,
            )
        )

    hit_count = sum(1 for row in rows if row.hit)
    return {
        "metric": f"source_hit_rate@{top_k}",
        "test_case_count": len(rows),
        "hit_count": hit_count,
        "score": round(hit_count / len(rows), 4),
        "results": [asdict(row) for row in rows],
    }
