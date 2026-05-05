from openai import OpenAI
from agente_rag.config import SETTINGS
from agente_rag.domain.ports import LLMPort

class PoliGPTLLM:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://api.poligpt.upv.es/v1",
            api_key=api_key
        )

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        # Nota: Requiere VPN de la UPV activa[cite: 3]
        resp = self.client.chat.completions.create(
            model="poligpt",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return resp.choices[0].message.content