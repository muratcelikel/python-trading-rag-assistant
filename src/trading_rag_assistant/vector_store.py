"""ChromaDB persistence and similarity-query adapter."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from .config import COLLECTION_NAME, VECTOR_DB_DIRECTORY
from .schemas import RetrievedChunk


class ChromaVectorStore:
    """Local persistent ChromaDB collection for document embeddings."""

    def __init__(
        self,
        persist_directory: str | Path = VECTOR_DB_DIRECTORY,
        collection_name: str = COLLECTION_NAME,
    ) -> None:
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self._client = None
        self._collection = None

    def _get_client(self):
        if self._client is None:
            try:
                import chromadb
            except ImportError as exc:
                raise RuntimeError(
                    "chromadb kurulu değil. "
                    "Önce `python -m pip install -e .[dev]` komutunu çalıştırın."
                ) from exc

            self.persist_directory.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=str(self.persist_directory))
        return self._client

    def _get_collection(self):
        if self._collection is None:
            self._collection = self._get_client().get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def upsert(
        self,
        ids: Sequence[str],
        documents: Sequence[str],
        metadatas: Sequence[dict[str, Any]],
        embeddings: Sequence[Sequence[float]],
    ) -> None:
        """Insert or replace document chunks and their vectors."""
        lengths = {len(ids), len(documents), len(metadatas), len(embeddings)}
        if len(lengths) != 1:
            raise ValueError("ids, documents, metadatas ve embeddings aynı uzunlukta olmalıdır.")
        if not ids:
            return

        self._get_collection().upsert(
            ids=list(ids),
            documents=list(documents),
            metadatas=list(metadatas),
            embeddings=[list(vector) for vector in embeddings],
        )

    def delete_source(self, source_key: str) -> None:
        """Remove all previous chunks for one source before re-indexing it."""
        if not source_key:
            raise ValueError("source_key boş olamaz.")
        self._get_collection().delete(where={"source_key": source_key})

    def clear(self) -> None:
        """Delete the current collection and recreate it lazily on the next operation."""
        client = self._get_client()
        try:
            client.delete_collection(name=self.collection_name)
        except ValueError:
            # An empty/new local database may not contain the collection yet.
            pass
        self._collection = None

    def count(self) -> int:
        """Return the number of stored chunks."""
        return int(self._get_collection().count())

    def query(
        self,
        query_embedding: Sequence[float],
        n_results: int,
        source_key: str | None = None,
    ) -> list[RetrievedChunk]:
        """Return nearest chunks for one query embedding, optionally from one source."""
        if n_results <= 0:
            raise ValueError("n_results sıfırdan büyük olmalıdır.")

        arguments: dict[str, Any] = {
            "query_embeddings": [list(query_embedding)],
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"],
        }
        if source_key:
            arguments["where"] = {"source_key": source_key}

        result = self._get_collection().query(**arguments)
        documents = result.get("documents", [[]])[0] or []
        metadatas = result.get("metadatas", [[]])[0] or []
        distances = result.get("distances", [[]])[0] or []

        retrieved: list[RetrievedChunk] = []
        for document, metadata, distance in zip(documents, metadatas, distances):
            metadata = metadata or {}
            retrieved.append(
                RetrievedChunk(
                    chunk_id=int(metadata.get("chunk_id", 0)),
                    text=str(document),
                    source_file=str(metadata.get("source_file", "bilinmeyen_kaynak")),
                    source_key=str(metadata.get("source_key", "bilinmeyen_kaynak")),
                    start_word=int(metadata.get("start_word", 0)),
                    end_word=int(metadata.get("end_word", 0)),
                    distance=float(distance),
                )
            )
        return retrieved
