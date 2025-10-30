from core.rag.hierarchical import DEFAULT_RETRIEVER


def test_retriever_returns_citations():
    citations = DEFAULT_RETRIEVER.retrieve("tenant1", "consultoria", "lead123")
    assert citations, "El retriever debe devolver al menos una cita"
