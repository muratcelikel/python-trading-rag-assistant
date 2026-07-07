"""Small Groq client adapter used by the grounded query engine."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from .config import (
    DEFAULT_GROQ_MODEL,
    LLM_MAX_COMPLETION_TOKENS,
    LLM_TEMPERATURE,
    get_groq_api_key,
)


class AnswerGenerator(Protocol):
    """Interface that makes the query engine easy to test without network calls."""

    def generate(self, messages: Sequence[dict[str, str]]) -> str:
        """Generate a plain-text answer from chat messages."""


class GroqAnswerGenerator:
    """Synchronous Groq Chat Completions adapter."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_GROQ_MODEL,
        temperature: float = LLM_TEMPERATURE,
        max_completion_tokens: int = LLM_MAX_COMPLETION_TOKENS,
    ) -> None:
        self.api_key = api_key or get_groq_api_key()
        self.model = model
        self.temperature = temperature
        self.max_completion_tokens = max_completion_tokens
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from groq import Groq
            except ImportError as exc:
                raise RuntimeError(
                    "groq paketi kurulu değil. "
                    "Önce `python -m pip install -e .[dev]` komutunu çalıştırın."
                ) from exc

            self._client = Groq(api_key=self.api_key)

        return self._client

    def generate(self, messages: Sequence[dict[str, str]]) -> str:
        """Call Groq and return non-empty response text."""
        if not messages:
            raise ValueError("LLM mesaj listesi boş olamaz.")

        try:
            completion = self._get_client().chat.completions.create(
                model=self.model,
                messages=list(messages),
                temperature=self.temperature,
                max_completion_tokens=self.max_completion_tokens,
            )
        except Exception as exc:
            raise RuntimeError(
                "Groq cevap isteği başarısız oldu. "
                "API anahtarını, model adını ve internet bağlantısını kontrol edin."
            ) from exc

        content = completion.choices[0].message.content
        if not content or not content.strip():
            raise RuntimeError("Groq boş bir cevap döndürdü.")

        return content.strip()
