from agente_rag.config import get_chatbot_service
from agente_rag.domain.entities import Question

# Instancia única del servicio para eficiencia
_service = get_chatbot_service()

def answer(pregunta: str, conversation_id: str | None = None, k: int = 5) -> dict:
    q = Question(text=pregunta, conversation_id=conversation_id)
    res = _service.answer(q) # res debe ser el objeto Answer del dominio
    
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