import pytest

from trading_rag_assistant.chunker import chunk_text


def test_chunk_text_creates_overlap() -> None:
    text = "bir iki üç dört beş altı yedi sekiz dokuz on"
    chunks = chunk_text(text, chunk_size=5, overlap=2)
    assert len(chunks) == 3
    assert chunks[0].text == "bir iki üç dört beş"
    assert chunks[1].text.startswith("dört beş")


def test_chunk_text_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        chunk_text("örnek metin", chunk_size=5, overlap=5)
