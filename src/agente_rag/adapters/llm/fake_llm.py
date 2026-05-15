"""Adapter LLM falso para tests del dominio sin red."""

from agente_rag.domain.entities import GenerationResult


class FakeLLM:
    """LLM que devuelve respuestas pregrabadas — para tests unitarios."""

    def __init__(self, canned_response: str = "Los desayunos son a las 8h (01_faq_dni.txt)."):
        self.canned_response = canned_response
        self.last_prompt = None

    def generate(self, prompt: str, temperature: float = 0.2) -> GenerationResult:
        self.last_prompt = prompt
        return GenerationResult(
            text=self.canned_response,
            stats={
                "prompt_tokens": 100,
                "output_tokens": 20,
                "tokens_per_sec": 50.0,
                "latencia_s": 0.01,
                "modelo": "fake",
            },
        )
