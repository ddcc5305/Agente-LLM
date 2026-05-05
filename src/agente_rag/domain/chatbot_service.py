from .ports import LLMPort, RetrieverPort
from .entities import Question, Answer

class ChatbotService:
    def __init__(self, llm: LLMPort, retriever: RetrieverPort):
        self.llm = llm
        self.retriever = retriever

    def answer(self, question: Question, k: int = 15) -> Answer:
        """
        Resuelve una pregunta utilizando RAG optimizado
        
        Ajustes aplicados:
        - Query Refinement: Prefijo 'search_query:' para mejorar el recall de Nomic.
        - Detail-Oriented Prompt: Obliga a priorizar entidades y nombres específicos.
        """
        
        query_para_retriever = f"search_query: {question.text}"
        relevant_chunks = self.retriever.retrieve(query_para_retriever, k=k)
        
        context_str = "\n\n".join([f"[{c.source}]: {c.text}" for c in relevant_chunks])
        
        prompt = f"""Eres el asistente experto de la asociación voluntaria DNI Valencia. 
Tu misión es responder de forma precisa y útil basándote EXCLUSIVAMENTE en el CONTEXTO proporcionado.

INSTRUCCIONES DE CALIDAD:
1. Si en el contexto aparecen nombres propios de lugares, direcciones o colegios (ej: CEIP Antonio Ferrandis, Residencia L'Acollida, Porta de la Mar), DEBES incluirlos en tu respuesta.
2. Prioriza siempre la información detallada sobre las descripciones generales.
3. Si la respuesta no se encuentra en los fragmentos, di: "No tengo esa información en mis fuentes".
4. Mantén un tono amable, joven y profesional.

CONTEXTO:
{context_str}

PREGUNTA: {question.text}
RESPUESTA:"""

        gen_result = self.llm.generate(prompt)
        
        return Answer(
            text=gen_result["text"],
            sources=list({c.source for c in relevant_chunks}),
            chunks=relevant_chunks,
            stats=gen_result["stats"] 
        )