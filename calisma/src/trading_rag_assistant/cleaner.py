"""Basic text cleaning functions."""

import re


def clean_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph boundaries."""
    if not isinstance(text, str):
        raise TypeError("Metin değeri str olmalıdır.")

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = []

    for raw_paragraph in re.split(r"\n\s*\n", normalized):
        paragraph = re.sub(r"[ \t]+", " ", raw_paragraph)
        paragraph = re.sub(r"\s*\n\s*", " ", paragraph).strip()
        if paragraph:
            paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)
