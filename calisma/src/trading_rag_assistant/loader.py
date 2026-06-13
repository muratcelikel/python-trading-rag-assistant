"""Text document loading utilities."""

from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md"}


def load_text_file(file_path: str | Path) -> str:
    """Read a UTF-8 TXT or Markdown file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {path}")
    if not path.is_file():
        raise ValueError(f"Geçerli bir dosya yolu değil: {path}")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Desteklenmeyen dosya türü. Desteklenenler: {supported}")

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Dosya boş: {path}")

    return content
