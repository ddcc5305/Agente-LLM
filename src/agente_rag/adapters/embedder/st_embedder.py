"""Adapter Embedder con sentence-transformers — segunda implementación del EmbedderPort.

Alternativa local a Ollama embeddings. No requiere servidor externo.
Usa paraphrase-multilingual-MiniLM-L12-v2 (384 dims, multilingüe).
"""

from sentence_transformers import SentenceTransformer


class STEmbedder:
    """Embedder local usando sentence-transformers (sin Ollama)."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        """Genera el embedding de un texto."""
        return self.model.encode(text, normalize_embeddings=True).tolist()
