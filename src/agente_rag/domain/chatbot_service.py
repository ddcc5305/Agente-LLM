from .ports import LLMPort, RetrieverPort
from .entities import Question, Answer

class ChatbotService:
    def __init__(self, llm: LLMPort, retriever: RetrieverPort):
        self.llm = llm
        self.retriever = retriever

    def answer(self, question: Question) -> Answer:
        relevant_chunks = self.retriever.retrieve(question.text, k=5)
        context_str = "\n\n".join([f"[{c.source}]: {c.text}" for c in relevant_chunks])
        
        prompt = f"""Eres un asistente experto de la asociación DNI Valencia.
Responde SOLO con el CONTEXTO. Si no lo sabes, di: "No tengo esa información en mis fuentes".
CONTEXTO: {context_str}
PREGUNTA: {question.text}
RESPUESTA:"""

        # Ahora generate() devuelve un dict {"text": ..., "stats": ...}
        gen_result = self.llm.generate(prompt)
        
        return Answer(
            text=gen_result["text"],
            sources=list({c.source for c in relevant_chunks}),
            chunks=relevant_chunks,
            stats=gen_result["stats"] # <--- PASAMOS LAS STATS REALES
        )