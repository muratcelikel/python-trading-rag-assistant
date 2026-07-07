"""Index the sample trading document into local ChromaDB."""

from pathlib import Path

from trading_rag_assistant.embeddings import SentenceTransformerEmbedder
from trading_rag_assistant.indexer import index_document
from trading_rag_assistant.vector_store import ChromaVectorStore


def main() -> None:
    document_path = Path("data/sample/sample_strategy_notes.txt")

    result = index_document(
        file_path=document_path,
        embedder=SentenceTransformerEmbedder(),
        vector_store=ChromaVectorStore(),
        chunk_size=60,
        overlap=10,
    )

    print("İndeksleme tamamlandı.")
    print(f"Kaynak: {result['source_file']}")
    print(f"Kelime sayısı: {result['word_count']}")
    print(f"Vektör veritabanına eklenen parça: {result['chunk_count']}")


if __name__ == "__main__":
    main()
