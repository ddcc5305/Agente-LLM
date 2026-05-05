from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    ollama_url: str
    llm_model: str
    embed_model: str
    verify_ssl: bool
    chroma_path: Path
    collection_name: str
    api_host: str
    api_port: int
    corpus_dir: Path

    @classmethod
    def from_env(cls) -> Settings:
        # Detectamos la raíz del proyecto (donde está .git)
        repo_root = Path(__file__).resolve().parents[2]
        return cls(
            ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434/api"),
            llm_model=os.getenv("LLM_MODEL", "gemma3:4b"), # Modelo local sugerido
            embed_model=os.getenv("EMBED_MODEL", "nomic-embed-text"),
            verify_ssl=True,
            chroma_path=repo_root / "data" / "chroma",
            collection_name="dni_valencia", # Cambiado para el caso DNI
            api_host="127.0.0.1",
            api_port=8000,
            corpus_dir=repo_root / "corpus", # Carpeta que sale en tu captura
        )

SETTINGS = Settings.from_env()

# Composition Root: Aquí instanciamos todo para la Banda 10
def get_chatbot_service():
    from .adapters.llm.ollama_llm import OllamaLLM
    from .adapters.retriever.chroma_adapter import ChromaRetriever
    from .adapters.embedder.ollama_embedder import OllamaEmbedder
    from .domain.chatbot_service import ChatbotService

    llm = OllamaLLM(base_url=SETTINGS.ollama_url, model=SETTINGS.llm_model)
    embedder = OllamaEmbedder()
    retriever = ChromaRetriever(
        path=str(SETTINGS.chroma_path), 
        collection_name=SETTINGS.collection_name,
        embed_fn=embedder.embed
    )
    return ChatbotService(llm=llm, retriever=retriever)