"""Adapter LLM → PoliGPT (API UPV compatible con OpenAI).

Requiere VPN de la UPV activa y clave API en variable de entorno.
"""

import time

from openai import OpenAI

from agente_rag.domain.entities import GenerationResult


class PoliGPTLLM:
    """Implementa LLMPort conectándose a PoliGPT UPV."""

    def __init__(self, api_key: str, base_url: str = "https://api.poligpt.upv.es/v1",
                 model: str = "poligpt"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.2) -> GenerationResult:
        t0 = time.time()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        elapsed = time.time() - t0

        usage = resp.usage
        prompt_tokens = usage.prompt_tokens if usage else 0
        output_tokens = usage.completion_tokens if usage else 0
        tokens_per_sec = (
            output_tokens / elapsed if elapsed > 0 else 0.0
        )

        return GenerationResult(
            text=resp.choices[0].message.content,
            stats={
                "prompt_tokens": prompt_tokens,
                "output_tokens": output_tokens,
                "tokens_per_sec": round(tokens_per_sec, 2),
                "latencia_s": round(elapsed, 2),
                "modelo": self.model,
            },
        )