"""Delete the local Chroma collection used by this project."""

from trading_rag_assistant.vector_store import ChromaVectorStore


if __name__ == "__main__":
    ChromaVectorStore().clear()
    print("Yerel Chroma koleksiyonu temizlendi.")
