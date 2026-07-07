import pytest

from trading_rag_assistant.retriever import SemanticRetriever
from trading_rag_assistant.schemas import RetrievedChunk


class FakeEmbedder:
    def __init__(self):
        self.question = None

    def embed_documents(self, texts):
        return []

    def embed_query(self, text):
        self.question = text
        return [0.3, 0.7]


class FakeStore:
    def __init__(self):
        self.query_embedding = None
        self.n_results = None
        self.source_key = None

    def query(self, query_embedding, n_results, source_key=None):
        self.query_embedding = query_embedding
        self.n_results = n_results
        self.source_key = source_key
        return [
            RetrievedChunk(3, "Yakın parça", "a.txt", "a.txt", 50, 60, 0.12),
            RetrievedChunk(4, "Uzak parça", "b.txt", "b.txt", 61, 70, 1.10),
        ]


def test_semantic_retriever_filters_chunks_above_distance_threshold() -> None:
    embedder = FakeEmbedder()
    store = FakeStore()
    retriever = SemanticRetriever(embedder, store, max_distance=0.50)
    results = retriever.search("Günlük zarar limiti nedir?", top_k=2, source_key="a.txt")

    assert embedder.question == "Günlük zarar limiti nedir?"
    assert store.query_embedding == [0.3, 0.7]
    assert store.n_results == 2
    assert store.source_key == "a.txt"
    assert [item.chunk_id for item in results] == [3]


def test_semantic_retriever_can_disable_threshold() -> None:
    retriever = SemanticRetriever(FakeEmbedder(), FakeStore(), max_distance=None)
    assert len(retriever.search("Soru")) == 2


def test_semantic_retriever_rejects_blank_question() -> None:
    retriever = SemanticRetriever(FakeEmbedder(), FakeStore())
    with pytest.raises(ValueError, match="boş"):
        retriever.search("   ")
