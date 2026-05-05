from typing import Protocol, List
from .entities import Chunk

class LLMPort(Protocol):
    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        """Contrato para cualquier modelo de lenguaje."""
        ...

class RetrieverPort(Protocol):
    def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        """Contrato para cualquier motor de búsqueda."""
        ...