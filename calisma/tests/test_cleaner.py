import pytest

from trading_rag_assistant.cleaner import clean_text


def test_clean_text_normalizes_whitespace() -> None:
    raw = "İlk   satır\naynı paragraf.\n\n  İkinci    paragraf. "
    cleaned = clean_text(raw)
    assert cleaned == "İlk satır aynı paragraf.\n\nİkinci paragraf."


def test_clean_text_rejects_non_string() -> None:
    with pytest.raises(TypeError):
        clean_text(123)  # type: ignore[arg-type]
