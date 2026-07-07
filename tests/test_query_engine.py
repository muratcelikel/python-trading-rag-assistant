from trading_rag_assistant.citations import format_grounded_answer
from trading_rag_assistant.query_engine import GroundedQueryEngine
from trading_rag_assistant.schemas import RetrievedChunk


class FakeRetriever:
    def __init__(self, results):
        self.results = results
        self.calls = []

    def search(self, question, top_k=None, source_key=None, max_distance=None):
        self.calls.append((question, top_k, source_key, max_distance))
        return self.results


class FakeGenerator:
    def __init__(self):
        self.messages = None

    def generate(self, messages):
        self.messages = list(messages)
        return "Günlük maksimum kayıp yüzde iki ile sınırlandırılmıştır."


def make_chunk() -> RetrievedChunk:
    return RetrievedChunk(3, "Günlük maksimum kayıp yüzde iki.", "risk.md", "risk.md", 50, 61, 0.12)


def test_query_engine_returns_answer_and_preserves_sources() -> None:
    retriever = FakeRetriever([make_chunk()])
    generator = FakeGenerator()
    engine = GroundedQueryEngine(retriever, generator)

    result = engine.ask("Günlük maksimum kayıp sınırı nedir?", top_k=1, source_key="risk.md")

    assert result.status == "answered"
    assert result.used_sources is True
    assert "yüzde iki" in result.answer
    assert retriever.calls == [("Günlük maksimum kayıp sınırı nedir?", 1, "risk.md", None)]
    assert "risk.md" in generator.messages[1]["content"]
    assert "Kullanılan kaynak parçaları" in format_grounded_answer(result)


def test_query_engine_does_not_call_llm_when_no_sources_exist() -> None:
    retriever = FakeRetriever([])
    class NeverCalledGenerator:
        def generate(self, messages):
            raise AssertionError("LLM çağrılmamalı")

    result = GroundedQueryEngine(retriever, NeverCalledGenerator()).ask("Belgede olmayan bilgi nedir?")

    assert result.status == "insufficient_context"
    assert result.used_sources is False
    assert "yeterli ve ilgili bilgi" in result.answer
