"""Ports (interfaces) del dominio — contratos para los adapters.

Define los 4 ports exigidos por la banda 10:
  - LLMPort (ILLMClient)
  - EmbedderPort (IEmbeddingsClient)
  - RetrieverPort (IRetriever)
  - VectorStorePort (IVectorStore)
"""

from typing import Protocol, List

from .entities import Chunk, GenerationResult


class LLMPort(Protocol):
    """Contrato para cualquier modelo de lenguaje."""

    def generate(self, prompt: str, temperature: float = 0.2) -> GenerationResult: ...


class EmbedderPort(Protocol):
    """Contrato para cualquier servicio de embeddings."""

    def embed(self, text: str) -> list[float]: ...


class RetrieverPort(Protocol):
    """Contrato para cualquier motor de búsqueda semántica."""

    def retrieve(self, query: str, k: int = 5) -> List[Chunk]: ...


class VectorStorePort(Protocol):
    """Contrato para cualquier almacén de vectores (indexación)."""

    def add_documents(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> int: ...

    def reset_collection(self) -> None: ...