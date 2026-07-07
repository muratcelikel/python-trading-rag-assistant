from trading_rag_assistant.citations import format_citation, format_retrieval_results
from trading_rag_assistant.schemas import RetrievedChunk


def make_chunk() -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=2,
        text="Risk sınırı yüzde ikidir.",
        source_file="sample_strategy_notes.txt",
        source_key="sample_strategy_notes.txt",
        start_word=21,
        end_word=25,
        distance=0.08,
    )


def test_format_citation_contains_source_and_chunk_number() -> None:
    citation = format_citation(make_chunk())
    assert "sample_strategy_notes.txt" in citation
    assert "Parça 2" in citation


def test_format_retrieval_results_contains_text_distance_and_hint() -> None:
    output = format_retrieval_results([make_chunk()])
    assert "Risk sınırı yüzde ikidir." in output
    assert "Mesafe: 0.0800" in output
    assert "Benzerlik ipucu" in output
