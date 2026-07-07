"""Single-document and multi-document indexing orchestration."""

from __future__ import annotations

from pathlib import Path

from .documents import SourceDocument, discover_documents, make_chunk_id
from .embeddings import EmbeddingProvider
from .pipeline import prepare_document
from .vector_store import ChromaVectorStore


def index_document(
    file_path: str | Path,
    embedder: EmbeddingProvider,
    vector_store: ChromaVectorStore,
    chunk_size: int = 100,
    overlap: int = 20,
    source_key: str | None = None,
) -> dict[str, int | str]:
    """Load, clean, chunk, embed and replace one source document."""
    path = Path(file_path)
    normalized_source_key = source_key or path.name
    prepared = prepare_document(path, chunk_size=chunk_size, overlap=overlap)
    chunks = prepared["chunks"]

    # Deleting by source prevents obsolete chunks surviving after a file becomes shorter.
    vector_store.delete_source(normalized_source_key)

    documents = [chunk.text for chunk in chunks]
    embeddings = embedder.embed_documents(documents)
    ids = [make_chunk_id(normalized_source_key, chunk.chunk_id) for chunk in chunks]
    metadatas = [
        {
            "source_file": path.name,
            "source_key": normalized_source_key,
            "chunk_id": chunk.chunk_id,
            "start_word": chunk.start_word,
            "end_word": chunk.end_word,
        }
        for chunk in chunks
    ]

    vector_store.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    return {
        "source_file": path.name,
        "source_key": normalized_source_key,
        "word_count": int(prepared["word_count"]),
        "chunk_count": int(prepared["chunk_count"]),
    }


def index_directory(
    directory: str | Path,
    embedder: EmbeddingProvider,
    vector_store: ChromaVectorStore,
    chunk_size: int = 100,
    overlap: int = 20,
) -> list[dict[str, int | str]]:
    """Index every supported source in a directory and return a compact report."""
    documents: list[SourceDocument] = discover_documents(directory)
    reports: list[dict[str, int | str]] = []
    for source in documents:
        reports.append(
            index_document(
                file_path=source.path,
                embedder=embedder,
                vector_store=vector_store,
                chunk_size=chunk_size,
                overlap=overlap,
                source_key=source.source_key,
            )
        )
    return reports
