"""Local embedding model adapter.

The actual SentenceTransformer model is imported lazily. This keeps basic unit
tests fast and makes missing runtime dependencies fail with a clear message.
"""

from collections.abc import Sequence
from typing import Protocol

from .config import EMBEDDING_MODEL_NAME


class EmbeddingProvider(Protocol):
    """Small interface used by indexing and retrieval code."""

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """Create embeddings for document chunks."""

    def embed_query(self, text: str) -> list[float]:
        """Create an embedding for a user query."""


class SentenceTransformerEmbedder:
    """Embedding adapter using a local multilingual Sentence Transformers model."""

    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME) -> None:
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError(
                    "sentence-transformers kurulu değil. "
                    "Önce `python -m pip install -e .[dev]` komutunu çalıştırın."
                ) from exc

            self._model = SentenceTransformer(self.model_name)

        return self._model

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        model = self._get_model()
        vectors = model.encode(
            list(texts),
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Sorgu metni boş olamaz.")

        model = self._get_model()
        vector = model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vector.tolist()
