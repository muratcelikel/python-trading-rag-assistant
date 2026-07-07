import pytest

from trading_rag_assistant.llm_client import GroqAnswerGenerator


def test_groq_client_rejects_empty_message_list() -> None:
    client = GroqAnswerGenerator(api_key="test-key")

    with pytest.raises(ValueError, match="boş"):
        client.generate([])
