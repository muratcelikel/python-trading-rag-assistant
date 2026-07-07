"""Ask one question against the sample index and show its sources."""

from __future__ import annotations

import argparse

from trading_rag_assistant.citations import format_grounded_answer
from trading_rag_assistant.embeddings import SentenceTransformerEmbedder
from trading_rag_assistant.llm_client import GroqAnswerGenerator
from trading_rag_assistant.query_engine import GroundedQueryEngine
from trading_rag_assistant.retriever import SemanticRetriever
from trading_rag_assistant.vector_store import ChromaVectorStore


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Yerel trading doküman indeksine kaynak dayanaklı soru sorar."
    )
    parser.add_argument(
        "question",
        nargs="+",
        help="Sorulacak soru. Örnek: Günlük maksimum kayıp sınırı nedir?",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Kullanılacak en fazla kaynak parçası sayısı.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    question = " ".join(args.question)

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

    result = engine.ask(question)
    print(format_grounded_answer(result))


if __name__ == "__main__":
    main()
