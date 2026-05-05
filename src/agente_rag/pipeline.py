from agente_rag.config import get_chatbot_service
from agente_rag.domain.entities import Question

from typing import Optional

# Instancia única del servicio para eficiencia
_service = get_chatbot_service()

def answer(pregunta: str, conversation_id: Optional[str] = None, k: int = 15) -> dict:
    q = Question(text=pregunta, conversation_id=conversation_id)

    res = _service.answer(q, k=k)
    
    # El contrato oficial exige esta estructura exacta
    return {
        "respuesta": res.text,  
        "fuentes": res.sources, 
        "chunks": [
            {"source": c.source, "text": c.text, "score": c.score} 
            for c in res.chunks
        ],
        "metricas": res.stats,  
        "trazas": []
    }