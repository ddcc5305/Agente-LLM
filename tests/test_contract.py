"""Tests del contrato (enunciado §9).

Verifican que consultar() devuelve el dict con la forma exacta
del contrato, usando FakeLLM y FakeRetriever (sin red).
"""

from __future__ import annotations

from unittest.mock import patch

from agente_rag.domain.entities import Chunk, GenerationResult

CONTRACT_KEYS = {"respuesta", "fuentes", "chunks", "metricas", "trazas"}


def _fake_service_answer(question, k=15):
    """Simula ChatbotService.answer() con datos fake."""
    from agente_rag.domain.entities import Answer
    return Answer(
        text="DNI es una asociación de voluntariado (01_faq_dni.txt).",
        sources=["01_faq_dni.txt", "04_filosofia_dni.txt"],
        chunks=[
            Chunk(source="01_faq_dni.txt", text="DNI es una asociación...", score=0.91),
            Chunk(source="04_filosofia_dni.txt", text="Filosofía de DNI...", score=0.84),
        ],
        stats={
            "prompt_tokens": 420,
            "output_tokens": 37,
            "tokens_per_sec": 42.1,
            "latencia_s": 1.8,
            "modelo": "fake",
        },
    )


def test_consultar_signature_and_keys():
    with patch("agente_rag.pipeline._get_service") as mock:
        mock.return_value.answer = _fake_service_answer
        import consultar
        out = consultar.consultar("¿Qué es DNI?")

    assert set(out.keys()) >= CONTRACT_KEYS, f"faltan claves: {CONTRACT_KEYS - set(out.keys())}"
    assert isinstance(out["respuesta"], str) and out["respuesta"]
    assert isinstance(out["fuentes"], list)
    assert all(isinstance(s, str) for s in out["fuentes"])
    assert isinstance(out["chunks"], list)
    assert isinstance(out["metricas"], dict)


def test_metricas_have_banda7_fields():
    with patch("agente_rag.pipeline._get_service") as mock:
        mock.return_value.answer = _fake_service_answer
        import consultar
        out = consultar.consultar("¿algo?")

    metricas = out["metricas"]
    for k in ("prompt_tokens", "output_tokens", "tokens_per_sec", "latencia_s"):
        assert k in metricas, f"falta métrica {k!r}"
    assert metricas["output_tokens"] == 37
    assert metricas["tokens_per_sec"] == 42.1
