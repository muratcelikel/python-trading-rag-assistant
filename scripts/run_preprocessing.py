"""Run preprocessing on the sample document."""

from pathlib import Path

from trading_rag_assistant.pipeline import prepare_document


def main() -> None:
    sample_path = Path("data/sample/sample_strategy_notes.txt")
    result = prepare_document(sample_path, chunk_size=60, overlap=10)

    print(f"Kaynak: {result['source']}")
    print(f"Kelime sayısı: {result['word_count']}")
    print(f"Parça sayısı: {result['chunk_count']}")

    for chunk in result["chunks"]:
        print("\n" + "-" * 60)
        print(f"Parça {chunk.chunk_id} ({chunk.start_word}-{chunk.end_word})")
        print(chunk.text)


if __name__ == "__main__":
    main()
