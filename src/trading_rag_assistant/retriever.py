"""Semantic retrieval service with a relevance guardrail."""

from __future__ import annotations

from .config import DEFAULT_MAX_DISTANCE, DEFAULT_TOP_K
from .embeddings import EmbeddingProvider
from .schemas import RetrievedChunk
from .vector_store import ChromaVectorStore


class SemanticRetriever:
    """Retrieve nearby chunks using the same model used for indexing."""

    def __init__(
        self,
        embedder: EmbeddingProvider,
        vector_store: ChromaVectorStore,
        default_top_k: int = DEFAULT_TOP_K,
        max_distance: float | None = DEFAULT_MAX_DISTANCE,
    ) -> None:
        if default_top_k <= 0:
            raise ValueError("default_top_k sıfırdan büyük olmalıdır.")
        if max_distance is not None and max_distance < 0:
            raise ValueError("max_distance negatif olamaz.")

        self.embedder = embedder
        self.vector_store = vector_store
        self.default_top_k = default_top_k
        self.max_distance = max_distance

    def search(
        self,
        question: str,
        top_k: int | None = None,
        source_key: str | None = None,
        max_distance: float | None = None,
    ) -> list[RetrievedChunk]:
        """Embed one question and return only sufficiently close source chunks."""
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Soru boş olamaz.")

        limit = top_k if top_k is not None else self.default_top_k
        if limit <= 0:
            raise ValueError("top_k sıfırdan büyük olmalıdır.")

        threshold = self.max_distance if max_distance is None else max_distance
        if threshold is not None and threshold < 0:
            raise ValueError("max_distance negatif olamaz.")

        query_embedding = self.embedder.embed_query(question)
        candidates = self.vector_store.query(
            query_embedding=query_embedding,
            n_results=limit,
            source_key=source_key,
        )
        if threshold is None:
            return candidates
        return [chunk for chunk in candidates if chunk.distance <= threshold]
