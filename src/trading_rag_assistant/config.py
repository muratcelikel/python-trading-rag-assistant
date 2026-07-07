"""Central configuration for retrieval and grounded answer generation."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load a local .env file before any client reads environment variables.
load_dotenv()

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "trading_notes"
DEFAULT_TOP_K = 3

# Chroma cosine distance is smaller for nearer results. This is a starting guardrail,
# not a universal quality guarantee; it can be changed from .env during calibration.
DEFAULT_MAX_DISTANCE = float(os.getenv("RETRIEVAL_MAX_DISTANCE", "0.85"))

DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
LLM_TEMPERATURE = 0.0
LLM_MAX_COMPLETION_TOKENS = 500

NO_SOURCE_ANSWER = (
    "Sağlanan kaynaklarda bu soruyu yanıtlayacak yeterli ve ilgili bilgi bulunamadı."
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_DB_DIRECTORY = PROJECT_ROOT / "data" / "chroma"
OUTPUT_DIRECTORY = PROJECT_ROOT / "output"


def get_groq_api_key() -> str:
    """Return the configured Groq key or raise a clear local setup error."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY bulunamadı. "
            ".env.example dosyasını .env olarak kopyalayın ve anahtarı ekleyin."
        )
    return key
