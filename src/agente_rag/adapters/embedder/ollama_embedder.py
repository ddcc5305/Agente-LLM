"""Adapter Embedder → Ollama (nomic-embed-text).

Genera embeddings via POST /api/embeddings del servidor Ollama local.
"""

import requests


class OllamaEmbedder:
    """Implementa EmbedderPort usando Ollama para embeddings."""

    def __init__(self, base_url: str = "http://localhost:11434/api",
                 model: str = "nomic-embed-text", verify_ssl: bool = True):
        self.url = f"{base_url}/embeddings"
        self.model = model
        self.verify_ssl = verify_ssl

    def embed(self, text: str) -> list[float]:
        """Devuelve el embedding de ``text``."""
        r = requests.post(
            self.url,
            json={"model": self.model, "prompt": text},
            verify=self.verify_ssl,
            timeout=60,
        )
        r.raise_for_status()
        payload = r.json()
        if "embedding" not in payload:
            raise RuntimeError(f"Respuesta inesperada del embedder: {payload}")
        return payload["embedding"]