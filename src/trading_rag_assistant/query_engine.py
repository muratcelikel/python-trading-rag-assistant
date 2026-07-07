"""Source-grounded question-answer orchestration."""

from __future__ import annotations

from .answer_schema import GroundedAnswer
from .config import DEFAULT_TOP_K, NO_SOURCE_ANSWER
from .llm_client import AnswerGenerator
from .prompting import build_grounded_messages
from .retriever import SemanticRetriever


class GroundedQueryEngine:
    """Retrieve relevant chunks, generate a constrained answer, preserve sources."""

    def __init__(
        self,
        retriever: SemanticRetriever,
        answer_generator: AnswerGenerator,
        default_top_k: int = DEFAULT_TOP_K,
    ) -> None:
        if default_top_k <= 0:
            raise ValueError("default_top_k sıfırdan büyük olmalıdır.")
        self.retriever = retriever
        self.answer_generator = answer_generator
        self.default_top_k = default_top_k

    def ask(
        self,
        question: str,
        top_k: int | None = None,
        source_key: str | None = None,
        max_distance: float | None = None,
    ) -> GroundedAnswer:
        """Answer only when retrieval finds sufficiently relevant local evidence."""
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Soru boş olamaz.")
        limit = top_k if top_k is not None else self.default_top_k
        if limit <= 0:
            raise ValueError("top_k sıfırdan büyük olmalıdır.")

        sources = self.retriever.search(
            question,
            top_k=limit,
            source_key=source_key,
            max_distance=max_distance,
        )
        if not sources:
            return GroundedAnswer(
                question=question,
                answer=NO_SOURCE_ANSWER,
                sources=[],
                status="insufficient_context",
            )

        answer = self.answer_generator.generate(build_grounded_messages(question, sources))
        return GroundedAnswer(
            question=question,
            answer=answer,
            sources=sources,
            status="answered",
        )
