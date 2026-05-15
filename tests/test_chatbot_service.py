"""Tests del dominio sin red — usa FakeLLM + FakeRetriever.

Obligatorio para banda 10: demuestra que el dominio es testeable
sin infraestructura real (sin Ollama, sin ChromaDB, sin red).
"""

from agente_rag.domain.chatbot_service import ChatbotService
from agente_rag.domain.entities import Question, Chunk, REJECTION_PHRASE
from agente_rag.adapters.llm.fake_llm import FakeLLM
from agente_rag.adapters.retriever.fake_retriever import FakeRetriever


def test_chatbot_returns_answer_with_sources():
    """El servicio devuelve un Answer con texto, fuentes y chunks."""
    llm = FakeLLM(canned_response="DNI es una asociación de voluntariado (01_faq_dni.txt).")
    retriever = FakeRetriever(chunks=[
        Chunk(source="01_faq_dni.txt", text="DNI es una asociación juvenil.", score=0.95),
        Chunk(source="04_filosofia_dni.txt", text="La filosofía de DNI...", score=0.80),
    ])
    bot = ChatbotService(llm=llm, retriever=retriever)

    answer = bot.answer(Question(text="¿Qué es DNI?"))

    assert "DNI" in answer.text
    assert "01_faq_dni.txt" in answer.sources
    assert len(answer.chunks) == 2
    assert answer.stats is not None


def test_chatbot_preserves_source_order():
    """Las fuentes se devuelven únicas y en orden de aparición."""
    chunks = [
        Chunk(source="03_charlas_abuelitos.txt", text="a", score=0.9),
        Chunk(source="01_faq_dni.txt", text="b", score=0.8),
        Chunk(source="03_charlas_abuelitos.txt", text="c", score=0.7),
    ]
    bot = ChatbotService(FakeLLM(), FakeRetriever(chunks=chunks))

    answer = bot.answer(Question(text="¿algo?"))

    assert answer.sources == ["03_charlas_abuelitos.txt", "01_faq_dni.txt"]


def test_chatbot_includes_rejection_phrase_in_prompt():
    """El prompt enviado al LLM contiene la frase de rechazo literal."""
    llm = FakeLLM()
    bot = ChatbotService(llm=llm, retriever=FakeRetriever())

    bot.answer(Question(text="¿Algo?"))

    assert REJECTION_PHRASE in llm.last_prompt


def test_chatbot_stats_contain_required_fields():
    """Las métricas devueltas contienen los campos de banda 7."""
    bot = ChatbotService(FakeLLM(), FakeRetriever())
    answer = bot.answer(Question(text="¿test?"))

    for key in ("prompt_tokens", "output_tokens", "tokens_per_sec", "latencia_s"):
        assert key in answer.stats, f"falta métrica {key!r}"


def test_chatbot_handles_empty_retrieval():
    """Si no se recuperan chunks, el servicio sigue funcionando."""
    empty_retriever = FakeRetriever(chunks=[])
    # Verificar que el retriever devuelve vacío
    assert empty_retriever.retrieve("test") == []
    bot = ChatbotService(FakeLLM(), empty_retriever)
    result = bot.answer(Question(text="¿algo?"))

    assert result.text  # tiene respuesta (del fake)
    assert result.chunks == []
