"""Index all supported TXT/MD documents in a local folder."""

from __future__ import annotations

import argparse

from trading_rag_assistant.embeddings import SentenceTransformerEmbedder
from trading_rag_assistant.indexer import index_directory
from trading_rag_assistant.vector_store import ChromaVectorStore


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TXT/MD belgelerini toplu olarak indeksler.")
    parser.add_argument("directory", nargs="?", default="data/sample", help="Kaynak klasörü")
    parser.add_argument("--reset", action="store_true", help="Önce yerel indeks koleksiyonunu temizle")
    parser.add_argument("--chunk-size", type=int, default=80, help="Parça başına kelime sayısı")
    parser.add_argument("--overlap", type=int, default=15, help="Parçalar arası ortak kelime sayısı")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    store = ChromaVectorStore()
    if args.reset:
        store.clear()
        print("Yerel indeks temizlendi.")

    reports = index_directory(
        directory=args.directory,
        embedder=SentenceTransformerEmbedder(),
        vector_store=store,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
    if not reports:
        print("İndekslenecek desteklenen TXT/MD dosyası bulunamadı.")
        return

    print(f"İndekslenen belge sayısı: {len(reports)}")
    for report in reports:
        print(f"- {report['source_key']}: {report['chunk_count']} parça")
    print(f"Toplam kayıtlı parça: {store.count()}")


if __name__ == "__main__":
    main()
