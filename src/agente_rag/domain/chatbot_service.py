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

CONTEXTO:
{context_str}

INSTRUCCIONES PARA LA RESPUESTA:
1. Responde ÚNICAMENTE si la información exacta por la que se pregunta está contenida en el CONTEXTO.
2. Si la pregunta trata sobre un tema, objeto o servicio que NO está mencionado en el CONTEXTO (por ejemplo, trenes, transporte, autobús, cuotas, o cualquier tema ajeno), debes responder única y exclusivamente con la frase literal: "{REJECTION_PHRASE}". No aportes ningún otro dato.
3. Sé DIRECTO y CONCISO. Ve al grano y responde solo a lo que se pregunta, sin dar información extra o rodeos innecesarios.
4. Cita siempre el archivo fuente entre paréntesis al final de la respuesta.
5. Si el contexto contiene información contradictoria o versiones distintas sobre el tema preguntado (como diferentes horarios para los desayunos), estás OBLIGADO a presentar ambas versiones de manera objetiva citando la fuente de cada una. No elijas una sola.
6. Si en el contexto aparecen nombres propios de lugares, direcciones o colegios relevantes para responder, DEBES incluirlos.
7. Mantén un tono amable, joven y profesional.

PREGUNTA: {question}
RESPUESTA:"""