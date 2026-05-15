"""Tests del prompt anti-alucinación. No requieren Ollama."""

from agente_rag.domain.entities import Chunk, REJECTION_PHRASE
from agente_rag.domain.chatbot_service import ChatbotService
from agente_rag.adapters.llm.fake_llm import FakeLLM
from agente_rag.adapters.retriever.fake_retriever import FakeRetriever


def test_prompt_includes_rejection_phrase_literal():
    llm = FakeLLM()
    bot = ChatbotService(llm=llm, retriever=FakeRetriever())
    bot.answer(type("Q", (), {"text": "¿Algo?"})())

    assert REJECTION_PHRASE in llm.last_prompt, \
        "el prompt debe contener la frase de rechazo literal"


def test_prompt_includes_context_with_source_tags():
    chunks = [
        Chunk(source="03_charlas_abuelitos.txt", text="Charlas con mayores"),
        Chunk(source="01_faq_dni.txt", text="FAQ sobre DNI"),
    ]
    llm = FakeLLM()
    bot = ChatbotService(llm=llm, retriever=FakeRetriever(chunks=chunks))
    from agente_rag.domain.entities import Question
    bot.answer(Question(text="¿Qué son las charlas?"))

    assert "[03_charlas_abuelitos.txt]" in llm.last_prompt
    assert "[01_faq_dni.txt]" in llm.last_prompt
    assert "Charlas con mayores" in llm.last_prompt


def test_prompt_includes_question():
    llm = FakeLLM()
    bot = ChatbotService(llm=llm, retriever=FakeRetriever())
    from agente_rag.domain.entities import Question
    bot.answer(Question(text="¿Pregunta concreta?"))

    assert "¿Pregunta concreta?" in llm.last_prompt
