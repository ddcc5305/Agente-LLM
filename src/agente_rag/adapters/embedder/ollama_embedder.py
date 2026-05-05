import requests
from agente_rag.config import SETTINGS

class OllamaEmbedder:
    def __init__(self):
        self.url = f"{SETTINGS.ollama_url.replace('/api', '')}/api/embeddings"
        self.model = SETTINGS.embed_model

    def embed(self, text: str) -> list[float]:
        """Llamada a Ollama para generar el embedding."""
        r = requests.post(
            self.url,
            json={"model": self.model, "prompt": text}
        )
        r.raise_for_status()
        return r.json()["embedding"]