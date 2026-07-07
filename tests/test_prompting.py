from trading_rag_assistant.prompting import build_grounded_messages
from trading_rag_assistant.schemas import RetrievedChunk


def test_build_grounded_messages_keeps_question_and_source_key() -> None:
    chunk = RetrievedChunk(4, "Günlük kayıp yüzde ikidir.", "risk.md", "risk.md", 40, 49, 0.11)
    messages = build_grounded_messages("Günlük kayıp limiti nedir?", [chunk])

    assert len(messages) == 2
    assert "yalnızca" in messages[0]["content"].lower()
    assert "risk.md" in messages[1]["content"]
    assert "Günlük kayıp limiti nedir?" in messages[1]["content"]
