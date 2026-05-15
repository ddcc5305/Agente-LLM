"""Adapter Retriever falso para tests del dominio sin red."""

from agente_rag.domain.entities import Chunk


class FakeRetriever:
    """Retriever que devuelve chunks pregrabados — para tests unitarios."""

    def __init__(self, chunks: list[Chunk] | None = None):
        if chunks is not None:
            self.chunks = chunks
        else:
            self.chunks = [
                Chunk(
                    source="01_faq_dni.txt",
                    text="Q: ¿Qué es DNI? A: DNI (Damos Nuestra Ilusión) es una asociación juvenil de voluntariado en Valencia.",
                    score=0.95,
                ),
            ]
        self.last_query = None

    def retrieve(self, query: str, k: int = 5) -> list[Chunk]:
        self.last_query = query
        return self.chunks[:k]
