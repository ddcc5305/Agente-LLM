"""Adapter Embedder falso para tests sin red."""


class FakeEmbedder:
    """Embedder que devuelve vectores constantes — para tests unitarios."""

    def __init__(self, dim: int = 768):
        self.dim = dim

    def embed(self, text: str) -> list[float]:
        # Vector simple basado en hash del texto para que sea determinista
        h = hash(text) % 1000
        return [float(h % (i + 1)) / 1000.0 for i in range(self.dim)]
