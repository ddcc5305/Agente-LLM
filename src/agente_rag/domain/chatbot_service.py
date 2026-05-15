"""Servicio de dominio — lógica del agente RAG.

Este módulo NO importa nada de infraestructura (ni requests, ni chromadb,
ni ollama). Solo depende de los ports y entidades definidos en el dominio.
"""

from .ports import LLMPort, RetrieverPort
from .entities import Question, Answer, Chunk, REJECTION_PHRASE


class ChatbotService:
    """Orquesta el flujo RAG: percibir → decidir → actuar."""

    def __init__(self, llm: LLMPort, retriever: RetrieverPort):
        self.llm = llm
        self.retriever = retriever

    def answer(self, question: Question, k: int = 15) -> Answer:
        """Resuelve una pregunta usando RAG.

        1. Recupera los k chunks más relevantes.
        2. Construye un prompt con contexto + instrucciones anti-alucinación.
        3. Genera la respuesta con el LLM.
        4. Empaqueta el resultado con fuentes y métricas.
        """
        # Prefijo para mejorar recall con modelos Nomic
        query = f"search_query: {question.text}"
        relevant_chunks = self.retriever.retrieve(query, k=k)

        prompt = self._build_prompt(question.text, relevant_chunks)
        gen_result = self.llm.generate(prompt)

        # Fuentes únicas preservando orden de aparición
        seen = set()
        sources = []
        for c in relevant_chunks:
            if c.source not in seen:
                seen.add(c.source)
                sources.append(c.source)

        return Answer(
            text=gen_result.text,
            sources=sources,
            chunks=relevant_chunks,
            stats=gen_result.stats,
        )

    def _build_prompt(self, question: str, chunks: list[Chunk]) -> str:
        """Construye el prompt anti-alucinación con contexto y fuentes."""
        context_str = "\n\n".join(
            f"[{c.source}]: {c.text}" for c in chunks
        )

        return f"""Eres el asistente experto de la asociación voluntaria DNI Valencia.
Tu misión es responder de forma precisa y útil basándote EXCLUSIVAMENTE en el CONTEXTO proporcionado.

INSTRUCCIONES:
1. Sé DIRECTO y CONCISO. Ve al grano y responde solo a lo que se pregunta, sin dar información extra o rodeos innecesarios.
2. Si en el contexto aparecen nombres propios de lugares, direcciones o colegios relevantes para responder, DEBES incluirlos.
3. Si la respuesta no se encuentra en los fragmentos, di literalmente: "{REJECTION_PHRASE}".
4. Cita siempre el archivo fuente entre paréntesis.
5. Si el contexto contiene información contradictoria, presenta ambas versiones citando ambas fuentes.
6. Mantén un tono amable, joven y profesional.

CONTEXTO:
{context_str}

PREGUNTA: {question}
RESPUESTA:"""