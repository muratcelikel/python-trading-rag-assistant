"""Run a semantic search against the local sample index."""

from trading_rag_assistant.citations import format_retrieval_results
from trading_rag_assistant.embeddings import SentenceTransformerEmbedder
from trading_rag_assistant.retriever import SemanticRetriever
from trading_rag_assistant.vector_store import ChromaVectorStore


def main() -> None:
    question = "Günlük maksimum kayıp sınırı nedir?"

    retriever = SemanticRetriever(
        embedder=SentenceTransformerEmbedder(),
        vector_store=ChromaVectorStore(),
    )
    results = retriever.search(question)

    print(f"Soru: {question}\n")
    print(format_retrieval_results(results))


if __name__ == "__main__":
    main()
