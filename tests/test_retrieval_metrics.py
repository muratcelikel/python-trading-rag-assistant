import pytest

from trading_rag_assistant.evaluation.dataset import RetrievalTestCase
from trading_rag_assistant.evaluation.retrieval_metrics import evaluate_source_hit_rate
from trading_rag_assistant.schemas import RetrievedChunk


class FakeRetriever:
    def search(self, question, top_k=None):
        if "risk" in question:
            return [RetrievedChunk(1, "x", "risk.md", "risk.md", 0, 1, 0.1)]
        return [RetrievedChunk(1, "x", "market.md", "market.md", 0, 1, 0.1)]


def test_source_hit_rate_counts_expected_source_in_top_k() -> None:
    cases = [
        RetrievalTestCase("risk question", "risk.md"),
        RetrievalTestCase("market question", "market.md"),
        RetrievalTestCase("wrong expected", "risk.md"),
    ]
    report = evaluate_source_hit_rate(FakeRetriever(), cases, top_k=3)

    assert report["metric"] == "source_hit_rate@3"
    assert report["hit_count"] == 2
    assert report["score"] == 0.6667


def test_source_hit_rate_rejects_empty_cases() -> None:
    with pytest.raises(ValueError, match="en az bir"):
        evaluate_source_hit_rate(FakeRetriever(), [])
