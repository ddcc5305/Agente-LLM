"""Composition Root — monta los adapters según la configuración.

Cambiar de adapter = 1 línea en .env (ej: RETRIEVER_BACKEND=faiss).
Este es el ÚNICO módulo que importa adapters concretos.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    ollama_url: str
    llm_model: str
    embed_model: str
    verify_ssl: bool
    chroma_path: Path
    faiss_path: Path
    collection_name: str
    api_host: str
    api_port: int
    corpus_dir: Path
    retriever_backend: str  # "chroma" | "faiss"
    embedder_backend: str   # "ollama" | "st"
    llm_backend: str        # "ollama" | "poligpt"
    poligpt_api_key: str
    poligpt_base_url: str
    poligpt_model: str

    @classmethod
    def from_env(cls) -> Settings:
        repo_root = Path(__file__).resolve().parents[2]
        return cls(
            ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434/api"),
            llm_model=os.getenv("LLM_MODEL", "gemma3:4b"),
            embed_model=os.getenv("EMBED_MODEL", "nomic-embed-text"),
            verify_ssl=os.getenv("VERIFY_SSL", "true").lower() == "true",
            chroma_path=repo_root / "data" / "chroma",
            faiss_path=repo_root / "data" / "faiss",
            collection_name=os.getenv("COLLECTION_NAME", "dni_valencia"),
            api_host=os.getenv("API_HOST", "127.0.0.1"),
            api_port=int(os.getenv("API_PORT", "8000")),
            corpus_dir=repo_root / "corpus",
            retriever_backend=os.getenv("RETRIEVER_BACKEND", "chroma"),
            embedder_backend=os.getenv("EMBEDDER_BACKEND", "ollama"),
            llm_backend=os.getenv("LLM_BACKEND", "ollama"),
            poligpt_api_key=os.getenv("POLIGPT_API_KEY", ""),
            poligpt_base_url=os.getenv("POLIGPT_BASE_URL", "https://api.poligpt.upv.es/v1"),
            poligpt_model=os.getenv("POLIGPT_MODEL", "poligpt"),
        )


SETTINGS = Settings.from_env()


def _build_embedder():
    """Instancia el embedder según EMBEDDER_BACKEND."""
    if SETTINGS.embedder_backend == "st":
        from .adapters.embedder.st_embedder import STEmbedder
        return STEmbedder()
    else:
        from .adapters.embedder.ollama_embedder import OllamaEmbedder
        return OllamaEmbedder(
            base_url=SETTINGS.ollama_url,
            model=SETTINGS.embed_model,
            verify_ssl=SETTINGS.verify_ssl,
        )


def _build_retriever(embed_fn):
    """Instancia el retriever según RETRIEVER_BACKEND."""
    if SETTINGS.retriever_backend == "faiss":
        from .adapters.retriever.faiss_adapter import FAISSRetriever
        return FAISSRetriever(
            index_path=str(SETTINGS.faiss_path),
            embed_fn=embed_fn,
        )
    else:
        from .adapters.retriever.chroma_adapter import ChromaRetriever
        return ChromaRetriever(
            path=str(SETTINGS.chroma_path),
            collection_name=SETTINGS.collection_name,
            embed_fn=embed_fn,
        )


def _build_llm(model_override: str | None = None):
    """Instancia el LLM según LLM_BACKEND."""
    if SETTINGS.llm_backend == "poligpt":
        from .adapters.llm.poligpt_llm import PoliGPTLLM
        return PoliGPTLLM(
            api_key=SETTINGS.poligpt_api_key,
            base_url=SETTINGS.poligpt_base_url,
            model=model_override or SETTINGS.poligpt_model,
        )
    else:
        from .adapters.llm.ollama_llm import OllamaLLM
        return OllamaLLM(
            base_url=SETTINGS.ollama_url,
            model=model_override or SETTINGS.llm_model,
            verify_ssl=SETTINGS.verify_ssl,
        )


def get_chatbot_service(model_override: str | None = None):
    """Composition root: ensambla dominio + adapters."""
    from .domain.chatbot_service import ChatbotService

    embedder = _build_embedder()
    retriever = _build_retriever(embedder.embed)
    llm = _build_llm(model_override)
    return ChatbotService(llm=llm, retriever=retriever)