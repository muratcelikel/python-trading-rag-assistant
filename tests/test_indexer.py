from pathlib import Path

from trading_rag_assistant.indexer import index_directory, index_document


class FakeEmbedder:
    def embed_documents(self, texts):
        return [[float(index + 1), 0.0] for index, _ in enumerate(texts)]

    def embed_query(self, text):
        return [1.0, 0.0]


class FakeStore:
    def __init__(self):
        self.deleted_sources = []
        self.saved = None

    def delete_source(self, source_key):
        self.deleted_sources.append(source_key)

    def upsert(self, ids, documents, metadatas, embeddings):
        self.saved = {
            "ids": list(ids), "documents": list(documents),
            "metadatas": list(metadatas), "embeddings": list(embeddings),
        }


def test_index_document_replaces_same_source_and_stores_source_key(tmp_path: Path) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("Trend filtresi kullanılır. Risk limiti yüzde ikidir.", encoding="utf-8")
    store = FakeStore()

    result = index_document(source, FakeEmbedder(), store, chunk_size=4, overlap=1, source_key="folder/sample.txt")

    assert result["source_key"] == "folder/sample.txt"
    assert store.deleted_sources == ["folder/sample.txt"]
    assert store.saved["metadatas"][0]["source_key"] == "folder/sample.txt"
    assert store.saved["ids"][0].endswith("-chunk-1")


def test_index_directory_indexes_supported_files_recursively(tmp_path: Path) -> None:
    (tmp_path / "one.txt").write_text("Bir iki üç dört beş.", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "two.md").write_text("Alt belge metni.", encoding="utf-8")
    (tmp_path / "ignore.pdf").write_text("desteklenmez", encoding="utf-8")

    class DirectoryStore(FakeStore):
        def __init__(self):
            super().__init__()
            self.calls = []
        def upsert(self, ids, documents, metadatas, embeddings):
            self.calls.append((list(ids), list(metadatas)))

    store = DirectoryStore()
    report = index_directory(tmp_path, FakeEmbedder(), store, chunk_size=10, overlap=1)

    assert [row["source_key"] for row in report] == ["nested/two.md", "one.txt"]
    assert len(store.calls) == 2
