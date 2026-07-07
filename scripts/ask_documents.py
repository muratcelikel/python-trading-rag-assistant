"""Ask a source-grounded question against the local multi-document index."""

from __future__ import annotations

import argparse

from trading_rag_assistant.citations import format_grounded_answer
from trading_rag_assistant.embeddings import SentenceTransformerEmbedder
from trading_rag_assistant.llm_client import GroqAnswerGenerator
from trading_rag_assistant.query_engine import GroundedQueryEngine
from trading_rag_assistant.retriever import SemanticRetriever
from trading_rag_assistant.vector_store import ChromaVectorStore


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Kaynak dayanaklı RAG sorusu sorar.")
    parser.add_argument("question", nargs="+", help="Sorulacak soru")
    parser.add_argument("--top-k", type=int, default=3, help="En fazla kaynak parçası sayısı")
    parser.add_argument("--max-distance", type=float, default=None, help="İsteğe bağlı mesafe eşiği")
    parser.add_argument("--source", default=None, help="İsteğe bağlı kaynak filtresi, ör: risk_management_notes.md")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    retriever = SemanticRetriever(
        embedder=SentenceTransformerEmbedder(),
        vector_store=ChromaVectorStore(),
        default_top_k=args.top_k,
    )
    engine = GroundedQueryEngine(
        retriever=retriever,
        answer_generator=GroqAnswerGenerator(),
        default_top_k=args.top_k,
    )
    result = engine.ask(
        question=" ".join(args.question),
        top_k=args.top_k,
        source_key=args.source,
        max_distance=args.max_distance,
    )
    print(format_grounded_answer(result))


if __name__ == "__main__":
    main()
