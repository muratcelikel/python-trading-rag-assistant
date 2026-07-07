"""Run the local source-hit retrieval evaluation and write a JSON report."""

from __future__ import annotations

from pathlib import Path
import json

from trading_rag_assistant.config import OUTPUT_DIRECTORY
from trading_rag_assistant.embeddings import SentenceTransformerEmbedder
from trading_rag_assistant.evaluation.dataset import load_retrieval_testset
from trading_rag_assistant.evaluation.retrieval_metrics import evaluate_source_hit_rate
from trading_rag_assistant.retriever import SemanticRetriever
from trading_rag_assistant.vector_store import ChromaVectorStore


def main() -> None:
    testset_path = Path("data/evaluation/retrieval_testset.json")
    cases = load_retrieval_testset(testset_path)
    retriever = SemanticRetriever(
        embedder=SentenceTransformerEmbedder(),
        vector_store=ChromaVectorStore(),
    )
    report = evaluate_source_hit_rate(retriever, cases, top_k=3)
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT_DIRECTORY / "retrieval_evaluation.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{report['metric']}: {report['score']:.2%} ({report['hit_count']}/{report['test_case_count']})")
    print(f"Rapor yazıldı: {report_path}")


if __name__ == "__main__":
    main()
