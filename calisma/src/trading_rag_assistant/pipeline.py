"""Document preprocessing pipeline."""

from pathlib import Path
from typing import Any

from .chunker import chunk_text
from .cleaner import clean_text
from .loader import load_text_file


def prepare_document(
    file_path: str | Path,
    chunk_size: int = 100,
    overlap: int = 20,
) -> dict[str, Any]:
    """Load, clean and chunk a text document."""
    path = Path(file_path)
    raw_text = load_text_file(path)
    cleaned_text = clean_text(raw_text)
    chunks = chunk_text(cleaned_text, chunk_size=chunk_size, overlap=overlap)

    return {
        "source": str(path),
        "character_count": len(cleaned_text),
        "word_count": len(cleaned_text.split()),
        "chunk_count": len(chunks),
        "chunks": chunks,
    }
