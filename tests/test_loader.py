from pathlib import Path

import pytest

from trading_rag_assistant.loader import load_text_file


def test_load_text_file_reads_utf8_content(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Örnek trading notu", encoding="utf-8")
    assert load_text_file(file_path) == "Örnek trading notu"


def test_load_text_file_rejects_unsupported_extension(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    file_path.write_text("test", encoding="utf-8")
    with pytest.raises(ValueError, match="Desteklenmeyen"):
        load_text_file(file_path)
