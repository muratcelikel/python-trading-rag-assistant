from pathlib import Path

from trading_rag_assistant.pipeline import prepare_document


def test_prepare_document_returns_metadata_and_chunks(tmp_path: Path) -> None:
    file_path = tmp_path / "notes.md"
    file_path.write_text(
        "Trend filtresi kullanılır.\n\nRisk sınırı yüzde ikidir.",
        encoding="utf-8",
    )

    result = prepare_document(file_path, chunk_size=5, overlap=1)

    assert result["source"].endswith("notes.md")
    assert result["word_count"] > 0
    assert result["chunk_count"] >= 1
