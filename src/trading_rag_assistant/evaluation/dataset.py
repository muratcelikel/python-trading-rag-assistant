"""Small human-authored evaluation dataset loader."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class RetrievalTestCase:
    question: str
    expected_source_key: str


def load_retrieval_testset(path: str | Path) -> list[RetrievalTestCase]:
    """Load a simple JSON test set with question and expected source fields."""
    testset_path = Path(path)
    raw = json.loads(testset_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Test set JSON kök seviyesi liste olmalıdır.")

    cases: list[RetrievalTestCase] = []
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Test set satırı {index} nesne olmalıdır.")
        question = str(item.get("question", "")).strip()
        source = str(item.get("expected_source_key", "")).strip()
        if not question or not source:
            raise ValueError(f"Test set satırı {index} question ve expected_source_key içermelidir.")
        cases.append(RetrievalTestCase(question=question, expected_source_key=source))
    return cases
