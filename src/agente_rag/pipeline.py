"""Orquestador — adapta el dominio al contrato del enunciado §9.

Traduce la respuesta del dominio (Answer) al formato dict que el
corrector espera: {respuesta, fuentes, chunks, metricas, trazas}.
"""

from __future__ import annotations

from typing import Optional

from agente_rag.domain.entities import Question

# Lazy init para no provocar side-effects al importar (timeout del corrector)
_service = None


def _get_service():
    global _service
    if _service is None:
        from agente_rag.config import get_chatbot_service
        _service = get_chatbot_service()
    return _service


def answer(pregunta: str, conversation_id: Optional[str] = None, k: int = 15,
           model_override: str | None = None, backend_override: str | None = None) -> dict:
    """Punto de entrada del pipeline RAG.

    Si se pasa model_override, crea un servicio con ese modelo (para benchmark).
    """
    if model_override or backend_override:
        from agente_rag.config import get_chatbot_service
        service = get_chatbot_service(model_override=model_override, backend_override=backend_override)
    else:
        service = _get_service()

    q = Question(text=pregunta, conversation_id=conversation_id)
    res = service.answer(q, k=k)

    return {
        "respuesta": res.text,
        "fuentes": res.sources,
        "chunks": [
            {"source": c.source, "text": c.text, "score": c.score}
            for c in res.chunks
        ],
        "metricas": res.stats,
        "trazas": [],
    }