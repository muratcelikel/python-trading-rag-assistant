"""Discovery and identity helpers for supported source documents."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from .loader import SUPPORTED_EXTENSIONS


@dataclass(frozen=True)
class SourceDocument:
    """A supported local document with a stable key relative to its source folder."""

    path: Path
    source_key: str


def discover_documents(directory: str | Path) -> list[SourceDocument]:
    """Find supported TXT/MD files recursively in deterministic order."""
    root = Path(directory)
    if not root.exists():
        raise FileNotFoundError(f"Kaynak klasörü bulunamadı: {root}")
    if not root.is_dir():
        raise ValueError(f"Kaynak yolu bir klasör olmalıdır: {root}")

    documents: list[SourceDocument] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.append(
                SourceDocument(path=path, source_key=path.relative_to(root).as_posix())
            )
    return documents


def make_chunk_id(source_key: str, chunk_id: int) -> str:
    """Create a Chroma-safe stable ID that avoids filename collisions."""
    digest = sha256(source_key.encode("utf-8")).hexdigest()[:16]
    return f"{digest}-chunk-{chunk_id}"
