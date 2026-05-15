"""Agente RAG — Asistente DNI Valencia (arquitectura hexagonal).

Estructura del paquete:
- domain/: entidades, ports y servicio de dominio (sin deps externas).
- adapters/: implementaciones concretas (Ollama, PoliGPT, ChromaDB, FAISS...).
- config: composition root — ensambla adapters según .env.
- pipeline: adapta el dominio al contrato del enunciado §9.
- chunker: troceo de los .txt del corpus.
"""

__version__ = "0.1.0"
