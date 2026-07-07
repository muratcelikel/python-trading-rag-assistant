from pathlib import Path
import pytest

from trading_rag_assistant.documents import discover_documents, make_chunk_id


def test_discover_documents_returns_supported_files_in_order(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    nested = tmp_path / "a"
    nested.mkdir()
    (nested / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "ignored.pdf").write_text("x", encoding="utf-8")

    docs = discover_documents(tmp_path)
    assert [doc.source_key for doc in docs] == ["a/a.md", "b.txt"]


def test_discover_documents_rejects_missing_folder(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        discover_documents(tmp_path / "missing")


def test_make_chunk_id_changes_when_source_changes() -> None:
    assert make_chunk_id("a.txt", 1) != make_chunk_id("b.txt", 1)
    assert make_chunk_id("a.txt", 1).endswith("-chunk-1")
